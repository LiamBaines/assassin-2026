import csv
import random

input_file = "target/allocation_notes_stripped.csv"
output_file = "target/player_targets_round_2.csv"
MAX_ATTEMPTS = 10000

# Read players and exclusions
players = []
exclusions_map = {}

with open(input_file, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row['name'].strip()
        players.append(name)

        exclusions = row.get('exclusions', '').strip()
        if exclusions:
            exclusions_map[name] = set(x.strip() for x in exclusions.split('/'))
        else:
            exclusions_map[name] = set()

def is_valid_circle(order):
    for i, player in enumerate(order):
        target = order[(i + 1) % len(order)]
        if target in exclusions_map[player]:
            return False
    return True

# Try random circular assignments until valid
for attempt in range(MAX_ATTEMPTS):
    shuffled = players[:]
    random.shuffle(shuffled)

    if is_valid_circle(shuffled):
        player_targets_map = {
            shuffled[i]: shuffled[(i + 1) % len(shuffled)]
            for i in range(len(shuffled))
        }
        break
else:
    raise RuntimeError("Could not find a valid assignment with given exclusions.")

# Write output
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'target'])
    for name, target in player_targets_map.items():
        writer.writerow([name, target])

print(f"Generated {output_file}")