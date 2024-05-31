import requests
from bs4 import BeautifulSoup
import csv
import time

# 函数：获取CWE页面内容
def fetch_cwe_page(url):
    response = requests.get(url)
    response.raise_for_status()  # 如果请求失败，则引发HTTPError异常
    return response.text

# 函数：解析CWE页面并提取脆弱性名称和定义
def parse_cwe_page(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    vulnerabilities = []

    # 提取CWE名称（通常在h2标签中）
    cwe_name = soup.find('h2').get_text(strip=True) if soup.find('h2') else '未找到名称'
    
    # 提取CWE定义（通常在class为'indent'的div标签中）
    description_tag = soup.find('div', class_='indent')
    description = description_tag.get_text(strip=True) if description_tag else '未找到定义'
    
    # 提取扩展描述（假设在class为'extended'的div标签中）
    extended_description_tag = soup.find('div', class_='extended')
    extended_description = extended_description_tag.get_text(strip=True) if extended_description_tag else ''
    
    # 拼接描述和扩展描述
    full_description = f"{description} {extended_description}".strip()

    vulnerabilities.append((cwe_name, full_description))

    return vulnerabilities

# 函数：将脆弱性信息保存到CSV文件
def save_to_csv(vulnerabilities, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['名称', '定义'])
        writer.writerows(vulnerabilities)

# 主函数：运行爬虫
def cwe_main():
    base_url = 'https://cwe.mitre.org/data/definitions/'  # 基础URL
    vulnerabilities = []
    start_id = 1  # 起始CWE ID
    end_id = 10  # 假设有1200个CWE定义，根据实际情况调整

    for cwe_id in range(start_id, end_id + 1):
        url = f'{base_url}{cwe_id}.html'
        try:
            html_content = fetch_cwe_page(url)  # 获取页面内容
            vulnerabilities.extend(parse_cwe_page(html_content))  # 解析并提取数据
            print("************************")
            print(f'成功获取 {url} 的数据')
            print(parse_cwe_page(html_content))
            time.sleep(0.1)  # 添加延迟，避免对服务器造成负担
        except requests.HTTPError as e:
            print(f'获取 {url} 失败: {e}')
        except Exception as e:
            print(f'发生错误: {e}')

    save_to_csv(vulnerabilities, 'cwe_vulnerabilities.csv')
    print(f"已保存 {len(vulnerabilities)} 条脆弱性信息到 'cwe_vulnerabilities.csv'")

if __name__ == '__main__':
    cwe_main()
    
