from . import codeSplitter
import voyageai
from pyunpack import Archive
from dotenv import load_dotenv
import faiss
import os
import pickle

load_dotenv()


def multiFileProcess(file_path: str) -> list:
    """
    处理多文件文本
    """
    if file_path is None:
        print("文件路径为空")
        return

    # 解压文件
    file_name = os.path.splitext(file_path)[0]
    Archive(file_path).extractall("upload/" + file_name)
    file_list = os.listdir("upload/" + file_name)

    # 初始化代码分割器
    text_splitter = codeSplitter.astSplitter(2)

    # 切分文本
    split_documents = []

    type_dict = {
        "py": "python",
        "js": "javascript",
        "java": "java",
        "c": "c",
        "cpp": "cpp",
        "go": "go",
    }
    # 维护过滤列表
    filtered_extensions = ["py", "js", "java", "c", "cpp", "go"]

    # 文件过滤
    filtered_file_list = [
        file for file in file_list if file.split(".")[-1] in filtered_extensions
    ]

    for file in filtered_file_list:
        file_type = file.split(".")[-1]
        language = type_dict[file_type]
        with open(f"upload/{file_name}/{file}", "r") as f:
            text = f.read()
        split_documents.extend(text_splitter.createCodeChunk(text, language))

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
    for i, doc in enumerate(split_documents):
        query = VectorStore[:, i]  # 取出第i个文档的向量作为查询向量
        _, indices = index.search(query, 3)  # 搜索最相似的3个向量

        # 将最相似的三个文档组合
        top_indices = [indices[0][j] for j in range(len(indices[0]))]
        combined_doc = " ".join([split_documents[idx] for idx in top_indices])

        combined_docs.append(combined_doc)
