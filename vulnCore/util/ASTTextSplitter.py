from tree_sitter import Parser, Language
import re
import os

class ASTTextSplitter:
    def __init__(
        self,
        node_number: int = 2,  # 每个代码块的节点数
        overlap: int = 1,  # 重叠节点数
        chunk_size: int = 400,  # 每个代码块的最大长度
    ):
        self.chunk_size = chunk_size
        self.node_number = node_number
        self.overlap = overlap

        # 检查语言库文件是否存在，不存在则创建
        self.language_library_path = "build/my-languages.so"
        if not os.path.exists(self.language_library_path):
            Language.build_library(
                self.language_library_path,
                [
                    "vendor/tree-sitter-python",
                    "vendor/tree-sitter-javascript",
                    "vendor/tree-sitter-java",
                    "vendor/tree-sitter-c",
                    "vendor/tree-sitter-cpp",
                    "vendor/tree-sitter-go",
                ],
            )

    def create_documents(self, text: str, language: str) -> list:
        """
        将给定文本按函数和类定义进行切分,返回每个函数代码块
        """
        accept_languages = [
            "python",
            "javascript",
            "java",
            "c",
            "cpp",
            "go",
        ]
        if language not in accept_languages:
            raise ValueError(f"Unsupported language: {language}")

        parser = Parser()
        LANGUAGE = Language(self.language_library_path, language)
        parser.set_language(LANGUAGE)
        tree = parser.parse(bytes(text, "utf-8"))

        def get_node_range(node):
            return node.start_byte, node.end_byte

        chunks = []
        current_chunk = []
        counter = 0

        nodes = list(tree.root_node.children)  # 获取根节点的所有子节点

        # 遍历所有节点
        for node in nodes:
            if node.type in ["function_definition", "class_definition"]:
                start_byte, end_byte = get_node_range(node)
                chunk = text[start_byte:end_byte]
                current_chunk.append(chunk)
                counter += 1

                # 每隔 n 个函数或类定义进行一次切割
                if counter >= self.node_number:
                    if self.overlap == 0:
                        chunks.append("".join(current_chunk))
                        current_chunk = []
                        counter = 0
                    else:
                        overlap_chunk = current_chunk[-self.overlap:]
                        chunks.append("".join(current_chunk))
                        current_chunk = overlap_chunk
                        counter = 0

        # 处理最后一个块
        if current_chunk:
            chunks.append("".join(current_chunk))

        # 利用正则表达式去除空白行
        chunks = [re.sub(r"^\n+", "", chunk) for chunk in chunks]
        chunks = [re.sub(r"\n+$", "", chunk) for chunk in chunks]

        return chunks
