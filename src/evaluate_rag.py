import os
from dotenv import load_dotenv
from datasets import Dataset

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)

from langchain_mistralai import ChatMistralAI
from langchain_huggingface import HuggingFaceEmbeddings

from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

from rag_service import RAGService


load_dotenv()


def build_evaluation_dataset():
    rag = RAGService()

    questions = [
        "Quel est le scope temporel des événements ?",
        "Combien d'événements sont disponibles ?",
        "Quels sont les événements disponibles à Paris ?",
        "Quels événements ont lieu en mai 2026 ?",
        "Quels sont les lieux des événements disponibles ?",
    ]

    ground_truths = [
        "Les événements couvrent une période entre janvier 2026 et mai 2026 selon les données indexées.",
        "Le système doit indiquer le nombre d'événements disponibles dans le contexte ou dans l'index.",
        "La réponse doit lister les événements pertinents disponibles à Paris à partir du contexte.",
        "La réponse doit retourner les événements de mai 2026 présents dans les données.",
        "La réponse doit identifier les lieux associés aux événements présents dans le contexte.",
    ]

    answers = []
    contexts = []

    for question in questions:
        docs = rag.retriever.invoke(question)
        context_list = [doc.page_content for doc in docs]
        answer = rag.ask(question)

        answers.append(answer)
        contexts.append(context_list)

    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths,
    }

    return Dataset.from_dict(data)


def main():
    api_key = os.getenv("MISTRAL_API_KEY")

    if not api_key:
        raise ValueError("MISTRAL_API_KEY introuvable dans le fichier .env")

    dataset = build_evaluation_dataset()

    evaluator_llm = LangchainLLMWrapper(
        ChatMistralAI(
            model="mistral-small-latest",
            mistral_api_key=api_key,
            temperature=0,
        )
    )

    evaluator_embeddings = LangchainEmbeddingsWrapper(
        HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    )

    result = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ],
        llm=evaluator_llm,
        embeddings=evaluator_embeddings,
    )

    print("Résultats RAGAS :")
    print(result)

    df = result.to_pandas()
    df.to_csv("ragas_results.csv", index=False)

    print("Résultats sauvegardés dans ragas_results.csv")


if __name__ == "__main__":
    main()