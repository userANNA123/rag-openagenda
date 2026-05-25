import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.rag_service import RAGService


app = FastAPI(
    title="API RAG OpenAgenda",
    description="API REST pour interroger un système RAG basé sur FAISS, LangChain et Mistral.",
    version="1.0.0"
)

rag_service = RAGService()


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "API RAG OpenAgenda opérationnelle",
        "docs": "http://127.0.0.1:8000/docs"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="La question ne peut pas être vide."
        )

    try:
        answer = rag_service.ask(request.question)
        return {
            "question": request.question,
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur pendant la génération de réponse : {str(e)}"
        )


@app.post("/rebuild")
def rebuild_vectorstore():
    try:
        subprocess.run(["python", "src/data_loader.py"], check=True)
        subprocess.run(["python", "src/clean_data.py"], check=True)
        subprocess.run(["python", "src/build_faiss_index.py"], check=True)

        global rag_service
        rag_service = RAGService()

        return {
            "message": "Base vectorielle reconstruite avec succès.",
            "steps": [
                "Données récupérées depuis OpenAgenda",
                "Données nettoyées",
                "Embeddings générés",
                "Index FAISS reconstruit",
                "index.faiss et index.pkl sauvegardés"
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur pendant la reconstruction : {str(e)}"
        )