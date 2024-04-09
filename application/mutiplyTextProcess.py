from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import voyageai
from langchain_community.document_loaders import TextLoader
from pyunpack import Archive
import faiss
import os
import pickle

os.environ["VOYAGE_API_KEY"] = "pa-holqOWcNg6Q2JNeVbgh0xCHRw6Wm1xyalGSL7hH1-2Y"


def mutiplyTextProcess(file_path: str) -> list:
    """
    处理多文件文本
    """
    if file_path is None:
        print("文件路径为空")
        return

    # 解压文件
    file_name = file_path.split("/")[-1]
    Archive(file_path).extractall("upload/" + file_name)
    file_list = os.listdir("upload/" + file_name)
    # 读取文件
    texts = []
    for file in file_list:
        text = TextLoader("upload/" + file_name + "/" + file).load()
        texts.append(text[0])

    # 初始化代码分割器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=100,
        min_chunk_length=25,
        length_function=len,
    )

    # 切分文本
    split_documents = []
    for t in texts:
        split_documents.extend(text_splitter(t))

    # 嵌入embedding层
    if os.path.exists(f"embedding/{file_name}.pkl"):
        with open(f"embedding/{file_name}.pkl", "rb") as f:
            VectorStore = pickle.load(f)
    else:

        vo = voyageai.Client()
        result = vo.embed(split_documents, model="voyage-code-2", input_type="document")
        VectorStore = result.embeddings
        with open(f"embedding/{file_name}.pkl", "wb") as f:
            pickle.dump(VectorStore, f)

    # 构建向量索引
    index = faiss.IndexFlatL2(VectorStore.shape[0])
    index.add(VectorStore.T)

    # 为每个拆分文档找到最相似的三个文档并进行重组
    combined_docs = []
    for i, doc in enumerate(texts):
        query = VectorStore[:, i]  # 取出第i个文档的向量作为查询向量
        _, indices = index.search(query, 3)  # 搜索最相似的3个向量

        # 将最相似的三个文档组合
        top_indices = [indices[0][j] for j in range(len(indices[0]))]
        combined_doc = " ".join([texts[idx] for idx in top_indices])

        combined_docs.append(combined_doc)
