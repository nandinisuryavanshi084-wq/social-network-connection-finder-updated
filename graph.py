from collections import deque
from time import perf_counter

class SocialGraph:
    def __init__(self): self.adj={}
    def clear(self): self.adj.clear()
    def add_user(self,user):
        if user not in self.adj: self.adj[user]=set()
    def remove_user(self,user):
        if user not in self.adj: return False
        for n in list(self.adj[user]): self.adj[n].discard(user)
        del self.adj[user]; return True
    def add_connection(self,a,b):
        self.add_user(a); self.add_user(b); self.adj[a].add(b); self.adj[b].add(a)
    def remove_connection(self,a,b):
        if a in self.adj: self.adj[a].discard(b)
        if b in self.adj: self.adj[b].discard(a)
    def _path(self,parent,start,target):
        if target not in parent: return []
        p=[]; cur=target
        while cur is not None:
            p.append(cur)
            if cur==start: break
            cur=parent.get(cur)
        p.reverse()
        return p if p and p[0]==start else []
    def _result(self,algo,start,target,order,path,elapsed):
        return {"algorithm":algo,"start":start,"target":target,"traversal_order":order,
                "path":path,"path_length":len(path)-1 if path else None,"found":bool(path),
                "nodes_visited":len(order),"execution_time_ms":round(elapsed*1000,4),
                "explanation":f"{algo} explored {len(order)} node(s). "+
                (f"The connection requires {len(path)-1} edge(s)." if path else "The target was not reached.")}
    def bfs(self,start,target):
        if start not in self.adj or target not in self.adj: return self._result("BFS",start,target,[],[],0)
        t=perf_counter(); q=deque([start]); seen={start}; parent={start:None}; order=[]
        while q:
            cur=q.popleft(); order.append(cur)
            if cur==target: break
            for n in sorted(self.adj[cur]):
                if n not in seen: seen.add(n); parent[n]=cur; q.append(n)
        return self._result("BFS",start,target,order,self._path(parent,start,target),perf_counter()-t)
    def dfs(self,start,target):
        if start not in self.adj or target not in self.adj: return self._result("DFS",start,target,[],[],0)
        t=perf_counter(); stack=[start]; seen={start}; parent={start:None}; order=[]
        while stack:
            cur=stack.pop(); order.append(cur)
            if cur==target: break
            for n in sorted(self.adj[cur],reverse=True):
                if n not in seen: seen.add(n); parent[n]=cur; stack.append(n)
        return self._result("DFS",start,target,order,self._path(parent,start,target),perf_counter()-t)
    def to_dict(self):
        edges=[]; seen=set()
        for u in sorted(self.adj):
            for v in sorted(self.adj[u]):
                e=tuple(sorted((u,v)))
                if e not in seen: seen.add(e); edges.append({"source":e[0],"target":e[1]})
        return {"nodes":[{"id":u} for u in sorted(self.adj)],"edges":edges,
                "adjacency":{u:sorted(self.adj[u]) for u in sorted(self.adj)}}
