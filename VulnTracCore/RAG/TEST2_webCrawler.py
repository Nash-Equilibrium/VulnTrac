import requests
from bs4 import BeautifulSoup
import csv
import time

# 函数：获取CWE页面内容
def fetch_cwe_page(url):
    response = requests.get(url)
    response.raise_for_status()  # 如果请求失败，则引发HTTPError异常
    return response.text

# 函数：解析CWE页面并提取脆弱性名称、定义、常见后果和示范例子
def parse_cwe_page(html_content, cwe_id):
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

    # 提取常见后果
    consequences = []
    consequences_section = soup.find('div', id='Common_Consequences')
    if consequences_section:
        rows = consequences_section.find_all('tr')[1:]  # 跳过表头
        for row in rows:
            columns = row.find_all('td')
            if len(columns) == 3:
                scope = columns[0].get_text(strip=True)
                impact = columns[1].get_text(strip=True)
                likelihood = columns[2].get_text(strip=True)
                consequences.append({'Scope': scope, 'Impact': impact, 'Likelihood': likelihood})

    # 提取示范例子
    examples = []
    example_soup_path = '#oc_'+str(cwe_id)+'_Demonstrative_Examples > div > div'
    examples_path = soup.select(example_soup_path)
    for example in examples_path:
        example_text = example.get_text(strip=True)
        examples.append(example_text)

    # 提取可能的解决方法
    mitigations = []
    mitigation_soup_path = '#oc_'+str(cwe_id)+'_Potential_Mitigations > div > div > div'
    mitigations_path = soup.select(mitigation_soup_path)
    for mitigation in mitigations_path:
        mitigation_text = mitigation.get_text(strip=True)
        mitigations.append(mitigation_text)

    vulnerabilities.append((cwe_name, full_description, consequences, examples, mitigations))

    return vulnerabilities

# 函数：将脆弱性信息保存到CSV文件
def save_to_csv(vulnerabilities, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['名称', '定义', '常见后果', '示范例子', '可能的缓解方案'])

        for vuln in vulnerabilities:
            cwe_name, full_description, consequences, examples, mitigations = vuln
            consequences_str = "; ".join([f"Scope: {c['Scope']}, Impact: {c['Impact']}, Likelihood: {c['Likelihood']}" for c in consequences]) if consequences else '无常见后果信息'
            examples_str = "; ".join(examples) if examples else '无示范例子'
            mitigations_str = "; ".join(mitigations) if mitigations else '无可能的缓解方案'
            writer.writerow([cwe_name, full_description, consequences_str, examples_str, mitigations_str])

# 主函数：运行爬虫
def main():
    base_url = 'https://cwe.mitre.org/data/definitions/'  # 基础URL
    vulnerabilities = []
    start_id = 12  # 起始CWE ID
    end_id = 12  # 假设有一部分CWE定义，根据实际情况调整

    for cwe_id in range(start_id, end_id + 1):
        url = f'{base_url}{cwe_id}.html'
        try:
            html_content = fetch_cwe_page(url)  # 获取页面内容
            vulnerabilities.extend(parse_cwe_page(html_content, cwe_id))  # 解析并提取数据
            print(f'成功获取 {url} 的数据')
            time.sleep(1)  # 添加延迟，避免对服务器造成负担
        except requests.HTTPError as e:
            print(f'获取 {url} 失败: {e}')
        except Exception as e:
            print(f'发生错误: {e}')

    save_to_csv(vulnerabilities, 'cwe_vulnerabilities.csv')
    print(f"已保存 {len(vulnerabilities)} 条脆弱性信息到 'cwe_vulnerabilities.csv'")

if __name__ == '__main__':
    main()
