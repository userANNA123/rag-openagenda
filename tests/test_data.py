import json

def test_cleaned_events_exists():
    with open("data/cleaned_events.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) > 0