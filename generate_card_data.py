import csv
import json
import base64

# Input files
ids_file = "player_ids.csv"
targets_file = "player_targets.csv"
output_file = "player_card_data.csv"

# Read player IDs
player_id_map = {}
with open(ids_file, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        player_id_map[row['name']] = row['id']

# Read player targets
player_target_map = {}
with open(targets_file, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        player_target_map[row['name']] = row['target']

# Generate Base64-encoded JSON for each player
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['player', 'card_data'])
    for player in player_id_map:
        data = {
            "assassin": player,
            "id": player_id_map[player],
            "target": player_target_map[player]
        }
        json_str = json.dumps(data)
        b64_str = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
        writer.writerow([player, b64_str])

print(f"Generated {output_file}")
