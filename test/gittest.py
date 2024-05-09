import requests
import os


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


# 使用示例
repo_url = "https://github.com/Nash-Equilibrium/ciscn"
save_path = "C:\\Users\\ray\\Desktop\\ciscn\\ciscn\\repo\\repofile\\repo.zip"
download_repo_zip(repo_url, save_path)
