from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from modelProcess import modelProcess
import os
import pickle
import faiss


def textProcess(self, file_path):
    # 导入文本
    loader = UnstructuredFileLoader(file_path)
    # 将文本转成 Document 对象
    document = loader.load()
    if document is None:
        print("文档为空")
        return None
    print(f"documents:{len(document)}")

    # 初始化代码分割器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    # 切分文本
    split_documents = text_splitter.split_documents(document)
    print(f"documents:{len(split_documents)}")

    # 创建嵌入
    file_name = file_path.split("/")[-1]
    file_name = file_name.split(".")[0]
    if os.path.exists(f"{file_name}.pkl"):
        with open(f"{file_name}.pkl", "rb") as f:
            VectorStore = pickle.load(f)
    else:
        embeddings = OpenAIEmbeddings()
        VectorStore = faiss.from_texts(split_documents, embedding=embeddings)
        with open(f"{file_name}.pkl", "wb") as f:
            pickle.dump(VectorStore, f)

        # 传递大模型
        result = modelProcess(file_name)
        return result
