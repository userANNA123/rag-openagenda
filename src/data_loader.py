import requests
import json
import os
from datetime import datetime, timedelta

os.makedirs("data", exist_ok=True)

url = "https://public.opendatasoft.com/api/records/1.0/search/"

today = datetime.now()
six_months_ago = today - timedelta(days=180)

params = {
    "dataset": "evenements-publics-openagenda",
    "rows": 100,
    "lang": "fr",
    "q": "Paris"
}

response = requests.get(url, params=params)
response.raise_for_status()

data = response.json()
records = data.get("records", [])

filtered_records = []

for record in records:
    fields = record.get("fields", {})
    date_str = fields.get("firstdate_begin", "")

    try:
        event_date = datetime.fromisoformat(date_str.replace("Z", "+00:00")).replace(tzinfo=None)
        if six_months_ago <= event_date <= today:
            filtered_records.append(record)
    except Exception:
        continue

if filtered_records:
    data["records"] = filtered_records
    print("Filtre temporel appliqué ✅")
else:
    print("Aucun événement trouvé sur les 6 derniers mois.")
    print("Fallback : utilisation des événements Paris disponibles.")
    data["records"] = records

with open("data/events.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Data saved ✅")
print("Nombre de records :", len(data.get("records", [])))