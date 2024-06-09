from datetime import datetime
from flask import request, jsonify
from VulnTracLibrary.textProcess import textProcess
from VulnTracLibrary.multiFileProcess import multiFileProcess
from VulnTracLibrary.sendMail import mailsend
from VulnTracLibrary.getReport import getReport
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin
from init import db, app
from loguru import logger
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
import threading
import ctypes
import time
import os
import atexit
import random
import re

DETAILED = 0
SIMPLE = 1

# 日志配置
logger.add("app.log", rotation="50MB", retention="10 days", level="INFO", colorize=True)


from dbTables import User, File, Repo, Analysis, AnalysisHistory, RepoHistory, get_user

# 定时执行监测任务
from celery.schedules import crontab
from tasks import celery, repoMonitor
import hashlib

app.secret_key = "123"
# celery配置
celery.conf.update(
    broker_url=app.config["CELERY_BROKER_URL"],
    result_backend=app.config["CELERY_RESULT_BACKEND"],
)

# cors配置
CORS(app, supports_credentials=True)

# 数据库初始化
with app.app_context():
    db.create_all()

    login_manager = LoginManager()
    login_manager.init_app(app)


with app.app_context():
    app.config.update(
        CELERYBEAT_SCHEDULE={
            "repo_monitor": {
                "task": "tasks.repoMonitor",
                "schedule": crontab(minute=0, hour="*/24"),  # 每 24 小时执行一次
                "args": (Repo.query.with_entities(Repo.id).all(),),  # 传递所有仓库 ID
            },
        }
    )


@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)


