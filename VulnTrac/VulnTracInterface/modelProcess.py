import os
import json

from flask import Flask, send_file
from flask import request, render_template
from transformers import AutoModelForCausalLM, AutoTokenizer
from abc import ABC
from langchain.llms.base import LLM
from typing import Any, List, Mapping, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.prompts.prompt import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SimpleSequentialChain

# 保存文件路径
FILE_PATH = "C:/Users/ray/Desktop/ciscn/ciscn/reports/normal"
# 设置使用的设备
device = "cuda"
# 设置使用的GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "2"
# 加载模型
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen1.5-7B-Chat", torch_dtype="auto", device_map="auto"
)
# 加载分词器
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen1.5-7B-Chat")

app = Flask(__name__)


class Qwen(LLM, ABC):
    max_token: int = 10000
    temperature: float = 0.01
    top_p = 0.9
    history_len: int = 3

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
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
        text = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        model_inputs = tokenizer([text], return_tensors="pt").to(device)
        generated_ids = model.generate(model_inputs.input_ids, max_new_tokens=512)
        generated_ids = [
            output_ids[len(input_ids) :]
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {
            "max_token": self.max_token,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "history_len": self.history_len,
        }


@app.route("/", methods=["POST", "GET"])
def root():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])

def chat():
    # 获取数据
    data_seq = request.get_data()
    data_dict = json.loads(data_seq)
    split_documents = data_dict["split_documents"]

    # 初始化模型
    llm = Qwen()

    # location 链
    LOCATE_TEMPLATE = """ You're a professional code bug fix engineer.
      You've been asked to fix a bug in a piece of code.
      You need to find out the location of the bug in the code and just return the code.
      And you need to tell me what is the kind of bug in the code.
    % USER LOCATION
    {bug_location}
    
    YOUR RESPONSE:  
    """

    # 构造prompt
    location_prompt_template = PromptTemplate(
        input_variables=["bug_location"], template=LOCATE_TEMPLATE
    )
    location_chain = LLMChain(llm=llm, prompt=location_prompt_template)

    # fix 链
    FIX_TEMPLATE = """Based on the location of the bug in the code
                  and the kind of bug in the code you found.
                  you need to fix the bug in the code.
                  just return the code after fix.
    % BUG FIX
    {bug_fix}

    YOUR RESPONSE:
    """
    fix_prompt_template = PromptTemplate(
        input_variables=["bug_fix"], template=FIX_TEMPLATE
    )
    fix_chain = LLMChain(llm=llm, prompt=fix_prompt_template)

    # 通过 SimpleSequentialChain 串联起来
    overall_chain = SimpleSequentialChain(
        chains=[location_chain, fix_chain], verbose=True
    )
    # 保存location链和fix链处理后结果
    results = []

    for split_document in split_documents:
        result = overall_chain.run(split_document)
        results.append(result)

    # summarize 链
    SUMMARIZE_TEMPLATE = """summarize the bug you found in the code.
    % BUG SUMMARIZE
    {bug_summarize}

    YOUR RESPONSE:
    """
    summarize_prompt_template = PromptTemplate(
        input_variables=["bug_summarize"], template=SUMMARIZE_TEMPLATE
    )
    summarize_chain = LLMChain(llm=llm, prompt=summarize_prompt_template)
    summarize_result = summarize_chain.run("\n".join(str(result) for result in results))
    """
    汇总结果处理，生成报告，逻辑需要完善
    """

    return send_file(FILE_PATH, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
