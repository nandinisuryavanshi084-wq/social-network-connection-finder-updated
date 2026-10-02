# Social Network Connection Finder — Updated DSA Project

## Features
- Add/remove users
- Add/remove connections
- Clear network and restore sample network
- Build a custom social network
- BFS and DFS traversal
- Graph visualization with path highlighting
- Traversal order, path length, nodes visited, measured execution time
- BFS vs DFS comparison
- Algorithm analysis: time/space complexity and characteristics

## Run
Open this folder in VS Code:
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## DSA
Graph: users are vertices and friendships are undirected edges.
Adjacency list: Python dictionary of user -> neighbors.
BFS: queue, O(V+E), O(V), shortest path for unweighted graphs.
DFS: stack, O(V+E), O(V), shortest path not guaranteed.

## Presentation Demo
1. Load Sample.
2. Select Alice -> Jack.
3. Run BFS.
4. Run DFS.
5. Click Compare BFS vs DFS.
6. Clear Network.
7. Add your own users and connections.
8. Run both algorithms on your custom network.
9. Explain V, E, O(V+E), queue, stack, and shortest-path difference.

Execution time shown on the site is an experimental measurement and can vary; theoretical complexity should be used for algorithm analysis.
