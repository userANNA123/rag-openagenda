import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.rag_service import RAGService


app = FastAPI(
    title="API RAG OpenAgenda",
    description="API REST permettant d'interroger un chatbot RAG basé sur FAISS et Mistral.",
    version="1.0.0"
)

rag_service = RAGService()


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "API RAG OpenAgenda opérationnelle",
        "docs": "/docs"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):
    """
    Pose une question au système RAG et retourne une réponse augmentée.
    """
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
    """
    Reconstruit la base vectorielle FAISS à partir des données nettoyées.
    """
    try:
        subprocess.run(
            ["python", "src/build_faiss_index.py"],
            check=True
        )

        global rag_service
        rag_service = RAGService()

        return {
            "message": "Base vectorielle reconstruite avec succès."
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur pendant la reconstruction : {str(e)}"
        )
    