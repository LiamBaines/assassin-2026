import csv
import json
import requests
import time

WEBHOOK_URL = "https://hooks.slack.com/triggers/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"

PLAYERS_FILE = "players.csv"
IDS_FILE = "player_ids.csv"

# Load name -> slack_user_id
players = {}
with open(PLAYERS_FILE, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        players[row["name"]] = row["slack_user_id"]

# Load name -> assassinId
ids = {}
with open(IDS_FILE, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        ids[row["name"]] = row["id"]

# Send webhook for each player
for name in players:
    time.sleep(1)
    if name not in ids:
        raise ValueError(f"No ID found for player '{name}'")

    payload = {
        "assassinId": str(ids[name]),
        "recipient": players[name],
    }

    response = requests.post(
        WEBHOOK_URL,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=10,
    )

    if response.status_code >= 400:
        raise RuntimeError(
            f"Failed to send message for {name}: "
            f"{response.status_code} {response.text}"
        )

    print(f"Sent webhook for {name}")

print("All webhooks sent successfully.")
