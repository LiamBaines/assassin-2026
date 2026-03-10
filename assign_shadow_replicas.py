import csv
import random

# Input/output files
shadow_replicas_file = "shadow_replicas.csv"
players_file = "shadow_replica_originals.csv"
assignments_file = "shadow_replica_assignments.csv"

# Read shadow replicas
with open(shadow_replicas_file, newline="") as f:
    reader = csv.DictReader(f)
    shadow_replicas = [row["shadow_replica"] for row in reader]

# Read players and existing assignments
assignments = []
with open(assignments_file, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        assignments.append(row)

# Shuffle shadow replicas
if len(shadow_replicas) != len(assignments):
    raise ValueError("Number of shadow replicas must match number of players in assignments file")
random.shuffle(shadow_replicas)

# Assign shadow replicas to each player, keeping the 'replica' column
for i, row in enumerate(assignments):
    row["shadow_replica"] = shadow_replicas[i]

# Write updated assignments
with open(assignments_file, "w", newline="") as f:
    fieldnames = ["player", "replica", "shadow_replica"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(assignments)

print(f"Updated assignments written to {assignments_file}")