import csv
from openai import OpenAI

# --- Configuration ---
PLAYERS_FILE = "players.csv"
OUTPUT_FILE = "target/words.csv"

# --- Read players ---
players = []
with open(PLAYERS_FILE, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        players.append(row["name"])

num_players = len(players)
if num_players == 0:
    raise ValueError("No players found in CSV.")

# --- Call ChatGPT ---
client = OpenAI()

prompt = (
    f"Generate {num_players} random words for me. The words will be used in a game of "
    "word assassin, where players try to get someone to say the word, so they shouldn't be "
    "super common (i.e. likely to come up naturally in conversation regardless), though you should "
    "avoid words that the average person would likely be completely unfamiliar with. This is for "
    "a group of colleagues who work as software engineers in a UK bank, so avoid words that "
    "could easily be elicited by discussing work (e.g. words related to payments, Java, biometrics, "
    "or general workplace terminology). Avoid words commonly used by language models as 'interesting' "
    "examples (e.g. quasar, zeppelin, alcove, serendipity, ephemeral, labyrinth, juxtaposition). "
    "Give your response as a comma-separated list without any other content. Avoid poetic, sci-fi, "
    "or creative-writing-prompt style words. Generate a new random starting letter before deciding each "
    "word."
)

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": prompt}],
)

words_text = response.choices[0].message.content.strip()
words = [w.strip() for w in words_text.split(",")]

if len(words) != num_players:
    raise ValueError(
        f"Number of words ({len(words)}) does not match number of players ({num_players})"
    )

# --- Write words.csv ---
with open(OUTPUT_FILE, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["name", "word"])

    for name, word in zip(players, words):
        writer.writerow([name, word])

print(f"Wrote {num_players} words to {OUTPUT_FILE}")
