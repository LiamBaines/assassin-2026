import csv
import sys
import time
import json
import requests

# --- Configuration ---
PLAYERS_FILE = "players.csv"
WORDS_FILE = "target/words.csv"
SLACK_WEBHOOK = "https://hooks.slack.com/triggers/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"

# --- Optional CLI name filter ---
filter_names = {name.lower() for name in sys.argv[1:]}

# --- Load players (name -> slack_user_id) ---
players = {}
with open(PLAYERS_FILE, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        players[row["name"].lower()] = row["slack_user_id"]

if not players:
    raise ValueError("No players found in players CSV.")

# --- Load word assignments ---
assignments = []
with open(WORDS_FILE, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        assignments.append(row)

if not assignments:
    raise ValueError("No assignments found in words CSV.")

# --- Send messages ---
for entry in assignments:
    name = entry["name"]
    word = entry["word"]

    if filter_names and name.lower() not in filter_names:
        continue

    slack_user_id = players.get(name.lower())
    if not slack_user_id:
        print(f"No Slack user ID found for {name}, skipping")
        continue

    payload = {
        "word": word,
        "recipient": slack_user_id
    }

    time.sleep(1)
    resp = requests.post(
        SLACK_WEBHOOK,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=10,
    )

    if resp.status_code != 200:
        print(f"Failed to send word to {name}: {resp.text}")
    else:
        print(f"Sent word to {name}")
