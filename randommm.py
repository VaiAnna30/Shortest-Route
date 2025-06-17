import random
import math

# random.seed(42)

# Must be ≥ num_nodes - 1 to ensure connectivity
num_nodes = 50
num_edges = 75  

# Assert statement is given because we have to check the bug{Here the bug is that no. of edges are less than no. of nodes-1}
assert num_edges >= num_nodes - 1, "Not enough edges to ensure connectivity."

# Generate unique node coordinates (id, x, y)
nodes = []
for i in range(num_nodes):
    # Here x and y are storing rangom number b/w 0 to 100 upto 2 decimal places
    x = round(random.uniform(0, 100), 2)
    y = round(random.uniform(0, 100), 2)
    nodes.append((i, x, y))


# Helper: Euclidean distance + noise
def edge_weight(i, j):
    x1, y1 = nodes[i][1], nodes[i][2]
    x2, y2 = nodes[j][1], nodes[j][2]
    #calculating Distance
    dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    # adding some noise indicating trafic lights
    return round(dist + random.uniform(0, 10), 2)

# Step 1: Ensure connectivity using a randomized Prim-like method
# connected and edges are a set because we dont want duplicates
connected = set([0])
# connected stores set of connected nodes
edges = set()
# edges stored the set of edges

# Below code makes sure that every node is reachable from every other node
# counting is done till my connected size is not equal to number of node which means all nodes are noy connected
while len(connected) < num_nodes:
    # First we Randomly Choose a node from previously connected nodes
    u = random.choice(list(connected))

    # list of unconnected nodes will store all the nodes which are not connected till now 
    unconnected_nodes = []
    for n in range(num_nodes):
        if n not in connected:
            unconnected_nodes.append(n)
    # v will store the random calue from the list of unconnected_nodes
    v = random.choice(unconnected_nodes)

    #define a edge between u and v with an edge weight w
    w = edge_weight(u, v)
    edges.add((u, v, w))
    connected.add(v)

# Step 2: Add extra random edges
while len(edges) < num_edges:
    # for u and v we are choosing any random integer from 0 to no. of node-1
    u = random.randint(0, num_nodes - 1)
    v = random.randint(0, num_nodes - 1)
    # made sure that u an v are not already present in my edges
    if u != v and (u, v) not in edges and (v, u) not in edges:
        w = edge_weight(u, v)
        edges.add((u, v, w))

# Step 3: Save to map.txt
output = [f"{num_nodes} {len(edges)}"]
output.extend(f"{i} {x} {y}" for i, x, y in nodes)
output.extend(f"{u} {v} {w}" for u, v, w in edges)

with open("map.txt", "w") as f:
    f.write("\n".join(output) + "\n")
