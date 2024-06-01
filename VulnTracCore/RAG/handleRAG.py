import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM

# 读取CSV文件
df = pd.read_csv('cwe_vulnerabilities_all.csv')

# 合并各列数据形成一个完整的描述
df['combined'] = df.apply(lambda row: f"名称: {row['名称']}\n定义: {row['定义']}\n常见后果: {row['常见后果']}\n示范例子: {row['示范例子']}\n可能的缓解方案: {row['可能的缓解方案']}", axis=1)
texts = df['combined'].tolist()

# 加载预训练的句子嵌入模型
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# 向量化文本数据
embeddings = embed_model.encode(texts, convert_to_tensor=True)

# 创建Faiss索引
d = embeddings.shape[1]
index = faiss.IndexFlatL2(d)
embeddings_np = embeddings.cpu().detach().numpy().astype('float32')
index.add(embeddings_np)

# 用户的Prompt
user_prompt = "用户的输入内容"

# 向量化用户的Prompt
query_embedding = embed_model.encode(user_prompt, convert_to_tensor=True).cpu().detach().numpy().astype('float32').reshape(1, -1)

# 查询最相似的向量
D, I = index.search(query_embedding, k=5)
retrieved_texts = [texts[i] for i in I[0]]

# 将查询结果合并为一个字符串
retrieved_info = "\n".join(retrieved_texts)
combined_input = f"用户的Prompt: {user_prompt}\n\n相关信息:\n{retrieved_info}"

# 加载预训练的CodeQwen-1.5模型和tokenizer
tokenizer = AutoTokenizer.from_pretrained('Qwen/Qwen-1.5')
model = AutoModelForCausalLM.from_pretrained('Qwen/Qwen-1.5')

# 对结合后的输入进行编码
inputs = tokenizer.encode(combined_input, return_tensors='pt')

# 生成响应
outputs = model.generate(inputs, max_length=500)

# 解码生成的响应
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
