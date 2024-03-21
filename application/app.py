from flask import Flask, request, jsonify, render_template
from application.textProcess import textProcess
from werkzeug.utils import secure_filename
import os
import hashlib


app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World"


@app.route("/api/upload_file", methods=["POST"])
def upload_file():
    if "file" in request.files and request.files["file"] != "":
        file = request.files["file"]
        # 文件大小检查
        if file.content_length > 1024 * 1024 * 5:
            return jsonify({"message": "文件大小超过5MB", "status": "error"})
        # 文件类型检查
        filename = secure_filename(file.filename)
        receive_file_type = [
            ".txt",
            ".pdf",
            "c",
            ".cpp",
            ".java",
            ".py",
            ".js",
            ".php",
            ".sh",
        ]
        for i in receive_file_type:
            if filename.endswith(i):
                return jsonify({"message": "文件类型错误", "status": "error"})
        # 保存文件
        hash = hashlib.md5(file.read().encode("utf-8")).hexdigest()  # 加密区分不同文件
        filename = filename.split(".")[0] + "_" + hash + "." + filename.split(".")[1]
        file.save("upload/file/" + filename)

        return jsonify(
            {
                "message": "成功上传文件",
                "status": "success",
                "file_path": "upload/file/" + filename,
            }
        )
    else:  # 上传文件为空
        return jsonify({"message": "未上传文件", "status": "error"})


@app.route("/api/upload_text", methods=["POST"])
def upload_text():
    data = request.get_json()
    if "text" not in data or data["text"] == "":
        return jsonify({"message": "未上传文本", "status": "error"})
    else:
        hash = hashlib.md5(data["text"].encode("utf-8")).hexdigest()
        filename = "text_" + hash + ".txt"
        with open("upload/text/" + filename, "w") as f:
            f.write(data["text"])
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
    text_return = textProcess(file_path)
    if text_return is None:
        return jsonify({"message": "处理失败", "status": "error"})
    else:
        return jsonify(
            {"message": "处理成功", "status": "success", "text": text_return}
        )


if __name__ == "__main__":
    app.run(debug=True)
