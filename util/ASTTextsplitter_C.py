from tree_sitter import Parser, Language


class ASTTextSplitter_C:
    def __init__(
        self,
        language: str,  # 语言
        node_number: int,  # 每个代码块的节点数
        chunk_size: int = 400,  # 每个代码块的最大长度
    ):
        self.language = language
        self.chunk_size = chunk_size
        self.node_number = node_number
        Language.build_library(
            # Store the library in the `build` directory
            "build/my-languages.so",
            # Include one or more languages
            [
                "vendor/tree-sitter-c",
                "vendor/tree-sitter-cpp",
            ],
        )

    def create_documents(self, text: str) -> list:
        """
        将给定文本按函数和类定义进行切分,返回每个函数代码块
        """

        parser = Parser()
        LANGUAGE = Language("build/my-languages.so", self.language)
        parser.set_language(LANGUAGE)
        tree = parser.parse(bytes(text, "utf-8"))

        offsets = []

        nodes = list(tree.root_node.children)  # 获取根节点的所有子节点
        cnt = self.node_number

        for node in nodes:
            if node.type == "class_definition" and cnt == self.node_number:  # 类定义
                end_byte = node.end_byte
                offsets.append(end_byte)
            if (
                node.type == "function_definition" and cnt == self.node_number
            ):  # 函数定义
                end_byte = node.end_byte
                offsets.append(end_byte)
            if cnt == 1:
                cnt = self.node_number
            cnt -= 1

        chunks = []
        start = 0
        for offset in offsets:  # 按offset切分代码块
            chunk = text[start:offset]
            chunks.append(chunk)
            start = offset
        chunks.append(text[start:])

        return chunks
