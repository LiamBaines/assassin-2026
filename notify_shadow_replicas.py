import csv
import base64
import requests

# --- Configuration ---
PLAYER_FILE = "players.csv"
GAME_FILE = "player_statuses.csv"
SLACK_WEBHOOK_URL = "https://hooks.slack.com/triggers/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"

# --- Step 1: Load player name → Slack ID mapping ---
player_to_slack = {}
with open(PLAYER_FILE, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        player_to_slack[row["name"]] = row["slack_user_id"]

# --- Step 2: Load game data ---
game_rows = []
with open(GAME_FILE, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        game_rows.append(row)

# --- Step 3: Find shadow replica pairs ---
pairs = []
for row in game_rows:
    shadow_b64 = row.get("shadow_replica_b64", "")
    if shadow_b64:
        try:
            shadow_name = base64.b64decode(shadow_b64).decode("utf-8")
        except Exception as e:
            print(f"Skipping row {row['name']}: cannot decode shadow_replica_b64 ({e})")
            continue
        original_name = row["name"]
        pairs.append((original_name, shadow_name))

# --- Step 4: Send Slack webhook for each pair ---
for original_name, shadow_name in pairs:
    original_slack = player_to_slack.get(original_name)
    shadow_slack = player_to_slack.get(shadow_name)
    if not original_slack or not shadow_slack:
        print(f"Skipping pair {original_name} → {shadow_name}: missing Slack ID")
        continue

    payload = {
        "original": original_slack,
        "shadow_replica": shadow_slack
    }

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            print(f"Sent pair {original_name} → {shadow_name}")
        else:
            print(f"Failed to send pair {original_name} → {shadow_name}: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Error sending pair {original_name} → {shadow_name}: {e}")