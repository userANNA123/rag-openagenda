import json

with open("data/events.json", "r", encoding="utf-8") as f:
    data = json.load(f)

cleaned_events = []

for record in data.get("records", []):
    fields = record.get("fields", {})

    event = {
        "title": fields.get("title", ""),
        "description": fields.get("description", ""),
        "date": fields.get("firstdate_begin", ""),
        "location": fields.get("location_name", ""),
        "city": fields.get("city", "")
    }

    text = f"""
        Événement : {event['title']}
        Description : {event['description']}
        Date : {event['date']}
        Lieu : {event['location']}
        Ville : {event['city']}
      """
#if "paris" in event["city"].lower() and "culture" in event["description"].lower():
    
    cleaned_events.append(text)

with open("data/cleaned_events.json", "w", encoding="utf-8") as f:
    json.dump(cleaned_events, f, ensure_ascii=False, indent=2)

print("Cleaned data saved ✅")