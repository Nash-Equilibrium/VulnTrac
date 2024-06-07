import openai

INPUT_FILE_PATH = "/Users/young/Desktop/VulnTrac/VulnTrac/TEST_codeSplitter.py"
OUTPUT_FILE_PATH = "after.py"
OPENAI_API_KEY = ""


openai.api_key = OPENAI_API_KEY

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def get_annotated_code(code):
    prompt_template = """
    Please provide concise and precise comments for each line of source code to help the model better understand the source code. Please give the commented code directly\\n
    ```
    {code}
    ```
    Code after annotation:
    """
    prompt_user = prompt_template.format(code=code)
    prompt_sys = "You are an expert C/C++ programmer."

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo-0301", messages=[
                {"role": "system", "content":prompt_sys},
                {"role": "user", "content": prompt_user + code}], temperature=0,max_tokens=1024,top_p=1,frequency_penalty=0.0,presence_penalty=0.0,stop=["\n\n"]
    )

    annotated_code = response.choices[0].text.strip()
    return annotated_code

def annotate_code_file(input_path, output_path):
    code = read_file(input_path)
    annotated_code = get_annotated_code(code)
    write_file(output_path, annotated_code)

if __name__ == "__main__":
    input_file_path = INPUT_FILE_PATH  # 替换为你的代码文件路径
    output_file_path = OUTPUT_FILE_PATH  # 替换为你希望保存带注释代码的文件路径

    annotate_code_file(input_file_path, output_file_path)
    print(f"带注释的代码已保存到 {output_file_path}")
