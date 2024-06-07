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

'''
PROMPT_TEMPLATE = """
### Context ###
{context_str}

### Instruction ###
You are a coding security expert. Based on the context provided above, review the provided code for any potential vulnerabilities. Follow these steps precisely and use the examples provided to guide your analysis:

1. **Identify Vulnerabilities**: Determine if there are any vulnerabilities in the given code. Provide the common names of each identified vulnerability.
2. **Locate Vulnerabilities**: Locate every vulnerable part in the code and provide the relevant code snippets. Highlight the specific lines or parts where the vulnerability exists with comments.
3. **Explain Hazards**: Explain the potential hazards caused by each vulnerability in detail.
4. **Provide Fixes**: Offer step-by-step advice to fix each vulnerability, modifying only the vulnerable parts. Ensure the fixes are clear and specific.
5. **Additional Recommendations**: Include any additional information or recommendations that may help the developer improve the overall security of the code.

If the information provided is insufficient to review the code for vulnerabilities, respond with 'The code cannot be reviewed with the given information' or 'Not enough relevant information has been provided.' Avoid adding any information that is not present in the context.

### Examples ###

**Example 1:**

#### User's Code ####
```python
query = "SELECT * FROM users WHERE username = '" + user_input + "';"  # User input is not sanitized
```

#### Response ####

1. **Identify Vulnerabilities**:
   - SQL Injection

2. **Locate Vulnerabilities**:
   ```python
   query = "SELECT * FROM users WHERE username = '" + user_input + "';"  # User input is not sanitized
   ```

3. **Explain Hazards**:
   - **SQL Injection**: This vulnerability allows attackers to execute arbitrary SQL code, potentially accessing, modifying, or deleting database contents. It can lead to data breaches and unauthorized data manipulation.

4. **Provide Fixes**:
   ```python
   # Fix for SQL Injection
   # Use parameterized queries or prepared statements
   query = "SELECT * FROM users WHERE username = %s;"
   cursor.execute(query, (user_input,))
   ```

5. **Additional Recommendations**:
   - Always validate and sanitize user inputs to prevent injection attacks.
   - Utilize well-established security libraries for handling common tasks like authentication and encryption.
   - Conduct regular security audits and code reviews to catch vulnerabilities early.

**Example 2:**

#### User's Code ####
```python
password = input("Enter your password: ")
hashed_password = hashlib.md5(password.encode()).hexdigest()  # Using weak hashing algorithm
```

#### Response ####

1. **Identify Vulnerabilities**:
   - Weak Hashing Algorithm

2. **Locate Vulnerabilities**:
   ```python
   hashed_password = hashlib.md5(password.encode()).hexdigest()  # Using weak hashing algorithm
   ```

3. **Explain Hazards**:
   - **Weak Hashing Algorithm**: MD5 is a weak hashing algorithm that is vulnerable to collision attacks, making it easier for attackers to crack passwords and compromise the system.

4. **Provide Fixes**:
   ```python
   # Fix for Weak Hashing Algorithm
   # Use a stronger hashing algorithm such as SHA-256 or bcrypt
   hashed_password = hashlib.sha256(password.encode()).hexdigest()
   ```

5. **Additional Recommendations**:
   - Consider using bcrypt for password hashing as it provides additional security through salting and a higher computational cost for hashing.

### User's Code ###
{code}

### Response ###
"""
'''