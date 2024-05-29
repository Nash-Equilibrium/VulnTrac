from tree_sitter import Parser, Language
import re


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
        Language.build_library(
            # Store the library in the `build` directory
            "build/my-languages.so",
            # Include one or more languages
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
        # 检查语言是否支持
        accept_languages = [
            "python",
            "javascript",
            "java",
            "c",
            "cpp",
            "go",
        ]  # 支持语言列表
        if not any(language == lang for lang in accept_languages):
            raise ValueError(f"Unsupported language: {language}")
        parser = Parser()
        LANGUAGE = Language("build/my-languages.so", language)
        parser.set_language(LANGUAGE)
        tree = parser.parse(bytes(text, "utf-8"))

        offsets = []

        nodes = list(tree.root_node.children)  # 获取根节点的所有子节点

        def get_node_range(node):
            start_byte = node.start_byte
            end_byte = node.end_byte
            return start_byte, end_byte

        chunks = []
        current_chunk = []
        counter = 0

        # 遍历所有节点
        for node in nodes:
            if node.type in ["function_definition", "class_definition"]:
                start_byte, end_byte = get_node_range(node)
                chunk = text[start_byte:end_byte]
                current_chunk.append(chunk)
                counter += 1

                # 处理嵌套定义
                nested_nodes = list(node.children)
                for nested_node in nested_nodes:
                    if nested_node.type in ["function_definition", "class_definition"]:
                        nested_start, nested_end = get_node_range(nested_node)
                        nested_chunk = text[nested_start:nested_end]
                        current_chunk.append(nested_chunk)
                        counter += 1

                # 每隔 n 个函数或类定义进行一次切割
                if counter >= self.node_number:
                    if self.overlap == 0:
                        chunks.append("".join(current_chunk))
                        current_chunk = []
                        counter = 0
                    else:
                        overlap_chunk = current_chunk[-self.overlap :]
                        chunks.append("".join(current_chunk))
                        current_chunk = overlap_chunk
                        counter = 0

        # 利用正则表达式去除空白行
        chunks = [re.sub(r"^\n+", "", chunk) for chunk in chunks]
        chunks = [re.sub(r"\n+$", "", chunk) for chunk in chunks]

        return chunks
