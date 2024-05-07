from . import ASTTextSplitter


def textProcess(file_path: str) -> list:
    """
    处理单文件文本
    """
    if file_path is None:
        print("文件路径为空")
        return

    # 初始化代码分割器
    text_splitter = ASTTextSplitter.ASTTextSplitter(2)

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
    file_type = file_path.split(".")[-1]
    language = type_dict[file_type]
    with open(file_path, "r") as f:
        text = f.read()
    split_documents.extend(text_splitter.create_documents(text, language))

    return split_documents
