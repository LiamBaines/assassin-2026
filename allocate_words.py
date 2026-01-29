import csv
import json
import requests
import time
from openai import OpenAI

# --- Configuration ---
CSV_FILE = "players.csv"
SLACK_WEBHOOK = "https://hooks.slack.com/triggers/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"

# --- Read players from CSV ---
players = []
with open(CSV_FILE, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        players.append({"name": row["name"], "slack_user_id": row["slack_user_id"]})

num_players = len(players)
if num_players == 0:
    raise ValueError("No players found in CSV.")

# --- Call ChatGPT to generate words ---
client = OpenAI()

prompt = (
    f"Generate {num_players} random words for me. The words will be used in a game of "
    "word assassin, where players try to get someone to say the word, so they shouldn't be "
    "super common (i.e. likely to come up naturally in conversation regardless). This is for "
    "a group of colleagues who work as software engineers in a UK bank, so avoid words that "
    "could easily be elicited by discussing work (e.g. words related to payments, Java, biometrics, "
    "or general workplace terminology). Give your response as a comma-separated list without any other content."
)

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": prompt}],
)

# Parse the words from the response
words_text = response.choices[0].message.content.strip()
words = [w.strip() for w in words_text.split(",")]

if len(words) != num_players:
    raise ValueError(f"Number of words ({len(words)}) does not match number of players ({num_players})")

# --- Assign words to players and send to Slack ---
for player, word in zip(players, words):
    time.sleep(1)
    payload = {
        "word": word,
        "recipient": player["slack_user_id"]
    }
    resp = requests.post(
        SLACK_WEBHOOK,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=10,
    )
    if resp.status_code != 200:
        print(f"Failed to send word to {player['name']} ({player['slack_user_id']}): {resp.text}")
    else:
        print(f"Sent word '{word}' to {player['name']}")
