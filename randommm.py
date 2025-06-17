import random
import math

random.seed(42)  # Optional: Set seed for reproducibility

num_nodes = 50
num_edges = 75  # Must be ≥ num_nodes - 1 to ensure connectivity
assert num_edges >= num_nodes - 1, "Not enough edges to ensure connectivity."

# Generate unique node coordinates (id, x, y)
nodes = [(i, round(random.uniform(0, 100), 2), round(random.uniform(0, 100), 2)) for i in range(num_nodes)]

# Helper: Euclidean distance + noise
def edge_weight(i, j):
    x1, y1 = nodes[i][1], nodes[i][2]
    x2, y2 = nodes[j][1], nodes[j][2]
    dist = math.hypot(x2 - x1, y2 - y1)
    return round(dist + random.uniform(0, 10), 2)

# Step 1: Ensure connectivity using a randomized Prim-like method
connected = set([0])
edges = set()
while len(connected) < num_nodes:
    u = random.choice(list(connected))
    v = random.choice([n for n in range(num_nodes) if n not in connected])
    w = edge_weight(u, v)
    edges.add((u, v, w))
    connected.add(v)

# Step 2: Add extra random edges
while len(edges) < num_edges:
    u = random.randint(0, num_nodes - 1)
    v = random.randint(0, num_nodes - 1)
    if u != v and (u, v) not in edges and (v, u) not in edges:
        w = edge_weight(u, v)
        edges.add((u, v, w))

# Step 3: Save to map.txt
output = [f"{num_nodes} {len(edges)}"]
output.extend(f"{i} {x} {y}" for i, x, y in nodes)
output.extend(f"{u} {v} {w}" for u, v, w in edges)

with open("map.txt", "w") as f:
    f.write("\n".join(output) + "\n")
