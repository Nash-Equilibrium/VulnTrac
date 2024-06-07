import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import torch


csv_file = 'cwe_vulnerabilities_all.csv'
data = pd.read_csv(csv_file)

def process_row(row):
    return {
        'CWE Number': row['CWE Number'],
        'Definition': row['Definition'],
        'Common sequences': row['Common sequences'],
        'Demonstrative examples': row['Demonstrative examples'],
        'Possible mitigations': row['Possible mitigations']
    }

documents = [process_row(row) for _, row in data.iterrows()]

def concatenate_fields(doc):
    return f"CWE Number: {doc['CWE Number']} Definition: {doc['Definition']} Common sequences: {doc['Common sequences']} Demonstrative examples: {doc['Demonstrative examples']} Possible mitigations: {doc['Possible mitigations']}"

concatenated_docs = [concatenate_fields(doc) for doc in documents]


model_name = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(model_name, device='cuda' if torch.cuda.is_available() else 'cpu')

embeddings = model.encode(concatenated_docs, convert_to_tensor=True, show_progress_bar=True, device='cuda' if torch.cuda.is_available() else 'cpu')
embeddings = embeddings.cpu().numpy()
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

vector_store_name = 'cwe_FAISS.faiss'

faiss.write_index(index, vector_store_name)

with open('cwe_FAISS.pkl', 'wb') as f:
    pickle.dump(documents, f)

print(f"{csv_file}已保存至{vector_store_name}中。")

