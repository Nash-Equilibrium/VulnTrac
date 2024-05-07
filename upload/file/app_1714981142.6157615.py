from flask import Flask, request, jsonify
from textprocess.textProcess import textProcess
from textprocess.mutiplyTextProcess import mutiplyTextProcess
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from loguru import logger
from datetime import datetime
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_cors import CORS
import threading
import ctypes
import time
import os


# 日志配置
logger.add("app.log", rotation="50MB", retention="10 days", level="INFO", colorize=True)


# Flask和数据库配置
load_dotenv()
app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)


# File表
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(100), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.now)


# User表
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 0:普通用户 1:管理员
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)


# Analysis表
class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey("file.id"))
    result = db.Column(db.String(2000), nullable=False)
    status = db.Column(db.String(10), nullable=False)  # 0:未处理 1:处理中 2:处理完成
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)


# History表
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    file_id = db.Column(db.Integer, db.ForeignKey("file.id"))
    analysis_id = db.Column(db.Integer, db.ForeignKey("analysis.id"))
    created_at = db.Column(db.DateTime, default=datetime.now)


with app.app_context():
    db.create_all()

    login_manager = LoginManager()
    login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 主页
@app.route("/")
def index():
    return "Hello World!"


# 注册
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # 合法性检查放在前端
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        email = request.form["email"]
        role = 0
        new_user = User(username=username, password=password, email=email, role=role)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Registration successful", "status": "success"})
    return jsonify({"message": "Method not allowed", "status": "error"})


# 登录
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return jsonify({"message": "Login successful", "status": "success"})
        else:
            return jsonify(
                {"message": "Invalid username or password", "status": "error"}
            )
    return jsonify({"message": "Method not allowed", "status": "error"})


# 登出
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful", "status": "success"})


# 上传文件
@app.route("/api/upload_file", methods=["POST"])
# @login_required
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
        timestamp = str(time.time())  # 时间戳区分文件
        name, ext = os.path.splitext(filename)
        filename = name + "_" + timestamp + ext
        user_id = current_user.get_id()
        file_db = File(file_name=name, file_type=ext.lstrip("."), user_id=user_id)
        with app.app_context():
            db.session.add(file_db)
            db.session.commit()
        # 保存文件名及类型到数据库
        file.save("upload/file/" + filename)
        logger.info(f"{time.time()}：文件{filename}上传成功")

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


# 上传文本
@app.route("/api/upload_text", methods=["POST"])
# @login_required
def upload_text():
    # 处理文本
    text = request.form["text"]
    type = request.form["type"]

    if text == "":
        response = jsonify(
            {"message": "文本为空", "status": "error", "error": "empty text"}
        )
        response.status_code = 400
        return response
    else:
        timestamp = str(time.time())
        filename = "text_" + timestamp + ".txt"
        name, _ = os.path.splitext(filename)
        user_id = current_user.get_id()
        file_db = File(file_name=name, file_type=type, user_id=user_id)
        with app.app_context():
            db.session.add(file_db)
            db.session.commit()
        # 保存文件名及类型到数据库
        with open("upload/file/" + filename, "w") as f:
            f.write(text)
        logger.info(f"{time.time}：文本{filename}上传成功")

        return jsonify(
            {
                "message": "成功上传文本",
                "status": "success",
                "file_path": "upload/file/" + filename,
            }
        )


# 处理文件
@app.route("/api/process", methods=["POST"])
# @login_required
def process_file():
    file_path = request.form["file_path"]
    if file_path == " " or file_path is None:
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

    def file_process(file_path):
        conpress_type = ["zip", "rar", "7z"]
        try:
            if any(file_path.split(".")[-1] == i for i in conpress_type):
                text_return = mutiplyTextProcess(file_path)  # 处理压缩多文件
            else:
                text_return = textProcess(file_path)  # 处理普通文件
            if text_return is not None:
                logger.info(f"{time.time()}：文件{file_path}处理成功")
                return jsonify(
                    {"message": "处理成功", "status": "success", "text": text_return}
                )
        except Exception as e:
            response = jsonify(
                {"message": "处理失败", "status": "error", "error": "process error"}
            )
            response.status_code = 400
            return response

    def run_with_timeout(func, args, timeout=60):
        result = None
        thread = threading.Thread(target=func, args=args)
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            ctypes.pythonapi.PyThreadState_SetAsyncExc(
                ctypes.c_long(thread.ident), ctypes.py_object(SystemExit)
            )
            response = jsonify(
                {"message": "处理超时", "status": "error", "error": "process timeout"}
            )
            response.status_code = 400
            return response
        else:
            try:
                result = thread.join()
            except RuntimeError:
                response = jsonify(
                    {"message": "处理失败", "status": "error", "error": "process error"}
                )
                response.status_code = 400
                return response
        return result

    timeout = 1 * 60  # 1分钟

    response = run_with_timeout(file_process, (file_path,), timeout)
    return response


if __name__ == "__main__":
    app.run(debug=True)
