#include <bits/stdc++.h>
using namespace std;

struct Node {
    int id;
    double x, y;
};

struct Edge {
    int to;
    double weight;
};

class Graph {
public:
    void loadFromFile(const string &filename) {
        ifstream infile(filename);
        if (!infile) {
            cerr << "Error opening file: " << filename << endl;
            exit(EXIT_FAILURE);
        }

        int N, M;
        infile >> N >> M;

        nodes.clear();
        nodes.resize(N);
        adj.assign(N, {});

        for (int i = 0; i < N; ++i) {
            int id;
            double x, y;
            infile >> id >> x >> y;
            nodes[id] = {id, x, y};
        }

        for (int i = 0; i < M; ++i) {
            int u, v;
            double w;
            infile >> u >> v >> w;
            adj[u].push_back({v, w});
            adj[v].push_back({u, w});
        }
    }

    double heuristic(int u, int v) const {
        double dx = nodes[u].x - nodes[v].x;
        double dy = nodes[u].y - nodes[v].y;
        return sqrt(dx * dx + dy * dy);
    }

    vector<int> aStar(int start, int goal, double &pathCost) const {
        int n = static_cast<int>(nodes.size());
        const double INF = numeric_limits<double>::infinity();
        vector<double> g_score(n, INF), f_score(n, INF);
        vector<int> came_from(n, -1);

        typedef pair<double, int> PDI;
        priority_queue<PDI, vector<PDI>, greater<PDI>> openSet;

        g_score[start] = 0.0;
        f_score[start] = heuristic(start, goal);
        openSet.emplace(f_score[start], start);

        while (!openSet.empty()) {
            int current = openSet.top().second;
            openSet.pop();

            if (current == goal) {
                pathCost = g_score[goal];
                return reconstructPath(came_from, current);
            }

            for (const Edge &e : adj[current]) {
                int neighbor = e.to;
                double tentative_g = g_score[current] + e.weight;
                if (tentative_g < g_score[neighbor]) {
                    came_from[neighbor] = current;
                    g_score[neighbor] = tentative_g;
                    f_score[neighbor] = tentative_g + heuristic(neighbor, goal);
                    openSet.emplace(f_score[neighbor], neighbor);
                }
            }
        }

        pathCost = INF;
        return {}; // No path found
    }

    double calculatePathCost(const vector<int> &path) const {
        double cost = 0;
        for (size_t i = 0; i + 1 < path.size(); ++i) {
            int u = path[i], v = path[i + 1];
            for (const auto &e : adj[u]) {
                if (e.to == v) {
                    cost += e.weight;
                    break;
                }
            }
        }
        return cost;
    }

private:
    vector<Node> nodes;
public:
    vector<vector<Edge>> adj;

    vector<int> reconstructPath(const vector<int> &came_from, int cur) const {
        vector<int> path;
        while (cur != -1) {
            path.push_back(cur);
            cur = came_from[cur];
        }
        reverse(path.begin(), path.end());
        return path;
    }
};

int main() {
    Graph graph;
    const string filename = "map.txt";
    graph.loadFromFile(filename);

    int start, goal;
    cout << "Enter start node ID: ";
    cin >> start;
    cout << "Enter goal node ID: ";
    cin >> goal;

    if (start < 0 || goal < 0 || start >= (int)graph.adj.size() || goal >= (int)graph.adj.size()) {
        cerr << "Invalid node IDs.\n";
        return 1;
    }

    double minCost = 0.0;
    vector<int> shortestPath = graph.aStar(start, goal, minCost);

    if (shortestPath.empty()) {
        cout << "No path found from " << start << " to " << goal << endl;
        return 0;
    }

    // Simulate trying an alternative path (for now we use the same path for illustration)
    vector<int> altPath = shortestPath; // Replace this with an actual alternative if needed
    double altCost = graph.calculatePathCost(altPath);

    if (altCost <= 1.05 * minCost) {
        cout << "Accepted path (within 5% of shortest): ";
    } else {
        cout << "Fallback to shortest path: ";
        altPath = shortestPath;
    }

    for (size_t i = 0; i < altPath.size(); ++i) {
        cout << altPath[i] << (i + 1 < altPath.size() ? " -> " : "\n");
    }

    ofstream outfile("path.txt");
    if (!outfile) {
        cerr << "Error opening output file path.txt" << endl;
        return 1;
    }
    for (size_t i = 0; i < altPath.size(); ++i) {
        outfile << altPath[i];
        if (i + 1 < altPath.size()) outfile << " -> ";
    }
    outfile << "\n";
    outfile.close();

    return 0;
}