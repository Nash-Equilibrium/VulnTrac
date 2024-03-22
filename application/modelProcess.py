from langchain.llms.fake import FakeListLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain


def modelProcess(split_documents):
    responses = ["Test"]
    llm = FakeListLLM(responses=responses)

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
                  just return the code.
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
    return result


modelProcess("Test")
# results = []
# for document in split_documents:
#     overall_chain.process(document)
#     results.append(overall_chain.get_result())
# return results
