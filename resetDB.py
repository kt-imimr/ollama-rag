import ollama
import chromadb

'''
    client.reset() # Empties and completely resets the database. ⚠️ This is destructive and not reversible.
'''

client = chromadb.PersistentClient(path="/home/user/code/Projects/ollama-RAG/db")

# in order to empty the db, .env is an option to do it.
client.reset()