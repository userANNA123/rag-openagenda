import requests
import json
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def fetch_openagenda_events(city="Paris", months=6, rows=100):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=30 * months)

    url = "https://public.opendatasoft.com/api/records/1.0/search/"

    params = {
        "dataset": "evenements-publics-openagenda",
        "rows": rows,
        "lang": "fr",
        "q": "Paris 2026",
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()
    records = data.get("records", [])

    filtered_records = []

    for record in records:
        fields = record.get("fields", {})
        date_str = fields.get("firstdate_begin", "")

        if not date_str:
            continue

        try:
            event_date = datetime.fromisoformat(
                date_str.replace("Z", "+00:00")
            ).replace(tzinfo=None)

            if start_date <= event_date <= end_date:
                filtered_records.append(record)

        except Exception:
            continue

    if filtered_records:
        data["records"] = filtered_records
        print("Filtre temporel appliqué ✅")
    else:
        data["records"] = records
        print("Aucun événement trouvé sur les 6 derniers mois.")
        print("Fallback : utilisation des événements Paris disponibles.")

    output_path = DATA_DIR / "events.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Data saved ✅")
    print("Nombre de records :", len(data.get("records", [])))

    return data


if __name__ == "__main__":
    fetch_openagenda_events()