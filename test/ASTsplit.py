from tree_sitter import Language, Parser

Language.build_library(
    # Store the library in the `build` directory
    "build/my-languages.so",
    # Include one or more languages
    [
        "vendor/tree-sitter-python",
    ],
)

# 加载 Python 语言的解析器
PY_LANGUAGE = Language("build/my-languages.so", "python")


def get_code_chunks(code):
    """
    将给定代码按函数进行切分,返回每个函数代码块的起止字节偏移量列表
    """
    parser = Parser()
    parser.set_language(PY_LANGUAGE)
    tree = parser.parse(bytes(code, "utf-8"))

    chunks = []

    nodes = list(tree.root_node.children)
    print(nodes)

    for node in nodes:
        if node.type == "class_definition":
            end_byte = node.end_byte
            chunks.append(end_byte)
        if node.type == "function_definition":
            end_byte = node.end_byte
            chunks.append(end_byte)

    return chunks


def extract_code_chunks(code, offsets):
    """
    根据给定的字节偏移量列表,从代码中提取对应的代码块
    """
    chunks = []
    start = 0
    for offset in offsets:
        chunk = code[start:offset]
        chunks.append(chunk)
        start = offset
    chunks.append(code[start:])
    return chunks


# 示例用法
code = """
class MyClass:
    def __init__(self):
        self.data = []

    def add_data(self, x):
        self.data.append(x)

    def get_data(self):
        return self.data

def func1():
    print("Hello World")

def func2(x):
    return x * 2

print(func2(3))
"""

offsets = get_code_chunks(code)
print("Code chunk offsets:", offsets)

chunks = extract_code_chunks(code, offsets)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i}:\n{chunk}\n")