# 注册
@app.route("/v1/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # 合法性检查放在前端
        data = request.get_json()
        username = data.get("username", "")
        password = data.get("password", "")
        password = generate_password_hash(password)
        email = data.get("email", "")
        # 检查邮箱是否已经注册
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify(
                {
                    "ret": {
                        "message": "Email already registered",
                        "code": "400",
                    }
                }
            )
        role = "0"
        new_user = User(username=username, password=password, email=email, role=role)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(
            {
                "ret": {
                    "message": "Register successful",
                    "code": "200",
                }
            }
        )
    return jsonify(
        {
            "ret": {
                "message": "Method not allowed",
                "code": "405",
            }
        }
    )


# 登录
@app.route("/v1/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username", "")
        password = data.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return jsonify(
                {
                    "ret": {
                        "message": "Login successful",
                        "code": "200",
                    },
                }
            )
        else:
            return jsonify(
                {
                    "ret": {
                        "message": "Username or password is incorrect",
                        "code": "400",
                    }
                }
            )
    return jsonify(
        {
            "ret": {
                "message": "Method not allowed",
                "code": "405",
            }
        }
    )


# 登出
@app.route("/v1/logout")
# @login_required
def logout():
    logout_user()
    return jsonify(
        {
            "ret": {
                "message": "Logout successful",
                "code": "200",
            }
        }
    )


# 发送邮件
@app.post("/v1/send_register_sms")
def send_register_sms():
    # 1. 解析前端传递过来的数据
    data = request.get_json()
    email = data.get("email", "")
    # 2. 校验邮箱
    pattern = r"^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$"  # 邮箱校验，防止前端绕过
    ret = re.match(pattern, email)
    if not ret:
        return jsonify(
            {
                "ret": {
                    "message": "邮箱格式不正确",
                    "code": "400",
                }
            }
        )

    # 3.1 生成随机验证码
    my_sender = "439824791@qq.com"  # 发件人邮箱账号
    my_pass = "rdvyavudgjuhbigg"  # 发件人邮箱授权码
    my_user = email  # 收件人邮箱账号
    mailcode = random.choices("123456789", k=6)  # 生成随机验证码
    text = "".join(mailcode)  # 将验证码转换为字符串
    ret = mailsend(my_sender, my_pass, my_user, text)  # 发送邮件

    if ret:
        return jsonify(
            {
                "ret": {
                    "message": "发送邮箱验证码成功",
                    "code": "200",
                },
                "data": {"mailcode": text},
            }
        )
    else:
        return jsonify(
            {
                "ret": {
                    "message": "发送邮箱验证码失败",
                    "code": "400",
                }
            }
        )


# 上传文件
@app.route("/v1/upload_file", methods=["POST"])
# @login_required
def upload_file():
    if "file" in request.files and request.files["file"] != "":
        file = request.files["file"]
        # 文件大小检查
        if file.content_length > 1024 * 1024 * 5:
            return jsonify(
                {
                    "ret": {
                        "message": "文件大小超过5MB",
                        "code": "400",
                    }
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
                    "ret": {
                        "message": "文件类型不支持",
                        "code": "400",
                    }
                }
            )
            response.status_code = 400
            return response
        # 保存文件
        data = request.get_json()
        codename = data.get("codeName", "")
        timestamp = str(time.time())  # 时间戳区分文件
        _, ext = os.path.splitext(filename)
        filename = codename + "_" + timestamp + ext
        user_id = current_user.get_id()
        file_db = File(file_name=filename, file_type=ext.lstrip("."), user_id=user_id)
        with app.app_context():
            db.session.add(file_db)
            db.session.commit()
        # 保存文件名及类型到数据库
        file.save("upload/file/" + filename)
        logger.info(f"{time.time()}：文件{filename}上传成功")

        # 保存文件
        return jsonify(
            {
                "ret": {
                    "message": "文件上传成功",
                    "code": "200",
                },
                "data": {"file_path": "upload/file/" + filename, "file_name": filename},
            }
        )
    else:  # 上传文件为空
        response = jsonify(
            {
                "ret": {
                    "message": "文件为空",
                    "code": "400",
                }
            }
        )
        response.status_code = 400
        return response


# 上传文本
@app.route("/v1/upload_text", methods=["POST"])
# @login_required
def upload_text():
    # 处理文本
    data = request.get_json()
    text = data.get("codeText", "")
    type = data.get("codeType", "")
    name = data.get("codeName", "")
    granularity = data.get("granularity", 1)

    if text == "":
        response = jsonify(
            {
                "ret": {
                    "message": "文本为空",
                    "code": "400",
                }
            }
        )
        response.status_code = 400
        return response
    else:
        timestamp = str(time.time())
        type_dict = {
            "python": ".py",
            "javascript": ".js",
            "java": ".java",
            "c": ".c",
            "cpp": ".cpp",
            "go": ".go",
        }
        # 保存文件名及类型到数据库
        filename = name + "_" + timestamp + type_dict[type]
        user_id = current_user.get_id()
        file_db = File(
            file_name=filename, file_type=type_dict[type].lstrip(), user_id=user_id
        )
        with app.app_context():
            db.session.add(file_db)
            db.session.commit()

        with open("upload/file/" + filename, "w") as f:
            f.write(text)
        logger.info(f"{time.time}：文本{filename}上传成功")

        return jsonify(
            {
                "ret": {
                    "message": "文本上传成功",
                    "code": "200",
                },
                "data": {
                    "file_path": "upload/file/" + filename,
                    "file_name": filename,
                    "granularity": granularity,
                },
            }
        )


# 处理文件
@app.route("/v1/process", methods=["POST"])
# @login_required
def process_file():
    data = request.get_json().get("filepath", {}).get("data", "")
    file_path = data.get("file_path", "")
    granularity = data.get("granularity", "beginner")
    filename = data.get("file_name", "")
    if not file_path:
        return (
            jsonify(
                {
                    "ret": {
                        "message": "文件路径为空",
                        "code": 400,
                    }
                }
            ),
            400,
        )

    compress_types = ["zip", "rar", "7z"]
    if any(filename.endswith(ext) for ext in compress_types):
        text_return = multiFileProcess(file_path)  # 处理压缩多文件
        pdf_path = getReport(filename, text_return, granularity)
    else:
        text_return = textProcess(file_path)  # 处理普通文件
        pdf_path = getReport(filename, text_return, granularity)

    if pdf_path is not None:
        logger.info(f"{time.time()}：文件{file_path}处理成功")
        response = {
            "ret": {
                "message": "处理成功",
                "code": 200,
            },
            "data": pdf_path,
        }
        # 写入数据库
        user_id = current_user.get_id()
        file_id = File.query.filter_by(file_name=filename).first().id
        analysis_db = Analysis(
            file_id=file_id,
            status="completed",
            pdf_path=pdf_path,
        )
        History_db = AnalysisHistory(
            user_id=user_id,
            file_id=file_id,
            analysis_id=analysis_db.id,
        )
        with app.app_context():
            db.session.add(analysis_db)
            db.session.add(History_db)
            db.session.commit()
        return jsonify(response), 200
    else:
        return (
            jsonify(
                {
                    "ret": {
                        "message": "处理失败",
                        "code": 400,
                    }
                }
            ),
            400,
        )


# 仓库监测
@app.route("/v1/repo_monitor", methods=["POST"])
# @login_required
def repo_monitor():
    data = request.get_json()
    repo_url = data.get("repo_url", "")
    repo_name = data.get("repo_name", "")
    if repo_url == " " or repo_url is None:
        response = jsonify({"ret": {"message": "仓库地址为空", "code": "400"}})
        response.status_code = 400
        return response
    if repo_name == " " or repo_name is None:
        response = jsonify({"ret": {"message": "仓库名为空", "code": "400"}})
        response.status_code = 400
        return response
    # 写入数据库
    # 随机生成一个hash值
    hash_value = hashlib.sha256(str(random.randint(0, 999999)).encode()).hexdigest()
    user_id = current_user.get_id()
    repo_db = Repo(
        repo_name=repo_name,
        repo_url=repo_url,
        user_id=user_id,
        last_archive_hash=hash_value,
        last_checked_at=datetime.now(),
    )
    with app.app_context():
        db.session.add(repo_db)
        db.session.commit()
    logger.info(f"{time.time()}：仓库{repo_url}加入监测成功")
    # 调用 repoMonitor 任务
    user = get_user(user_id)
    user_email, username = user.email, user.username
    repoMonitor.delay(repo_url, user_email, username)

    return jsonify({"ret": {"message:": "仓库监测成功", "code": "200"}})


# 获取历史记录
@app.route("/v1/getRepoHistory", methods=["GET"])
# @login_required
def get_repo_history():
    user_id = current_user.get_id()
    history = RepoHistory.query.filter_by(user_id=user_id).all()
    data = []
    for i in history:
        repoName = Repo.query.filter_by(id=i.file_id).first().repo_name
        repoUrl = Repo.query.filter_by(id=i.file_id).first().repo_url
        uploadTime = File.query.filter_by(id=i.file_id).first().created_at
        pdfUrl = Analysis.query.filter_by(id=i.analysis_id).first().pdf_path

        data.append(
            {
                "repoName": repoName,
                "repoUrl": repoUrl,
                "uploadTime": uploadTime,
                "pdfUrl": pdfUrl,
                "status": "completed",
            }
        )
    return jsonify(
        {"ret": {"message": "获取历史记录成功", "code": "200"}, "data": data}
    )


# 获取分析历史记录
@app.route("/v1/getAnalysisHistory", methods=["GET"])
# @login_required
def get_analysis_history():
    user_id = current_user.get_id()
    history = AnalysisHistory.query.filter_by(user_id=user_id).all()
    data = []
    for i in history:
        fileName = File.query.filter_by(id=i.file_id).first().file_name
        uploadTime = File.query.filter_by(id=i.file_id).first().created_at
        pdfUrl = Analysis.query.filter_by(id=i.analysis_id).first().pdf_path
        username = User.query.filter_by(id=user_id).first().username
        data.append(
            {
                "projectName": fileName,
                "uploadTime": uploadTime,
                "pdfUrl": pdfUrl,
                "username": username,
                "status": "completed",
            }
        )
    return jsonify(
        {"ret": {"message": "获取历史记录成功", "code": "200"}, "data": data}
    )


# 添加钩子函数,在应用退出时关闭 Celery
def shutdown_celery_worker():
    celery.control.broadcast("shutdown", destination=["celery@worker"])


atexit.register(shutdown_celery_worker)


if __name__ == "__main__":
    app.run(debug=True, port=5800)
