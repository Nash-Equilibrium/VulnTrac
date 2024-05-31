from tree_sitter import Parser, Language
import re
import os

class ASTSplitter:
    def __init__(self, node_number=2, overlap=1, chunk_size=400):
        self.node_number = node_number
        self.overlap = overlap
        self.chunk_size = chunk_size
        
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
                ]
            )

    def create_documents(self, text, language):
        supported_languages = ["python", "javascript", "java", "c", "cpp", "go"]
        if language not in supported_languages:
            raise ValueError(f"Unsupported language: {language}")

        parser = Parser()
        LANGUAGE = Language(self.language_library_path, language)
        parser.set_language(LANGUAGE)
        tree = parser.parse(bytes(text, "utf-8"))

        chunks = []
        current_chunk = []
        counter = 0

        def collect_chunks(node):
            nonlocal counter
            if node.type in ["function_definition", "class_definition"]:
                start_byte = node.start_byte
                end_byte = node.end_byte
                chunk = text[start_byte:end_byte]
                current_chunk.append(chunk)
                counter += 1

                # If the number of nodes in the current chunk reaches the limit, split the chunk
                if counter >= self.node_number:
                    if self.overlap == 0:
                        chunks.append("".join(current_chunk))
                        current_chunk.clear()
                        counter = 0
                    else:
                        overlap_chunk = current_chunk[-self.overlap:]
                        chunks.append("".join(current_chunk))
                        current_chunk[:] = overlap_chunk
                        counter = len(overlap_chunk)

            # Recursively collect chunks from child nodes
            for child in node.children:
                collect_chunks(child)

        # Start collecting chunks from the root node
        collect_chunks(tree.root_node)

        # Handle the last remaining chunk
        if current_chunk:
            chunks.append("".join(current_chunk))

        # Remove leading and trailing whitespace from chunks
        chunks = [re.sub(r"^\n+", "", chunk) for chunk in chunks]
        chunks = [re.sub(r"\n+$", "", chunk) for chunk in chunks]

        return chunks