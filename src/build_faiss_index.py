import json
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# 1. Charger les données nettoyées
with open("data/cleaned_events.json", "r", encoding="utf-8") as f:
    events = json.load(f)

# 2. Transformer les textes en Documents LangChain
documents = [
    Document(
        page_content=event,
        metadata={"source": "OpenAgenda"}
    )
    for event in events
]

# 3. Découper les textes en chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

print(f"Nombre de chunks créés : {len(chunks)}")

# 4. Créer le modèle d'embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 5. Créer l'index FAISS
vectorstore = FAISS.from_documents(chunks, embeddings)

# 6. Sauvegarder l'index
vectorstore.save_local("faiss_index")

print("Index FAISS créé et sauvegardé ✅")