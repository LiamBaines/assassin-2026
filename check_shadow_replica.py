import csv
import sys
import base64

ASSIGNMENTS_FILE = "player_statuses.csv"

if len(sys.argv) != 3:
    print("Usage: python check_shadow_link.py <player> <shadow_replica>")
    sys.exit(1)

player_input = sys.argv[1]
replica_input = sys.argv[2]

# Encode the replica input to Base64 for comparison
replica_input_b64 = base64.b64encode(replica_input.encode("utf-8")).decode("utf-8")

players = {}
replicas = set()

with open(ASSIGNMENTS_FILE, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        player = row["name"]
        shadow_replica_b64 = row.get("shadow_replica_b64")  # Use get in case column missing
        if shadow_replica_b64:  # Only include non-empty shadow replicas
            players[player] = shadow_replica_b64
            replicas.add(shadow_replica_b64)

# Check existence
player_exists = player_input in players
replica_exists = replica_input_b64 in replicas

if not player_exists and not replica_exists:
    print("Neither the player nor the shadow replica appear in the file.")
elif not player_exists:
    print("The player does not appear in the file.")
elif not replica_exists:
    print("The shadow replica does not appear in the file.")
else:
    if players[player_input] == replica_input_b64:
        print("YES: The player and shadow replica are linked.")
    else:
        print("NO: The player and shadow replica are not linked.")