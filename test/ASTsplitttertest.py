import sys

sys.path.append("..")

from textprocess.ASTTextSplitter import ASTTextSplitter

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

splitter = ASTTextSplitter("python", 2)
documents = splitter.create_documents(python_code)
for document in documents:
    print(document + "\n")
