import json
import os
import pdfkit
import requests
import markdown
import time


def analysisGet(filename: str, documents: list) -> str:
    payload = json.dumps({"documents": documents})

    # 设置请求头
    headers = {"Content-Type": "application/json"}

    # 发送 POST 请求
    url = "https://your-server.com/chat"
    response = requests.request("POST", url, headers=headers, data=payload)

    # 检查响应状态码
    if response.status_code == 200:
        # 获取响应内容并解析 JSON
        response_data = json.loads(response.text)
        results = response_data["results"]
    else:
        print(f"请求失败,状态码: {response.status_code}")

    # 打包报告
    result_content = "\n".join(results)
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
    path_wkhtmltopdf = r"C:\Users\ray\Desktop\ciscn\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    # 将 HTML 转换为 PDF 文件
    pdf_dir = r"C:\Users\ray\Desktop\ciscn\ciscn\reports\normal"
    timestamp = time.time()
    pdf_name = filename + "_" + timestamp + ".pdf"
    pdf_file_path = os.path.join(pdf_dir, pdf_name)
    pdfkit.from_string(html, pdf_file_path, options=options, configuration=config)
