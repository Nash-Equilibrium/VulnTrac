from tree_sitter import Parser, Language
import re


class ASTTextSplitter:
    def __init__(self, node_number: int = 2, overlap: int = 1, chunk_size: int = 400):
        self.chunk_size = chunk_size
        self.node_number = node_number
        self.overlap = overlap
        Language.build_library(
            "build/my-languages.so",
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
        accept_languages = ["python", "javascript", "java", "c", "cpp", "go"]
        if not any(language == lang for lang in accept_languages):
            raise ValueError(f"Unsupported language: {language}")

        parser = Parser()
        LANGUAGE = Language("build/my-languages.so", language)
        parser.set_language(LANGUAGE)
        tree = parser.parse(bytes(text, "utf-8"))

        nodes = list(tree.root_node.children)
        chunks = []
        current_chunk = []
        counter = 0
        node_num = 0
        final_end_byte = 0

        # 获取节点的起始和结束字节
        def get_node_range(node):
            start_byte = node.start_byte
            end_byte = node.end_byte
            return start_byte, end_byte

        # 根据counter分割代码块
        def split_node(counter):
            if counter >= self.node_number:
                if self.overlap == 0:
                    chunks.append("".join(current_chunk))
                    current_chunk.clear()
                else:
                    overlap_chunk = current_chunk[-self.overlap :]
                    chunks.append("".join(current_chunk))
                    current_chunk = overlap_chunk
                return 0
            return counter

        # 处理文件开头的代码
        if nodes:
            start_byte, _ = get_node_range(nodes[0])
            current_chunk.append(text[:start_byte])

        for node in nodes:
            if node.type in ["function_definition", "class_definition"]:
                start_byte, end_byte = get_node_range(node)
                parent_chunk = text[start_byte:end_byte]

                # 处理嵌套定义
                nested_nodes = list(node.children)
                for nested_node in nested_nodes:
                    if nested_node.type in ["function_definition", "class_definition"]:
                        nested_start, nested_end = get_node_range(nested_node)
                        nested_chunk = text[nested_start:nested_end]
                        current_chunk.append(nested_chunk)
                        counter += 1
                        counter = split_node(counter)

                        # 从父节点中删除嵌套节点
                        parent_chunk = parent_chunk.replace(nested_chunk, "")

                if parent_chunk:
                    current_chunk.append(parent_chunk)
                    counter += 1
                    counter = split_node(counter)

                if node_num == len(nodes) - 1:
                    final_end_byte = end_byte
                node_num += 1

        # 处理文件结尾的代码
        chunks.append("".join(current_chunk) + text[final_end_byte:])

        chunks = [re.sub(r"^\n+", "", chunk) for chunk in chunks]
        chunks = [re.sub(r"\n+$", "", chunk) for chunk in chunks]

        return chunks
