import ollama
import chromadb

# Step 1: Generate embeddings

import docx2txt

document_path = "/home/user/Downloads/Leave_Application_Form_KT.docx"
document_content = docx2txt.process(document_path)

# documents = document_content.split("\t\n")
documents = [document_content]
# documents = [
#   "llamas are Li King To's pets.",
# ]

client = chromadb.PersistentClient(path="/home/user/code/Projects/ollama-RAG/db")

try:
    client.heartbeat()
except chromadb.errors.ChromaDBError:
    print("could not connect to chromaDB at /home/user/code/Projects/ollama-RAG/db")

collection = client.get_collection(name="docs")
if collection is None:
    collection = client.create_collection(name="docs")

# store each document in a vector embedding database
for i, d in enumerate(documents):
  response = ollama.embeddings(model="mxbai-embed-large", prompt=d)
  embedding = response["embedding"]
  collection.upsert(
    ids=[str(i)],
    embeddings=[embedding],
    documents=[d]
  )






# Step 2: Retrieve
  # an example prompt
prompt = "How many leave days did I take in this form?"

# generate an embedding for the prompt and retrieve the most relevant doc
response = ollama.embeddings(
  prompt=prompt,
  model="mxbai-embed-large"
)
results = collection.query(
  query_embeddings=[response["embedding"]],
  n_results=1
)

print("🐍 File: ollama-RAG/main.py | Line: 42 | undefined ~ results",results)

data = results['documents'][0][0]


# Step 3
# generate a response combining the prompt and data we retrieved in step 2
output = ollama.generate(
  model="phi3",
  prompt=f"Using this data: {data}. Respond to this prompt within 5 sentences: {prompt}"
)

print(output['response'])