import requests


def test_home():
    response = requests.get("http://127.0.0.1:8000/")
    assert response.status_code == 200


def test_ask():
    payload = {
        "question": "Quels événements sont disponibles à Paris ?"
    }

    response = requests.post("http://127.0.0.1:8000/ask", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["answer"] != ""