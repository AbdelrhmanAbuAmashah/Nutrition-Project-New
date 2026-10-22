"""Fetch source records; never substitutes generated nutrient values."""
import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

FDC_IDS = [171705, 171688, 171413, 170457, 168409, 168878, 171477, 173424,
           173904, 170567, 172420, 173756, 170416, 170287, 169910, 173757,
           172421, 173944, 170000]
query = urlencode({"api_key": os.environ.get("FDC_API_KEY", "DEMO_KEY"),
                   "fdcIds": ",".join(map(str, FDC_IDS))})
with urlopen("https://api.nal.usda.gov/fdc/v1/foods?" + query, timeout=90) as response:
    records = json.load(response)
output = Path(__file__).resolve().parents[1] / "services/api/data/usda-source-records.json"
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps({"source": "USDA FoodData Central", "license": "CC0-1.0",
    "retrieved_at": "2026-10-22", "api_reference": "https://fdc.nal.usda.gov/api-guide/",
    "records": records}, ensure_ascii=False, indent=2) + "\n")
print(f"Saved {len(records)} USDA records")
for record in records:
    print(record["fdcId"], record["description"], record["dataType"])
