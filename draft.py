from util.codeSplitter import astSplitter


myast = astSplitter(node_number=1, overlap=0, chunk_size=400)

python_code = """
def hello_world():
    print("Hello, World!")

class MyClass:
    def __init__(self):
        self.value = 42

    def my_method(self):
        return self.value
"""
result = myast.create_documents(python_code, "python")
print(result)
