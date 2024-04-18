from flask import Flask, request, jsonify
from textprocess.textProcess import textProcess
from textprocess.mutiplyTextProcess import mutiplyTextProcess
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from loguru import logger
import time
import os

# 日志配置
logger.add("app.log", rotation="50MB", retention="10 days", level="INFO", colorize=True)

# Flask和数据库配置
load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False)


class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/api/upload_file", methods=["POST"])
def upload_file():
    if "file" in request.files and request.files["file"] != "":
        file = request.files["file"]
        # 文件大小检查
        if file.content_length > 1024 * 1024 * 5:
            return jsonify(
                {
                    "message": "文件大小超过5MB",
                    "status": "error",
                    "error": "file size too large",
                }
            )
        # 文件类型检查
        filename = secure_filename(file.filename)
        receive_file_type = [
            ".txt",
            "c",
            ".cpp",
            ".java",
            ".py",
            ".go",
            ".js",
            ".php",
            ".zip",
            ".rar",
            ".7z",
        ]
        if not any([filename.endswith(i) for i in receive_file_type]):
            response = jsonify(
                {
                    "message": "文件类型不支持",
                    "status": "error",
                    "error": "file type unsupported",
                }
            )
            response.status_code = 400
            return response
        # 保存文件
        timestamp = time.time()  # 时间戳区分文件
        filename = (
            filename.split(".")[0] + "_" + timestamp + "." + filename.split(".")[1]
        )
        name, type = filename.split(".")
        file_db = File(filename=name, type=type)
        with app.app_context():
            db.session.add(file_db)
            db.session.commit()
        # 保存文件名及类型到数据库
        file.save("upload/file/" + filename)
        logger.info(f"{time.time}：文件{filename}上传成功")

        # 保存文件
        return jsonify(
            {
                "message": "成功上传文件",
                "status": "success",
                "file_path": "upload/file/" + filename,
            }
        )
    else:  # 上传文件为空
        response = jsonify(
            {"message": "文件为空", "status": "error", "error": "empty file"}
        )
        response.status_code = 400
        return response


@app.route("/api/upload_text", methods=["POST"])
def upload_text():
    data = request.data
    if data == "":
        response = jsonify(
            {"message": "文本为空", "status": "error", "error": "empty text"}
        )
        response.status_code = 400
        return response
    else:
        timestamp = time.time()
        filename = "text_" + timestamp + ".txt"

        name, type = filename.split(".")
        text_db = Text(filename=name, type=type)
        with app.app_context():
            db.session.add(text_db)
            db.session.commit()
        # 保存文件名及类型到数据库
        with open("upload/text/" + filename, "w") as f:
            f.write(data["text"])
        logger.info(f"{time.time}：文本{filename}上传成功")

        return jsonify(
            {
                "message": "成功上传文本",
                "status": "success",
                "file_path": "upload/text/" + filename,
            }
        )


@app.route("/api/process", methods=["POST"])
def process_file():
    file_path = request.get_json()["file_path"]
    if file_path is None:
        response = jsonify(
            {"message": "文件路径为空", "status": "error", "error": "empty file path"}
        )
        response.status_code = 400
        return response
    # 数据库查询
    file_db = File.query.filter_by(
        filename=file_path.split("/")[-1].split(".")[0]
    ).first()
    if not file_db:
        response = jsonify(
            {"message": "文件不存在", "status": "error", "error": "file not found"}
        )
        response.status_code = 404
        return response
    conpress_type = ["zip", "rar", "7z"]
    text_return = textProcess(file_path)
    time_start = time.time()
    # 超时处理
    timeout = 1 * 60  # 1分钟
    while time.time() - time_start < timeout:
        try:
            if any(file_path.split(".")[-1] != i for i in conpress_type):
                text_return = mutiplyTextProcess(file_path)  # 处理压缩多文件
            else:
                text_return = textProcess(file_path)  # 处理普通文件
            if text_return is not None:
                break
        except Exception as e:
            response = jsonify(
                {"message": "处理失败", "status": "error", "error": "process error"}
            )
            response.status_code = 400
            return response
    else:
        response = jsonify(
            {"message": "处理超时", "status": "error", "error": "process timeout"}
        )
        response.status_code = 400
        return response

    logger.info(f"{time.time}：文件{file_path}处理成功")
    return jsonify({"message": "处理成功", "status": "success", "text": text_return})


if __name__ == "__main__":
    app.run(debug=True)
