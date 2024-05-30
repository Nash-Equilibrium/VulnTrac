from tree_sitter import Parser, Language


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
        text_bytes = text.encode(encoding="utf-8")
        tree = parser.parse(text_bytes)

        nodes = (node for node in tree.root_node.children)
        chunks = []
        current_chunk = bytearray()
        counter = 0
        final_end_byte = 0

        def get_node_range(node):
            """
            获取节点的起始和结束字节位置
            """
            start_byte = node.start_byte
            end_byte = node.end_byte
            return start_byte, end_byte

        def split_node(counter):
            """
            根据counter切分节点
            """
            if counter >= self.node_number:
                if self.overlap == 0:
                    chunks.append(bytes(current_chunk))
                    current_chunk.clear()
                else:
                    overlap_chunk = current_chunk[-self.overlap :]
                    chunks.append(bytes(current_chunk))
                    current_chunk = bytearray(overlap_chunk)
                return 0
            return counter

        if nodes:
            start_byte, _ = get_node_range(next(nodes))
            current_chunk.extend(text_bytes[:start_byte])

        for node in nodes:
            if node.type in ["function_definition", "class_definition"]:
                start_byte, end_byte = get_node_range(node)
                parent_chunk = text_bytes[start_byte:end_byte].strip()

                nested_nodes = (nested_node for nested_node in node.children)
                for nested_node in nested_nodes:
                    if nested_node.type in ["function_definition", "class_definition"]:
                        nested_start, nested_end = get_node_range(nested_node)
                        nested_chunk = text_bytes[nested_start:nested_end]
                        current_chunk.extend(nested_chunk)
                        counter += 1
                        counter = split_node(counter)

                        parent_chunk = parent_chunk.replace(nested_chunk, b"")

                if parent_chunk:
                    current_chunk.extend(parent_chunk)
                    counter += 1
                    counter = split_node(counter)

                if node is list(tree.root_node.children)[-1]:
                    final_end_byte = end_byte

        chunks.append(bytes(current_chunk) + text_bytes[final_end_byte:])

        chunks = [chunk.decode() for chunk in chunks]
        return chunks
