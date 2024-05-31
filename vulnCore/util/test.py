from ASTTextSplitter import ASTTextSplitter


myast = ASTTextSplitter(node_number=2, overlap=1, chunk_size=400)

python_code = """
def foo():
    pass

class Bar:
    def baz():
        pass

    def qux():
        pass

def corge():
    pass

class Grault:
    def garply():
        pass

    def waldo():
        def nested_func():
            pass
"""
result = myast.create_documents(python_code, "python")
print(result[2])
