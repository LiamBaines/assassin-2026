import csv
import base64
import random

# --- Step 1: Encode targets ---
with open("dummy/dummy_player_targets.csv", newline="") as f:
    reader = csv.DictReader(f)
    dummy_targets = {row["name"]: row["target"] for row in reader}

with open("player_statuses.csv", newline="") as f:
    players = list(csv.DictReader(f))

# Overwrite target_b64
for player in players:
    name = player["name"]
    if name in dummy_targets:
        target_b64 = base64.b64encode(dummy_targets[name].encode()).decode()
        player["target_b64"] = target_b64

# --- Step 2: Assign shadow replicas ---
shadow_replicas = [p for p in players if p["status"] == "shadow_replica"]
alive_players = [p for p in players if p["status"] == "alive"]

if len(shadow_replicas) != len(alive_players):
    raise ValueError("Number of shadow replicas and alive players must match for 1:1 assignment.")

random.shuffle(alive_players)

for shadow, alive in zip(shadow_replicas, alive_players):
    shadow_b64 = base64.b64encode(shadow["name"].encode()).decode()
    alive["shadow_replica_b64"] = shadow_b64

# --- Step 3: Assign oracle phrases ---
with open("shadow_inputs/phrases.csv", newline="") as f:
    reader = csv.DictReader(f)
    phrases_data = [row for row in reader]

# Extract Liam-unknown phrases and full list
liam_phrases = [row["phrase"] for row in phrases_data if row["known_by_liam"].strip().lower() == "no"]

players_by_name = {p["name"]: p for p in players}
shadow_map = {p["name"]: base64.b64decode(p["shadow_replica_b64"]).decode()
              for p in players if p.get("shadow_replica_b64")}

# Map shadow replicas and replicas to their originals
shadow_to_original = {base64.b64decode(p["shadow_replica_b64"]).decode(): p["name"]
                      for p in players if p.get("shadow_replica_b64")}
replica_to_original = {p["replica"]: p["name"] for p in players if p.get("replica")}

# Combine both mappings for uniform handling
special_reverse_map = {**shadow_to_original, **replica_to_original}

# --- Step 3a: Assign Liam-unknown phrases properly ---
special_assignments = set()

for p in players:
    name = p["name"]
    # Decode target
    target_name = base64.b64decode(p["target_b64"]).decode() if p.get("target_b64") else None
    target_shadow = shadow_map.get(target_name)

    # Condition 1: Directly targeting Liam
    if target_name == "Liam":
        special_assignments.add(name)
        continue
    # Condition 2: Target's shadow replica is Liam
    if target_shadow == "Liam":
        special_assignments.add(name)
        continue
    # Condition 3 & 4: This player is a shadow replica or replica for someone targeting Liam
    original_for = special_reverse_map.get(name)
    if original_for:
        original_target = base64.b64decode(players_by_name[original_for]["target_b64"]).decode()
        if original_target == "Liam":
            special_assignments.add(name)
            continue
        if shadow_map.get(original_target) == "Liam":
            special_assignments.add(name)
            continue

# --- Step 4: assign Liam-unknown phrases ---
special_assignments_list = sorted(special_assignments)
if len(liam_phrases) < len(special_assignments_list):
    raise ValueError("Not enough Liam-unknown phrases for special assignments.")

# Assign Liam-unknown phrases (base64-encoded)
assigned_phrases = set()
for name, phrase in zip(special_assignments_list, liam_phrases):
    encoded_phrase = base64.b64encode(phrase.encode()).decode()
    players_by_name[name]["oracle_phrase_b64"] = encoded_phrase
    assigned_phrases.add(phrase)

# --- Step 5: assign remaining phrases to everyone else ---
remaining_players = [p for p in players if p["name"] not in special_assignments_list]

# Pool all phrases not already assigned
all_phrases = [row["phrase"] for row in phrases_data]
available_phrases = [ph for ph in all_phrases if ph not in assigned_phrases]

if len(remaining_players) > len(available_phrases):
    raise ValueError("Not enough remaining phrases for remaining players.")

random.shuffle(remaining_players)
for player, phrase in zip(remaining_players, available_phrases):
    encoded_phrase = base64.b64encode(phrase.encode()).decode()
    player["oracle_phrase_b64"] = encoded_phrase

# --- Step 6: Write updated CSV ---
fieldnames = ["name", "status", "target_b64", "replica", "shadow_replica_b64", "oracle_phrase_b64"]

with open("player_statuses.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for player in players:
        row = {k: player.get(k, "") for k in fieldnames}
        writer.writerow(row)