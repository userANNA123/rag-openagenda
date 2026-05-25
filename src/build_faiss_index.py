import json
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

DATA_DIR = Path("data")
INDEX_DIR = Path("faiss_index")


def build_faiss_index():
    cleaned_path = DATA_DIR / "cleaned_events.json"

    with open(cleaned_path, "r", encoding="utf-8") as f:
        events = json.load(f)

    events = [event for event in events if event and event.strip()]

    if not events:
        raise ValueError(
            "Aucun événement nettoyé trouvé. Vérifie data/events.json et clean_data.py."
        )

    documents = [
        Document(
            page_content=event,
            metadata={"source": "OpenAgenda"}
        )
        for event in events
    ]

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(str(INDEX_DIR))

    return len(documents)


if __name__ == "__main__":
    count = build_faiss_index()
    print(f"Nombre de documents indexés : {count}")
    print("Index FAISS créé et sauvegardé ✅")