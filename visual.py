import matplotlib.pyplot as plt
import time

def read_map(filename):
    with open(filename) as f:
        N, M = map(int, f.readline().strip().split())
        nodes = {}
        for _ in range(N):
            id, x, y = f.readline().split()
            nodes[int(id)] = (float(x), float(y))
        edges = []
        for _ in range(M):
            u, v, w = f.readline().split()
            edges.append((int(u), int(v), float(w)))
    return nodes, edges

def read_path(filename):
    with open(filename) as f:
        content = f.read().strip()
    if '->' in content:
        parts = [p.strip() for p in content.split('->')]
    else:
        parts = [p.strip() for p in content.replace(',', ' ').split()]
    return [int(p) for p in parts]

def visualize(nodes, edges, path):
    fig, ax = plt.subplots(figsize=(16, 12))

    # Draw all edges
    for u, v, w in edges:
        x1, y1 = nodes[u]
        x2, y2 = nodes[v]
        ax.plot([x1, x2], [y1, y2], color='gray', linewidth=1, zorder=1)

    # Plot all nodes
    xs = [coord[0] for coord in nodes.values()]
    ys = [coord[1] for coord in nodes.values()]
    ax.scatter(xs, ys, color='black', zorder=2)
    for id, (x, y) in nodes.items():
        ax.text(x, y, str(id), color='blue', fontsize=12, zorder=3)

    # Setup plot
    ax.set_aspect('equal', 'box')
    ax.set_title('Animated Route Visualization')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)

    # Animate the path with 3-second delay between steps
    for i in range(len(path) - 1):
        x1, y1 = nodes[path[i]]
        x2, y2 = nodes[path[i + 1]]
        ax.plot([x1, x2], [y1, y2], color='red', linewidth=2, marker='o', zorder=4)
        plt.pause(1)  # ← 1 seconds pause

    plt.show()

# Main execution
if __name__ == '__main__':
    path_file = 'path.txt'
    map_file = 'map.txt'
    nodes, edges = read_map(map_file)
    path = read_path(path_file)
    visualize(nodes, edges, path)
