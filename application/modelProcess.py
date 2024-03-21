from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.llm_chains import LLMChain, SimpleSequentialChain


def modelProcess(file_name):
    # location 链
    llm = OpenAI(temperature=1)
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
    template = """Given a meal, give a short and simple recipe on how to make that dish at home.
    % MEAL
    {bug_fix}

    YOUR RESPONSE:
    """
    prompt_template = PromptTemplate(input_variables=["bug_fix"], template=template)
    meal_chain = LLMChain(llm=llm, prompt=prompt_template)

    # 通过 SimpleSequentialChain 串联起来
    overall_chain = SimpleSequentialChain(
        chains=[location_chain, meal_chain], verbose=True
    )
    review = overall_chain.run("Rome")
