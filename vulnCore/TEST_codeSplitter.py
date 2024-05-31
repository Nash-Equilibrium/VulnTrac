from util.codeSplitter import ASTSplitter

splitter = ASTSplitter()
code = """
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

result = []

language = "python"
documents = splitter.create_documents(code, language)
for doc in documents:
    result.append(doc)

for item in result:
    print("----------------------\n")
    print(f"chunk :\n {item}")