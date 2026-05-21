import streamlit as st
import requests

st.title("RAG OpenAgenda Chatbot")

question = st.text_input("Pose ta question :")

if st.button("Envoyer"):
    response = requests.post(
        "http://127.0.0.1:8000/ask",
        json={"question": question}
    )

    if response.status_code == 200:
        st.write(response.json()["answer"])
    else:
        st.error("Erreur API")