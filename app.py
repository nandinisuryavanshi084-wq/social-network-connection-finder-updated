from flask import Flask, render_template, request, jsonify
from graph import SocialGraph

app = Flask(__name__)
graph = SocialGraph()

SAMPLE_USERS = ["Alice","Bob","Charlie","David","Eve","Frank","Grace","Henry","Isha","Jack"]
SAMPLE_CONNECTIONS = [
    ("Alice","Bob"),("Alice","David"),("Bob","Charlie"),("Bob","Eve"),
    ("Charlie","Frank"),("David","Eve"),("David","Grace"),("Eve","Henry"),
    ("Frank","Isha"),("Grace","Isha"),("Grace","Jack"),("Henry","Jack")
]

def load_sample_graph():
    graph.clear()
    for u in SAMPLE_USERS: graph.add_user(u)
    for a,b in SAMPLE_CONNECTIONS: graph.add_connection(a,b)

load_sample_graph()

@app.route("/")
def index(): return render_template("index.html")

@app.get("/api/graph")
def get_graph(): return jsonify(graph.to_dict())

@app.post("/api/users")
def add_user():
    name=str((request.get_json() or {}).get("name","")).strip()
    if not name: return jsonify(success=False,error="User name cannot be empty."),400
    if name in graph.adj: return jsonify(success=False,error="User already exists."),400
    graph.add_user(name)
    return jsonify(success=True,message=f"User '{name}' added.",graph=graph.to_dict())

@app.delete("/api/users/<path:name>")
def remove_user(name):
    if name not in graph.adj: return jsonify(success=False,error="User not found."),404
    graph.remove_user(name)
    return jsonify(success=True,message=f"User '{name}' removed.",graph=graph.to_dict())

@app.post("/api/connections")
def add_connection():
    d=request.get_json() or {}; a=str(d.get("user1","")).strip(); b=str(d.get("user2","")).strip()
    if not a or not b: return jsonify(success=False,error="Both users are required."),400
    if a==b: return jsonify(success=False,error="A user cannot connect to themselves."),400
    if a not in graph.adj or b not in graph.adj: return jsonify(success=False,error="Both users must exist first."),400
    if b in graph.adj[a]: return jsonify(success=False,error="Connection already exists."),400
    graph.add_connection(a,b)
    return jsonify(success=True,message=f"Connection added: {a} — {b}.",graph=graph.to_dict())

@app.delete("/api/connections")
def remove_connection():
    d=request.get_json() or {}; a=str(d.get("user1","")).strip(); b=str(d.get("user2","")).strip()
    if a not in graph.adj or b not in graph.adj: return jsonify(success=False,error="Both users must exist."),400
    if b not in graph.adj[a]: return jsonify(success=False,error="Connection does not exist."),404
    graph.remove_connection(a,b)
    return jsonify(success=True,message=f"Connection removed: {a} — {b}.",graph=graph.to_dict())

@app.post("/api/traverse")
def traverse():
    d=request.get_json() or {}; start=str(d.get("start","")).strip(); target=str(d.get("target","")).strip()
    algo=str(d.get("algorithm","BFS")).upper()
    if start not in graph.adj or target not in graph.adj: return jsonify(success=False,error="Start and target users must exist."),400
    if algo not in ("BFS","DFS"): return jsonify(success=False,error="Algorithm must be BFS or DFS."),400
    r=graph.bfs(start,target) if algo=="BFS" else graph.dfs(start,target)
    return jsonify(success=True,result=r)

@app.post("/api/compare")
def compare():
    d=request.get_json() or {}; start=str(d.get("start","")).strip(); target=str(d.get("target","")).strip()
    if start not in graph.adj or target not in graph.adj: return jsonify(success=False,error="Start and target users must exist."),400
    b=graph.bfs(start,target); f=graph.dfs(start,target)
    return jsonify(success=True,comparison={"start":start,"target":target,"bfs":b,"dfs":f})

@app.post("/api/reset")
def reset():
    load_sample_graph()
    return jsonify(success=True,message="Sample graph restored.",graph=graph.to_dict())

@app.post("/api/clear")
def clear():
    graph.clear()
    return jsonify(success=True,message="Network cleared.",graph=graph.to_dict())

if __name__=="__main__":
    app.run(debug=True)
