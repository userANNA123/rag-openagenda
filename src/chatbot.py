from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate


load_dotenv(dotenv_path=r"C:\Users\anna\Documents\rag-openagenda\.env")

api_key = os.getenv("MISTRAL_API_KEY", "").strip()

if not api_key:
    raise ValueError("La clé MISTRAL_API_KEY n'a pas été trouvée dans le fichier .env")

print("API key loaded:", True)


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)


llm = ChatMistralAI(
    model="mistral-small-latest",
    mistral_api_key=api_key,
    temperature=0.2
)


prompt = ChatPromptTemplate.from_template("""
Je as un chatbot intelligent spécialisé dans les événements culturels.

mon rôle est de recommander des événements personnalisés à l'utilisateur
à partir des événements présents dans le contexte fourni.

Règles importantes :
- Réponds uniquement à partir du contexte.
- Ne crée jamais d'événement qui n'existe pas dans le contexte.
- Si l'information n'est pas disponible, dis :
  "Je ne sais pas d'après les données disponibles."
- Si plusieurs événements correspondent, propose 2 ou 3 recommandations.
- Réponds de manière claire, naturelle et utile.

Pour chaque événement recommandé, indique si disponible :
- le nom de l'événement ;
- la date ;
- le lieu ;
- la ville ;
- une courte raison de recommandation.

Contexte :
{context}

Question utilisateur :
{question}

Réponse :
""")


def ask_chatbot(question: str) -> str:
    docs = retriever.invoke(question)

    if not docs:
        return "Je ne sais pas d'après les données disponibles."

    context = "\n\n".join([doc.page_content for doc in docs])

    chain = prompt | llm

    response = chain.invoke({
        "context": context,
        "question": question
    })

    return response.content


if __name__ == "__main__":
    print("\nChatbot prêt.")
    print("Tape 'exit' pour quitter.\n")

    while True:
        question = input("Pose ta question : ")

        if question.lower() in ["exit", "quit", "q"]:
            print("Fin du chatbot.")
            break

        try:
            answer = ask_chatbot(question)
            print("\nRéponse :")
            print(answer)
            print("-" * 80)

        except Exception as e:
            print("\nErreur pendant l'appel au chatbot :")
            print(e)
            print("-" * 80)