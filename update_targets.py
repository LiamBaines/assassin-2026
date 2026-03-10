# update_targets.py
import csv
import sys

if len(sys.argv) < 2:
    print("Usage: python update_targets.py <eliminated_player_1> [<eliminated_player_2> ...]")
    sys.exit(1)

eliminated = set(sys.argv[1:])

input_file = 'target/player_targets_round_2.csv'
output_file = 'shadow_inputs/player_targets_pre_shadow.csv'

# Read CSV into dictionary
with open(input_file, newline='') as f:
    reader = csv.DictReader(f)
    players = {row['name']: row['target'] for row in reader}

# Remove eliminated players and reassign targets
for dead in eliminated:
    if dead not in players:
        continue
    # Find who had this dead player as their target
    for p, t in players.items():
        if t == dead:
            players[p] = players[dead]  # Assassin inherits the target
    # Remove dead player
    players.pop(dead)

# Write updated CSV
with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'target'])
    writer.writeheader()
    for name, target in players.items():
        writer.writerow({'name': name, 'target': target})