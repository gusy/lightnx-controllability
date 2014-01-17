from digraph import DiGraph
import collections,random

INFINITY = -1

def getBipartite(G):
    bip = {}
    for node in G.nodes():
        bip[str(node)+"+"] =set([])
        bip[str(node)+"-"] =set([])
    for link in G.edges():
        node1 = link[0]
        node2 = link[1]
        bip[str(node1)+"+"].add(str(node2)+"-")
        bip[str(node2)+"-"].add(str(node1)+"+")
    return bip


class signIT:
	"""Iterator for looping over a sequence backwards."""
	def __init__(self, data,fil):
		self.data = data
		self.index = 0
		self.fil=fil
	def __iter__(self):
		return self
	def next(self):
		if self.index == len(self.data):
			raise StopIteration
		while(str(self.data[self.index])[-1:]!=self.fil):
			self.index = self.index +1
			if self.index == len(self.data):
				raise StopIteration
		self.index = self.index +1
		return self.data[self.index-1]

def G1nodes(allnodes):
    return signIT(allnodes,"+")

def G2nodes(allnodes):
    return signIT(allnodes,"-")

def bfs(allnodes, bip, pair, dist, q):
    for node in G1nodes(allnodes):
        if pair[node] == None:
            dist[node] = 0
            q.append(node)
        else:
            dist[node] = INFINITY

    dist[None] = INFINITY

    while len(q) > 0:
        v = q.popleft()
        if v != None:
            neighbours3= bip[v]
#            random.shuffle(neighbours3)
            for u in neighbours3:
                if dist[ pair[u] ] == INFINITY:
                    dist[pair[u] ] = dist[v] + 1
                    q.append(pair[u])
    return dist[None] != INFINITY

def dfs(bip, v, pair, dist):
    if v != None:
        neighbours3= bip[v]
#        random.shuffle(neighbours3)
        for u in neighbours3:
            if dist[ pair[u] ] == dist[v] + 1 and dfs(bip, pair[u], pair, dist):
                pair[u] = v
                pair[v] = u
                edge = (v.split("+")[0],u.split("-")[0])
                return True
        dist[v] = INFINITY
        return False
    return True

'''
 Parameters
 ----------
 G : DiGraph
 Directed graph you need to find a maximum matching for
'''
def matching(G):
    pair = {}
    dist = {}
    q = collections.deque()
    bip = getBipartite(G)
    allnodes = bip.keys()
    for node in G1nodes(allnodes):
        pair[node] = None
        dist[node] = INFINITY
    for node in G2nodes(allnodes):
        pair[node] = None
        dist[node] = INFINITY
    matching = 0 ##candidato a ser borrado a muerte
    while  bfs(allnodes, bip, pair, dist, q):
        for node in G1nodes(allnodes):
            if ( (pair[node] == None) and (dfs(bip, node, pair, dist)) ):
                matching = matching + 1
    matching_edges=[]
    for node in G1nodes(allnodes):
        if pair[node]!= None:
            matching_edges.append((node[:-1],pair[node][:-1]))
    if len(matching_edges)!= matching:
        raise Exception("matching dimension and calculated number do not match")
    return matching_edges

