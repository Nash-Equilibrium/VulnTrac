import os
import pdfkit
import markdown
import time
import sys

sys.path.append(r"C:\Users\ray\Desktop\ciscn\ciscn")
from VulnTrac.VulnTracInterface.modelConnect import modelProcess


def getReport(filename: str, documents: list) -> str:
    # 模型处理
    file_path = modelProcess(documents, filename)
    # 读取结果文件
    with open(file_path, "r", encoding="utf-8") as f:
        result_content = f.read()
    # 将 Markdown 转换为 HTML
    html = markdown.markdown(result_content)

    # 设置 PDF 选项
    options = {
        "page-size": "Letter",
        "margin-top": "0.75in",
        "margin-right": "0.75in",
        "margin-bottom": "0.75in",
        "margin-left": "0.75in",
        "encoding": "UTF-8",
    }

    # pdfkit支撑应用
    path_wkhtmltopdf = r"C:\Users\ray\Desktop\ciscn\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    # 将 HTML 转换为 PDF 文件
    # 存放地址可以修改，之后部署的话需要放在服务器上
    pdf_dir = r"C:\Users\ray\Desktop\ciscn\ciscn\reports\normal"
    timestamp = time.time()
    pdf_name = filename + "_" + timestamp + ".pdf"
    pdf_file_path = os.path.join(pdf_dir, pdf_name)
    pdfkit.from_string(html, pdf_file_path, options=options, configuration=config)
