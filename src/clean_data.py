import json
from pathlib import Path

DATA_DIR = Path("data")

input_path = DATA_DIR / "events.json"
output_path = DATA_DIR / "cleaned_events.json"

with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

cleaned_events = []

records = data.get("records", [])

print("Nombre de records lus :", len(records))

if records:
    print("Champs disponibles dans le premier record :")
    print(records[0].get("fields", {}).keys())

for record in records:
    fields = record.get("fields", {})

    title = (
        fields.get("title")
        or fields.get("titre")
        or fields.get("slug")
        or ""
    )

    description = (
        fields.get("description")
        or fields.get("longdescription")
        or fields.get("conditions")
        or ""
    )

    date = (
        fields.get("firstdate_begin")
        or fields.get("date_start")
        or fields.get("lastdate_end")
        or ""
    )

    location = (
        fields.get("location_name")
        or fields.get("placename")
        or fields.get("address")
        or ""
    )

    city = (
        fields.get("city")
        or fields.get("location_city")
        or fields.get("department")
        or ""
    )

    text = f"""
Événement : {title}
Description : {description}
Date : {date}
Lieu : {location}
Ville : {city}
""".strip()

    if title or description or location or city:
        cleaned_events.append(text)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(cleaned_events, f, ensure_ascii=False, indent=2)

print("Cleaned data saved ✅")
print("Nombre d'événements nettoyés :", len(cleaned_events))