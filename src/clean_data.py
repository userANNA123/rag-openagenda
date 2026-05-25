import json
from pathlib import Path

DATA_DIR = Path("data")


def clean_events():
    input_path = DATA_DIR / "events.json"
    output_path = DATA_DIR / "cleaned_events.json"

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned_events = []
    records = data.get("records", [])

    for record in records:
        fields = record.get("fields", {})

        title = fields.get("title_fr") or fields.get("title") or fields.get("slug") or ""
        description = fields.get("description_fr") or fields.get("longdescription_fr") or ""
        date = fields.get("firstdate_begin") or fields.get("daterange_fr") or ""
        location = fields.get("location_name") or fields.get("location_address") or ""
        city = fields.get("location_city") or fields.get("city") or ""
        keywords = fields.get("keywords_fr") or ""
        url = fields.get("canonicalurl") or ""

        text = f"""
Événement : {title}
Description : {description}
Date : {date}
Lieu : {location}
Ville : {city}
Mots-clés : {keywords}
URL : {url}
""".strip()

        if title or description or location or city:
            cleaned_events.append(text)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_events, f, ensure_ascii=False, indent=2)

    return len(cleaned_events)


if __name__ == "__main__":
    count = clean_events()
    print("Cleaned data saved ✅")
    print("Nombre d'événements nettoyés :", count)