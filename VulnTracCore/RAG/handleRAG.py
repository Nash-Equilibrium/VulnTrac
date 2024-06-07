import numpy as np
import os
import re
import torch
import argparse
from transformers import AutoModelForCausalLM, AutoTokenizer
from abc import ABC
from typing import Any, List, Mapping, Optional, Tuple, Dict
from langchain_community.vectorstores import FAISS
from langchain.llms.base import LLM
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain_community.document_loaders import TextLoader, CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import RetrievalQA

device = "cuda" if torch.cuda.is_available() else "cpu"

model = AutoModelForCausalLM.from_pretrained(
    "/opt/project/qwen1.5",
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("/opt/project/qwen1.5")

class Qwen(LLM, ABC):
    max_token: int = 10000
    temperature: float = 0.01
    top_p = 0.9
    history_len: int = 4

    def __init__(self):
        super().__init__()

    @property
    def _llm_type(self) -> str:
        return "Qwen"

    @property
    def _history_len(self) -> int:
        return self.history_len

    def set_history_len(self, history_len: int = 10) -> None:
        self.history_len = history_len

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        messages = [
            {"role": "system", "content": """
                You are a coding security expert. Your task is to review the provided code for any potential vulnerabilities. Follow these steps precisely:

                1. **Identify Vulnerabilities**: Determine if there are any vulnerabilities in the given code. Provide the common names of each identified vulnerability.
                2. **Locate Vulnerabilities**: Locate every vulnerable part in the code and provide the relevant code snippets. Highlight the specific lines or parts where the vulnerability exists with comments.
                3. **Explain Hazards**: Explain the potential hazards caused by each vulnerability in detail.
                4. **Provide Fixes**: Offer step-by-step advice to fix each vulnerability, modifying only the vulnerable parts. Ensure the fixes are clear and specific.
                5. **Additional Recommendations**: Include any additional information or recommendations that may help the developer improve the overall security of the code.

                Format your report strictly as follows:

                ---

                # VulnTrac Code Review Report

                ## 1. Identify Vulnerabilities
                [List all identified vulnerabilities here, using their common names. For example: SQL Injection, Cross-Site Scripting (XSS), etc.]

                ## 2. Locate Vulnerabilities
                [Provide code snippets for each vulnerability, highlighting the specific lines or parts where the vulnerability exists with comments.]

                **Example:**
                ```python
                # Vulnerability: SQL Injection
                query = "SELECT * FROM users WHERE username = '" + user_input + "';" # User input is not sanitized
                ```

                ## 3. Explain Hazards
                [Explain the potential hazards caused by each vulnerability in detail. Discuss what attackers can do if the vulnerability is exploited.]

                **Example:**
                - **SQL Injection**: This vulnerability allows attackers to execute arbitrary SQL code, potentially accessing, modifying, or deleting database contents. It can lead to data breaches and unauthorized data manipulation.

                ## 4. Provide Fixes
                [Offer step-by-step advice to fix each vulnerability, modifying only the vulnerable parts. Ensure the fixes are clear and specific.]

                **Example:**
                ```python
                # Fix for SQL Injection
                # Use parameterized queries or prepared statements
                query = "SELECT * FROM users WHERE username = %s;"
                cursor.execute(query, (user_input,))
                ```

                ## 5. Additional Recommendations
                [Include any additional information or recommendations that may help the developer improve the overall security of the code. This could include best practices, libraries, or tools to use.]

                **Example:**
                - **Input Validation**: Always validate and sanitize user inputs to prevent injection attacks.
                - **Use Security Libraries**: Utilize well-established security libraries for handling common tasks like authentication and encryption.
                - **Regular Security Audits**: Conduct regular security audits and code reviews to catch vulnerabilities early.
                
                ---
                
                End of Report.
            """},
            {"role": "user", "content": prompt}
        ]

        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        model_inputs = tokenizer([text], return_tensors="pt").to(device)
        generated_ids = model.generate(
            model_inputs.input_ids,
            max_new_tokens=2048
        )

        response_ids = generated_ids[:, len(model_inputs.input_ids[0]):]  # 改进切片
        response = tokenizer.batch_decode(response_ids, skip_special_tokens=True)[0]
        return response

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"max_token": self.max_token,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "history_len": self.history_len}

def load_file(filepath: str) -> List[Document]:
    loader = CSVLoader(file_path=FILE_PATH, encoding='utf8')
    textsplitter = CharacterTextSplitter()
    docs = loader.load_and_split(textsplitter)
    return docs

if __name__ == '__main__':
    
    FILE_PATH = 'cwe_vulnerabilities_all.csv'
    EMBEDDING_MODEL = 'text2vec'
    PROMPT_TEMPLATE = """
    ### Context ###
    {context_str}

    ### Instruction ###
    You are a coding security expert. Based on the context provided above, review the provided code for any potential vulnerabilities. Follow these steps precisely and use the examples provided to guide your analysis:

    1. **Identify Vulnerabilities**: Determine if there are any vulnerabilities in the given code. Provide the common names of each identified vulnerability. Provide the most relevant CWE number(If there is no relevant CWE number, ignore this rule).
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
    {question}

    ### Response ###
    """

    EMBEDDING_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    VECTOR_SEARCH_TOP_K = 5
    CHAIN_TYPE = 'stuff'
    
    embedding_model_dict = {
        "text2vec": "all-MiniLM-L6-v2",
    }

    query = """
    #include <stdio.h>
    #include <string.h>

    void func(char *input) {
        char buffer[64];
        strcpy(buffer, input);
        printf("Buffer content: %s\n", buffer);
    }

    int main(int argc, char *argv[]) {
        if (argc != 2) {
            printf("Usage: %s <input>\n", argv[0]);
            return 1;
        }

        func(argv[1]);
        return 0;
    }
    """

    embeddings = HuggingFaceEmbeddings(
        model_name=embedding_model_dict[EMBEDDING_MODEL],
        model_kwargs={'device': EMBEDDING_DEVICE}
    )

    docs = load_file(FILE_PATH)
    docsearch = FAISS.from_documents(docs, embeddings)

    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE, input_variables=["context_str", "question"]
    )

    chain_type_kwargs = {"prompt": prompt, "document_variable_name": "context_str"}

    # 使用 RetrievalQA 来生成答案
    qa = RetrievalQA.from_chain_type(
        llm=Qwen(),
        chain_type=CHAIN_TYPE,
        retriever=docsearch.as_retriever(search_kwargs={"k": VECTOR_SEARCH_TOP_K}),
        chain_type_kwargs=chain_type_kwargs
    )

    # 获取回答
    response = qa.run(query)
    print("Response:", response)
