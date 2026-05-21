import requests
import json

url = "https://public.opendatasoft.com/api/records/1.0/search/"

params = {
    "dataset": "evenements-publics-openagenda",
    "rows": 100,
    "lang": "fr",
    "q": "Paris"
}

response = requests.get(url, params=params)
data = response.json()

with open("data/events.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Data saved ✅")