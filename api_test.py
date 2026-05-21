import requests

url = "http://127.0.0.1:8000/ask"

payload = {
    "question": "Quels événements sont disponibles à Paris ?"
}

response = requests.post(url, json=payload)

print("Status code:", response.status_code)
print("Réponse JSON:")
print(response.json())