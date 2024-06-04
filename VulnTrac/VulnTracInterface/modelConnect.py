import requests
import json


def modelProcess(split_documents):

    # 服务器地址
    url = "http://<flask_server_ip>:<flask_server_port>"

    # 转换数据为 JSON 格式
    json_data = json.dumps({"split_documents": split_documents})

    # 发送数据
    try:
        response = requests.post(url + "api/chat", data=json_data)
    except requests.exceptions.RequestException as e:
        print("Failed to send data.")
        return

    # 判断是否发送成功
    if response.status_code == 200:
        print("Data sent successfully.")
    else:
        print("Failed to send data.")

    # 返回结果处理
    response_data = json.loads(response.text)
    results = response_data["results"]
    return results
