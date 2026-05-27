import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("RAG OpenAgenda Chatbot")

question = st.text_input("Pose ta question :")

if st.button("Envoyer"):
    if not question.strip():
        st.warning("Veuillez saisir une question.")
    else:
        try:
            response = requests.post(
                f"{API_URL}/ask",
                json={"question": question},
                timeout=30
            )

            st.write("Status code:", response.status_code)

            if response.status_code == 200:
                data = response.json()
                st.subheader("Réponse")
                st.write(data.get("answer", data))
            else:
                st.error("Erreur API")
                st.code(response.text)

        except requests.exceptions.RequestException as e:
            st.error("Impossible de contacter l'API FastAPI.")
            st.code(str(e))