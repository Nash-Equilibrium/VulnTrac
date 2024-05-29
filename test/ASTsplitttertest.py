from util.codeSplitter import astSplitter

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

splitter = astSplitter("python", 2)
documents = splitter.createCodeChunk(python_code)
for document in documents:
    print(document + "\n")
