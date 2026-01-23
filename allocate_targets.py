import csv
import random

input_file = "players.csv"
output_file = "player_targets.csv"

# Read players
with open(input_file, newline='') as f:
    reader = csv.DictReader(f)
    players = [row['name'] for row in reader]

# Shuffle players for random circle
random.shuffle(players)

# Allocate targets in a circular manner
player_targets_map = {players[i]: players[(i + 1) % len(players)] for i in range(len(players))}

# Write player_targets.csv
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'target'])
    for name, target in player_targets_map.items():
        writer.writerow([name, target])

print(f"Generated {output_file}")
