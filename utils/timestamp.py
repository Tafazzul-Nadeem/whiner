import json
import os

def get_last_timestamp():
    json_path = "./last_timestamp.json"
    if not os.path.exists(json_path):
        # Create the file with default content
        with open(json_path, "w") as f:
            json.dump({"last_timestamp": None}, f)
        return None
    with open(json_path, "r") as f:
        data = json.load(f)
        return data.get("last_timestamp")

def update_last_timestamp(latest_email_date):
    with open("last_timestamp.json") as f:
            data = json.load(f)
    data["last_timestamp"] = latest_email_date
    with open("last_timestamp.json", "w") as f:
        json.dump(data, f)