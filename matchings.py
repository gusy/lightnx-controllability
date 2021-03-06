from digraph import DiGraph
import collections
import random
from sets import Set
import itertools
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

class SCC():
    def __init__(self,subgraph):
        self.graph = subgraph #either a networkX.DiGraph or a lightnx.DiGraph
        self.outnodes = set([])
        self.outlinks = []

    def __contains__(self, node):
        if self.graph.has_node(node):
            return True
        return False


def get_S_nt_rm_Gprime(G):
    '''returns a list set of perfect matchable non top-linked strongly connected components of a graph
        returned objects of class "scc"
        returns also a subgraph o G' (the rest of the graph except for the S_nt_ru)
        Steps 1 and 2 in the paper
    '''
    sccs = strongly_connected_components(G)
    perfect_matchable_nt = []
    nodesOnGPrime = set(G.nodes())
    for scc in sccs:
        if is_non_top_linked(G, scc):
            #non_top_linked.append(scc)
            sccnt = SCC(G.subgraph(scc))
            if is_perfect_matchable(sccnt.graph):
                for node in scc:
                    nodesOnGPrime.remove(node)
                    for outnode in G.successors(node):
                        # NOT USING NEI!!! is not nx compliant
                        if outnode not in sccnt:
                            sccnt.outnodes.add(outnode)
                            sccnt.outlinks.append((node, outnode))
                perfect_matchable_nt.append(sccnt)
    Gprime = G.subgraph(nodesOnGPrime)
    return perfect_matchable_nt, Gprime


def matching_with_driver(G, node):
    return matching_with_drivers(G, [node])

def matching_with_drivers(G, nodes):
    cut_links = []
    #keep a copy of removed links in memory to be readded afterwards
    for node in nodes:
        p = G.predecessors(node)
        if hasattr(p, 'copy'):
            pres = p.copy()
        else:
            pres = p[:]
        for pre in pres:
            cut_links.append((pre, node))
            G.remove_edge(pre, node)
    m = matching(G)
    G.add_edges_from(cut_links)
    return m


def is_assignable(S, Gprime, msize):
    #print "msize", msize
    outnodes = S.outnodes
    assignable = False
    for outnode in outnodes:
        m = matching_with_driver(Gprime, outnode)
        if len(m) == msize:
            assignable = True
            if hasattr(S, 'assignable_points'):
                S.assignable_points.add(outnode)
            else:
                S.assignable_points = set([outnode])
    return assignable



def sets_combinations(set_list):
    combinations = [[i] for i in set_list[0]]
    for set_i in set_list[1:]:
        print set_i
        tempcomb = []
        for i in set(set_i):
            tempcomb += [c + [i] for c in combinations if i not in c]
        if tempcomb:
            combinations = tempcomb
    return combinations


def isCompatible(compatibleSCCs, S_assignable, Gprime, msize):
    outnodes_sccs = {}
    outnodes_sccs[0] = S_assignable.outnodes
    scc_index = 1
    compatible = False
    for scc in compatibleSCCs:
        outnodes_sccs[scc_index] = scc.outnodes
        scc_index += 1
    print outnodes_sccs.values()
    posible_out_configs = sets_combinations(outnodes_sccs.values())
    for out_config in posible_out_configs:
        if len(out_config) == (len(compatibleSCCs)+1):
            match_c = matching_with_drivers(Gprime, out_config)
            #print match_c, out_config
            if len(match_c) == msize:
                compatible = True
                break
    print compatible
    print posible_out_configs
    if compatible:
        compatibleSCCs.insert(0, S_assignable)
        print "sccs compatibles"
        for i in xrange(0, len(compatibleSCCs)):
            print compatibleSCCs[i].graph.nodes(),
            compatibleSCCs[i].comp_node = out_config[i]
    return compatible, compatibleSCCs


#def optimum_controller_set(G):
    #s_nt_rm, Gprime = get_S_nt_rm_Gprime(G)
    #assignables = []
    #mSize = len(matching(Gprime))
    #for scc in s_nt_rm:
        #if (is_assignable(scc, Gprime, mSize)):
            #assignables.append(scc)
    #compatibles = []
    #if len(assignables) == 1:
        #compatibles = assignables
    #elif len(assignables) > 1:
        #compatibles = [assignables[0]]
        #for scc in assignables[1:]:
            #if isCompatible(compatibles, scc, Gprime, mSize):
                #compatibles.append(scc)
    #return len(Gprime.nodes()) - mSize + len(s_nt_rm) - len(compatibles)

