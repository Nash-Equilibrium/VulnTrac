import openai
from transformers import AutoModelForCausalLM, AutoTokenizer
import json


CODEQWEN_MODEL_PATH = "/opt/project/qwen1.5"
OPENAI_API_KEY = ""
openai.api_key = OPENAI_API_KEY

USER_CODE = ""



tokenizer = AutoTokenizer.from_pretrained(CODEQWEN_MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(CODEQWEN_MODEL_PATH)

# 使用CodeQwen生成报告的函数
def generate_report_with_codeqwen(user_code, temperature):
    inputs = tokenizer(user_code, return_tensors="pt")
    outputs = model.generate(inputs["input_ids"], max_length=1024, temperature=temperature)
    report = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return report

# 使用GPT-4选择更准确的报告
def choose_better_report(user_code, report1, report2):
    prompt_template = """
    The following code has been analyzed twice by CodeQwen. Please choose the more accurate report:
    
    User's code:
    {user_code}

    Report 1:
    {report1}

    Report 2:
    {report2}

    Respond with the number of the better report (1 or 2). You should only provide one number either 1 or 2.
    """
    prompt = prompt_template.format(user_code=user_code, report1=report1, report2=report2)
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in code analysis."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    response_text = response.choices[0].text.strip()
    return response_text

# 构建偏好数据集的函数
def build_preference_dataset(user_code, chosen_report, rejected_report):
    dataset_entry = {
        "query": user_code,
        "chosen": chosen_report,
        "rejected": rejected_report
    }
    return dataset_entry


def save_preference_data_to_json(preference_data, file_path):
    with open(file_path, 'w') as f:
        json.dump(preference_data, f, indent=4)


def main(user_code):
    # 生成两份报告
    report1 = generate_report_with_codeqwen(user_code, temperature=1)
    report2 = generate_report_with_codeqwen(user_code, temperature=1)

    # 让GPT-4选择更准确的一份报告
    choice_response = choose_better_report(user_code, report1, report2)
    chosen_report_number = int(choice_response.split()[0])
    
    if chosen_report_number == 1:
        chosen_report = report1
        rejected_report = report2
    else:
        chosen_report = report2
        rejected_report = report1

    # 构建偏好数据集
    preference_data = build_preference_dataset(user_code, chosen_report, rejected_report)
    
    return preference_data


if __name__ == "__main__":
    user_code = USER_CODE
    preference_data = main(user_code)
    
    # 保存偏好数据集为JSON文件
    save_preference_data_to_json(preference_data, 'preference_data.json')
    print(f"偏好数据集已保存到 preference_data.json")
