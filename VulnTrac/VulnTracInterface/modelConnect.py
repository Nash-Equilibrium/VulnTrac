import requests
import json
import os

# 服务器地址
FLASK_URL = "http://<flask_server_ip>:<flask_server_port>"
# 文件保存路径
SAVE_PATH = r"C:\Users\ray\Desktop\ciscn\ciscn\reports\Markdown"


def modelProcess(split_documents: list, filename: str, degree: int) -> str:
    # 转换数据为 JSON 格式
    json_data = json.dumps({"split_documents": split_documents})

    # 发送数据
    try:
        response = requests.post(FLASK_URL + "api/chat", data=json_data)
    except requests.exceptions.RequestException as e:
        print("Failed to send data.")
        return

    if response.status_code == 200:
        # 构造保存文件的完整路径
        file_path = os.path.join(SAVE_PATH, filename + ".md")
        with open(file_path, "wb") as f:
            f.write(response.content)
        print("File downloaded successfully")
    else:
        print("Error downloading file")

    return file_path
