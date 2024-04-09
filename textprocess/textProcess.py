from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms.fake import FakeListLLM


def textProcess(file_path: str) -> list:  # 处理文本
    """
    处理单一文本
    """
    if file_path is None:
        print("文件路径为空")
        return
    with open(file_path, "r") as f:
        text = f.read()

    if text is None:
        print("文档为空")

    # 初始化代码分割器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=100,
        min_chunk_length=25,
        length_function=len,
    )

    # 切分文本
    split_documents = text_splitter.create_documents(text)

    # # 传递大模型
    # results = modelProcess(split_documents: list)

    #    大模型处理
    results = []
    responses = ["Test"]
    llm = FakeListLLM(responses=responses)
    for document in split_documents:
        results.append(llm(document.page_content))


if __name__ == "__main__":
    textProcess("application/1.txt")
