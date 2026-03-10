import csv
import base64

# --- Load players ---
with open("player_statuses.csv", newline="") as f:
    players = list(csv.DictReader(f))

players_by_name = {p["name"]: p for p in players}

# --- Load phrases and Liam knowledge ---
with open("phrases.csv", newline="") as f:
    reader = csv.DictReader(f)
    phrases_info = {}
    for row in reader:
        phrase = row["phrase"].strip().strip('"')  # strip quotes and whitespace
        phrases_info[phrase] = row["known_by_liam"].strip().lower()  # yes/no

def is_known_by_liam(phrase):
    # strip quotes and whitespace for matching
    key = phrase.strip().strip('"')
    return phrases_info.get(key, "yes")  # default yes if not found

# --- Build reverse maps ---
shadow_to_original = {}
replica_to_original = {}

for p in players:
    if p.get("shadow_replica_b64"):
        shadow_name = base64.b64decode(p["shadow_replica_b64"]).decode()
        shadow_to_original[shadow_name] = p["name"]
    if p.get("replica"):
        replica_to_original[p["replica"]] = p["name"]

# --- Validation check ---
# Find who has Liam as shadow replica
liam_shadow_original = shadow_to_original.get("Liam")
if liam_shadow_original:
    print(f"Who has Liam as shadow replica?             {liam_shadow_original} (Liam)")

    # Who is targeting that player
    target_player = players_by_name[liam_shadow_original]
    targeter_name = None
    for p in players:
        if p.get("target_b64"):
            target_name = base64.b64decode(p["target_b64"]).decode()
            if target_name == liam_shadow_original:
                targeter_name = p["name"]
                break
    if targeter_name:
        print(f"Who is targeting {liam_shadow_original} (Liam)?         {targeter_name}")

        # Targeter's phrase
        targeter_phrase = players_by_name[targeter_name]["oracle_phrase"]
        print(f"What is {targeter_name}'s phrase?           {targeter_phrase}")
        print(f"Is this a phrase Liam knows?         {is_known_by_liam(targeter_phrase)}")

        # Targeter's shadow replica
        shadow_b64 = players_by_name[targeter_name].get("shadow_replica_b64")
        if shadow_b64:
            shadow_name = base64.b64decode(shadow_b64).decode()
            shadow_phrase = players_by_name[shadow_name]["oracle_phrase"]
            print(f"Who is {targeter_name}'s shadow replica?    {shadow_name}")
            print(f"What is {shadow_name}'s phrase?            {shadow_phrase}")
            print(f"Is this a phrase Liam knows?         {is_known_by_liam(shadow_phrase)}")
        else:
            shadow_name = None
            print(f"Who is {targeter_name}'s shadow replica?    n/a")
            print(f"What is n/a phrase?                         n/a")
            print(f"Is this a phrase Liam knows?         n/a")

        # Targeter's replica
        replica_name = players_by_name[targeter_name].get("replica")
        if replica_name and replica_name in players_by_name:
            replica_phrase = players_by_name[replica_name]["oracle_phrase"]
            print(f"Who is {targeter_name}'s replica?           {replica_name}")
            print(f"What is {replica_name}'s phrase?           {replica_phrase}")
            print(f"Is this a phrase Liam knows?         {is_known_by_liam(replica_phrase)}")
        else:
            print(f"Who is {targeter_name}'s replica?           n/a")
            print(f"What is n/a phrase?                         n/a")
            print(f"Is this a phrase Liam knows?         n/a")
else:
    print("No one has Liam as a shadow replica.")