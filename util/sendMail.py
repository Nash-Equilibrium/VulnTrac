import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def mailsend(my_sender, my_pass, my_user, text):
    ret = True
    try:
        msg = MIMEText("验证码为：" + text, "plain", "utf-8")
        msg["From"] = formataddr(
            ["From ray", my_sender]
        )  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg["To"] = formataddr(
            ["For you", my_user]
        )  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg["Subject"] = "验证码"

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(
            my_sender,
            [
                my_user,
            ],
            msg.as_string(),
        )  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()

    except Exception:
        ret = False
    return ret
