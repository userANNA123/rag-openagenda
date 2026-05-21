import os
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate


class RAGService:
    def __init__(self):
        load_dotenv(dotenv_path=r"C:\Users\anna\Documents\rag-openagenda\.env")

        self.api_key = os.getenv("MISTRAL_API_KEY", "").strip()

        if not self.api_key:
            raise ValueError("La clé MISTRAL_API_KEY est introuvable.")

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vectorstore = FAISS.load_local(
            "faiss_index",
            self.embeddings,
            allow_dangerous_deserialization=True
        )

        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 5}
        )

        self.llm = ChatMistralAI(
            model="mistral-small-latest",
            mistral_api_key=self.api_key,
            temperature=0.2
        )

        self.prompt = ChatPromptTemplate.from_template("""
Tu es un chatbot intelligent spécialisé dans les événements culturels.

Réponds uniquement à partir du contexte fourni.
Ne crée jamais d'événement qui n'existe pas dans le contexte.

Si l'information n'est pas disponible, réponds :
"Je ne sais pas d'après les données disponibles."

Contexte :
{context}

Question utilisateur :
{question}

Réponse :
""")

    def ask(self, question: str) -> str:
        if not question or not question.strip():
            return "La question ne peut pas être vide."

        docs = self.retriever.invoke(question)

        if not docs:
            return "Je ne sais pas d'après les données disponibles."

        context = "\n\n".join([doc.page_content for doc in docs])

        chain = self.prompt | self.llm

        response = chain.invoke({
            "context": context,
            "question": question
        })

        return response.content