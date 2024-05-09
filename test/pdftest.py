import pdfkit
import markdown
import json
import os

result_content = "# 这是标题\n\n这是一些**粗体**内容"
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
pdf_dir = r"C:\Users\ray\Desktop\ciscn\ciscn\reports"
pdf_name = f"test.pdf"
pdf_file_path = os.path.join(pdf_dir, pdf_name)
pdfkit.from_string(html, pdf_file_path, options=options, configuration=config)
