import os
import json

from flask import Flask
from flask import request, render_template
from transformers import AutoTokenizer, AutoModel

# system params
os.environ["CUDA_VISIBLE_DEVICES"] = "2"

tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
model = (
    AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()
)
model.eval()

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def root():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data_seq = request.get_data()
    data_dict = json.loads(data_seq)
    human_input = data_dict["human_input"]

    response, _ = model.chat(tokenizer, human_input, history=[])

    result_dict = {"response": response}
    result_seq = json.dumps(result_dict, ensure_ascii=False)
     # location 链

    template = """ You're a professional code bug fix engineer.
      You've been asked to fix a bug in a piece of code.
      You need to find out the location of the bug in the code and just return the code.
    % USER LOCATION
    {bug_location}
    
    YOUR RESPONSE:
    """

    prompt_template = PromptTemplate(
        input_variables=["bug_location"], template=template
    )
    location_chain = LLMChain(llm=llm, prompt=prompt_template)

    # fix 链
    template = """fix the bug in the code.
                  just return the code after fix.
    % BUG FIX
    {bug_fix}

    YOUR RESPONSE:
    """
    prompt_template = PromptTemplate(input_variables=["bug_fix"], template=template)
    fix_chain = LLMChain(llm=llm, prompt=prompt_template)

    # 通过 SimpleSequentialChain 串联起来
    overall_chain = SimpleSequentialChain(
        chains=[location_chain, fix_chain], verbose=True
    )

    result = overall_chain.process(split_documents)

    # summarize链

    return result


modelProcess("Test")
    return result_seq


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
