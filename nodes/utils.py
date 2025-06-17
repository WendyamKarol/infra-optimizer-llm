import json
import os
from datetime import datetime

def save_to_json(data, prefix: str, output_dir="outputs"):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{prefix}_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)

    os.makedirs(output_dir, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return filepath
