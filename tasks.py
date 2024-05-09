from celery import Celery
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from datetime import datetime
from git import Repo as GitRepo
import hashlib
import requests
from app import app, db
from models import Repo

from util.mutiplyTextProcess import mutiplyTextProcess
import os


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)


@celery.task
def repoMonitor(repo_url, user_email, username):

    def download_repo_zip(repo_url, save_path):
        # 将GitHub仓库URL转换为zip文件URL
        zip_url = (
            repo_url + "/archive/refs/heads/main.zip"
        )  # 如果默认分支不是main，请修改这里

        # 发送GET请求
        response = requests.get(zip_url)

        # 确保请求成功
        response.raise_for_status()

        # 写入文件
        with open(save_path, "wb") as f:
            f.write(response.content)

    # 下载最新的压缩包
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    latest_archive_path = (
        f"C:\\Users\\ray\\Desktop\\ciscn\\ciscn\\repo\\repofile\\{timestamp}.zip"
    )
    download_repo_zip(repo_url, save_path)

    # 计算最新压缩包的哈希值
    with open(latest_archive_path, "rb") as f:
        latest_archive_hash = hashlib.sha256(f.read()).hexdigest()

    with app.app_context():
        repo = Repo.query.get(repo_url)
        if not repo:
            return
    # 如果压缩包有变化,则进行漏洞检测
    if repo.last_archive_hash != latest_archive_hash:
        pass
        # 执行漏洞检测逻辑，生成报告
        # ...

    # 更新数据库中的压缩包信息
    repo.last_archive_hash = latest_archive_hash
    repo.last_checked_at = datetime.now()
    db.session.commit()

    os.remove(latest_archive_path)

    # 调用 sendMail 任务发送报告
    sendMail.delay(user_email, username, report_path)


@celery.task
def sendMail(email: str, username: str, attachment_path: str) -> bool:
    """
    发送检测报告给用户
    """
    SENDER = "439824791@qq.com"  # 发件人邮箱账号
    PASS = "rvxqnakagumybjde"  # 发件人邮箱授权码

    try:
        # 创建一个带附件的实例
        msg = MIMEMultipart()
        msg["From"] = formataddr(["From VulTrac", SENDER])
        msg["To"] = formataddr(["For you", username])
        msg["Subject"] = "检测报告"

        # 邮件正文
        text = f"""
        尊敬的用户{username}:

            您好!我们已完成对您提交的代码的漏洞检测。详细报告请查看附件:
                
            如有任何疑问,欢迎随时与我们联系。

        祝好!

        VulTrac 团队
        """
        msg.attach(MIMEText(text, "plain", "utf-8"))

        # 添加附件
        attachment = MIMEBase("application", "octet-stream")
        with open(attachment_path, "rb") as f:
            attachment.set_payload(f.read())
        encoders.encode_base64(attachment)
        attachment.add_header(
            "Content-Disposition",
            "attachment",
            filename=os.path.basename(attachment_path),
        )
        msg.attach(attachment)

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(SENDER, PASS)
        server.sendmail(SENDER, [email], msg.as_string())
        server.quit()

        print("邮件发送成功")
        return True
    except Exception as e:
        print("邮件发送失败")
        print(e)
        return False
