from celery import Celery
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
import os


def sendMail(email: str, username: str, repo_name: str, attachment_path: str) -> bool:
    """
    发送检测报告给用户
    """
    SENDER = "439824791@qq.com"  # 发件人邮箱账号
    PASS = "yqecvlbzfxjebhbh"  # 发件人邮箱授权码

    try:
        # 创建一个带附件的实例
        msg = MIMEMultipart()
        msg["From"] = formataddr(["From VulTrac", SENDER])
        msg["To"] = formataddr(["For you", username])
        msg["Subject"] = "检测报告"

        # 邮件正文
        text = f"""
        尊敬的用户{username}:

            您好!我们已完成对您仓库{repo_name}的漏洞检测。详细报告请查看附件:
                
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
