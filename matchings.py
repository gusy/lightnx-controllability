from digraph import DiGraph
import collections
import random
from sets import Set

INFINITY = -1

def getBipartite(G):
    bip = {}
    for node in G.nodes():
        bip[str(node)+"+"] =[] #set([])
        bip[str(node)+"-"] =[] #set([])
    for link in G.edges():
        node1 = link[0]
        node2 = link[1]
        bip[str(node1)+"+"].append(str(node2)+"-")
        bip[str(node2)+"-"].append(str(node1)+"+")
    return bip


class signIT:
    """Iterator for looping over a sequence backwards."""
    def __init__(self, data, fil):
        self.data = data
        self.index = 0
        self.fil = fil
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
                edge = (v.split("+")[0], u.split("-")[0])
                return True
        dist[v] = INFINITY
        return False
    return True

'''
 Parameters
---------
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
    matching = 0
    while  bfs(allnodes, bip, pair, dist, q):
        for node in G1nodes(allnodes):
            if ( (pair[node] == None) and (dfs(bip, node, pair, dist)) ):
                matching = matching + 1
    matching_edges=[]
    for node in G1nodes(allnodes):
        if pair[node]!= None:
            matching_edges.append((node[:-1], pair[node][:-1]))
    if len(matching_edges)!= matching:
        raise Exception("matching dimension and calculated number do not match")
    return matching_edges

def strongly_connected_components(G):
    """Return nodes in strongly connected components of graph.

    Parameters
    ----------
    G : NetworkX Graph
       An directed graph.

    Returns
    -------
    comp : list of lists
       A list of nodes for each component of G.
       The list is ordered from largest connected component to smallest.

    See Also
    --------
    connected_components

    Notes
    -----
    Uses Tarjan's algorithm with Nuutila's modifications.
    Nonrecursive version of algorithm.

    References
    ----------
    .. [1] Depth-first search and linear graph algorithms, R. Tarjan
       SIAM Journal of Computing 1(2):146-160, (1972).

    .. [2] On finding the strongly connected components in a directed graph.
       E. Nuutila and E. Soisalon-Soinen
       Information Processing Letters 49(1): 9-14, (1994)..
    """
    preorder={}
    lowlink={}
    scc_found={}
    scc_queue = []
    scc_list=[]
    i=0     # Preorder counter
    for source in G.nodes():
        if source not in scc_found:
            queue=[source]
            while queue:
                v=queue[-1]
                if v not in preorder:
                    i=i+1
                    preorder[v]=i
                done=1
                v_nbrs=G.successors(v)
                for w in v_nbrs:
                    if w not in preorder:
                        queue.append(w)
                        done=0
                        break
                if done==1:
                    lowlink[v]=preorder[v]
                    for w in v_nbrs:
                        if w not in scc_found:
                            if preorder[w]>preorder[v]:
                                lowlink[v]=min([lowlink[v],lowlink[w]])
                            else:
                                lowlink[v]=min([lowlink[v],preorder[w]])
                    queue.pop()
                    if lowlink[v]==preorder[v]:
                        scc_found[v]=True
                        scc=[v]
                        while scc_queue and preorder[scc_queue[-1]]>preorder[v]:
                            k=scc_queue.pop()
                            scc_found[k]=True
                            scc.append(k)
                        scc_list.append(scc)
                    else:
                        scc_queue.append(v)
    scc_list.sort(key=len,reverse=True)
    return scc_list

def is_non_top_linked(G,scc):
    isRoot=True
    scc=set(scc) # scc is better as set for optimized "in" below
    for node in scc:
        #print node, self.G3nei[node+"-"]
        predecessors=G.predecessors(node)
        if len(predecessors)>0:
            for source in predecessors:
                if source not in scc:
                    isRoot=False
                    break
        if not isRoot:
            break
    return isRoot

def controllers_dilation(matching,nodes):
    controllers = set(map(str,nodes[:]))
    for edge in matching:
        if edge[1] in controllers:
            controllers.remove(edge[1])
    return controllers
def is_perfect_matchable(sccGraph):
    sccSize=len(sccGraph.nodes())
    sccMatch=matching(sccGraph)
    is_perfect_matchable = False
    if len(sccMatch)==sccSize:
        is_perfect_matchable=True
    return is_perfect_matchable

def controller_set(G):
    sccs = strongly_connected_components(G)
    mm = matching(G)
    cont = controllers_dilation(mm,G.nodes())
    #non_tops = map(lambda scc: is_non_top(G,scc), sccs)
    non_top_linked = []
    for scc in sccs:
        if is_non_top_linked(G,scc):
            non_top_linked.append(scc)
            scc_controlled = False
            for node in scc:
                if str(node) in cont:
                    scc_controlled = True
                    break
            if not scc_controlled:
                cont.add(str(scc[0]))
    return cont
#def isAssignable(G,scc):

class SCC():
    def __init__(self,subgraph):
        self.graph = subgraph #either a networkX.DiGraph or a lightnx.DiGraph
        self.outnodes = set([])
        self.outlinks = []

    def __contains__(self, node):
        if self.graph.has_node(node):
            return True
        return False

def get_pm_nt_scc_and_Gprime(G):
    '''returns a list set of perfect matchable non top-linked strongly connected components of a graph
        returned objects of class "scc"
        returns also a subgraph o G' (the rest of the graph except for the S_nt_ru)
    '''
    sccs=strongly_connected_components(G)
    #non_top_linked=[]
    perfect_matchable_nt=[]
    nodesOnGPrime=Set(G.nodes())
    for scc in sccs:
        if is_non_top_linked(G,scc):
            #non_top_linked.append(scc)
            sccnt = SCC(G.subgraph(scc))
            if is_perfect_matchable(sccnt.graph):
                for node in scc:
                    nodesOnGPrime.remove(node)
                    for outnode in G.successors(node): # NOT USING NEI!!! is not nx compliant
                        if outnode not in sccnt: ##use the __contains in class scc)
                            sccnt.outnodes.add(outnode)
                            sccnt.outlinks.append((node, outnode))
                perfect_matchable_nt.append(sccnt)
#                            if node not in perfect_matchable_nt2[-1]["outlinks"]:
                                #perfect_matchable_nt2[-1]["outlinks"][node]=Set([])
                            #perfect_matchable_nt2[-1]["outlinks"][node].add(outlink)
#                perfect_matchable_nt.append(scc)
    Gprime=G.subgraph(nodesOnGPrime)
    return perfect_matchable_nt, Gprime

#def optimal_set(G):
#    s_nt_ru, gprime = get_pm_nt_scc_and_Gprime(G)
