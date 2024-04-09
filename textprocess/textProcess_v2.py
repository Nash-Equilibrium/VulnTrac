from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms.fake import FakeListLLM
from langchain.docstore.document import Document


def textProcess(file_path: str) -> list:  # 处理文本
    with open("application/1.txt", "r") as f:
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


if __name__ == "__main__":
    textProcess("application/1.txt")
