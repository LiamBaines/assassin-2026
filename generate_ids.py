import csv
import random

input_file = "players.csv"
output_file = "player_ids.csv"

# Read players
with open(input_file, newline='') as f:
    reader = csv.DictReader(f)
    players = [row['name'] for row in reader]

# Generate unique 4-digit IDs
ids = random.sample(range(1000, 10000), len(players))
player_id_map = dict(zip(players, ids))

# Write player_ids.csv
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'id'])
    for name, pid in player_id_map.items():
        writer.writerow([name, pid])

print(f"Generated {output_file}")
