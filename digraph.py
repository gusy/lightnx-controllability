from sets import Set


class DiGraph(object):
    def __init__(self):
        self.nei = {}
        self.rev_nei = {}
        return
    def is_directed(self):
        return True

    def add_node(self, node):
        self.nei[node] = Set([])
        self.rev_nei[node] = Set([])

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    def add_edge(self, source,  target):
        if source not in self.nei:
            self.add_node(source)
        if target not in self.nei:
            self.add_node(target)
        self.nei[source].add(target)
        self.rev_nei[target].add(source)

    def add_edges_from(self, t):
        for tup in t:
            self.add_edge(tup[0], tup[1])
    def nodes(self):
        return list(Set(self.nei.keys() + self.rev_nei.keys()))

    def has_node(self, node):
        if (node in self.nei) or (node in self.rev_nei):
            return True
        return False

    #NOT FAST, try to avoid
    def edges_iter(self):
        a = []
        for src in self.nei:
            for tgt in self.nei[src]:
                a.append((src, tgt))
        return a.__iter__()

    #NOT FAST, try to avoid
    def edges(self):
        a = []
        for src in self.nei:
            for tgt in self.nei[src]:
                a.append((src, tgt))
        return a

    def remove_node(self, node):
        neis = self.nei.pop(node, [])
        for n in neis:
            self.rev_nei[n].remove(node)
        neis = self.rev_nei.pop(node, [])
        for n in neis:
            self.nei[n].remove(node)

    def successors(self, node):
        if node in self.nei:
            return self.nei[node]
        return set([])

    def has_successor(self, node, target):
        if node in self.nei:
            if target in self.nei[node]:
                return True
        return False

    def successors_iter(self, node):
        if node in self.nei:
            return self.nei[node].__iter__()

    def predecessors(self, node):
        if node in self.rev_nei:
            return self.rev_nei[node]
        return set([])

    def has_predecesor(self, node, target):
        if node in self.rev_nei:
            if target in self.rev_nei[node]:
                return True
        return False

    def predecessors_iter(self, node):
        if node in self.rev_nei:
            return self.rev_nei[node].__iter__()

    def neighbors(self, node):
        return self.predecessors(node).union(self.successors(node))

    def has_edge(self, source, target):
        return self.has_successor(source, target)

    def remove_edge(self, source, target):
        if source in self.nei:
            self.nei[source].remove(target)
        if target in self.rev_nei:
            self.rev_nei[target].remove(source)

    def subgraph(self, nbunch):
        """Return the subgraph induced on nodes in nbunch.

        The induced subgraph of the graph contains the nodes in nbunch
        and the edges between those nodes.

        Parameters
        ----------
        nbunch : list, iterable
        A container of nodes which will be iterated through once.

        Returns
        -------
        G : Graph
        A subgraph of the graph with the same edge attributes.

        Notes
        -----
        The graph, edge or node attributes just point to the original graph.
        So changes to the node or edge structure will not be reflected in
        the original graph while changes to the attributes will.

        To create a subgraph with its own copy of the edge/node attributes use:
        nx.Graph(G.subgraph(nbunch))

        If edge attributes are containers, a deep copy can be obtained using:
        G.subgraph(nbunch).copy()

        For an inplace reduction of a graph to a subgraph you can remove nodes:
        G.remove_nodes_from([ n in G if n not in set(nbunch)])

        Examples
        --------
        >>> G = nx.Graph() # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> G.add_path([0,1,2,3])
        >>> H = G.subgraph([0,1,2])
        >>> H.edges()
        [(0, 1), (1, 2)]
        """
        bunch =nbunch# self.nbunch_iter(nbunch)
        # create new graph and copy subgraph into it
        H = self.__class__()
        # copy node and attribute dictionaries
        for n in bunch:
           # print n
            H.nei[n] = Set([])
            for n_i in self.nei[n]:
                if n_i in bunch:
                    if n_i not in H.rev_nei:
                        H.rev_nei[n_i] = Set([])
                    H.nei[n].add(n_i)
                    H.rev_nei[n_i] = Set([])
                    H.rev_nei[n_i].add(n)
        return H

    def nbunch_iter(self, nbunch=None):
        """Return an iterator of nodes contained in nbunch that are
        also in the graph.

        The nodes in nbunch are checked for membership in the graph
        and if not are silently ignored.

        Parameters
        ----------
        nbunch : iterable container, optional (default=all nodes)
        A container of nodes. The container will be iterated
        through once.

        Returns
        -------
        niter : iterator
        An iterator over nodes in nbunch that are also in the graph.
        If nbunch is None, iterate over all nodes in the graph.

        Raises
        ------
        NetworkXError
        If nbunch is not a node or or sequence of nodes.
        If a node in nbunch is not hashable.

        See Also
        --------
        Graph.__iter__

        Notes
        -----
        When nbunch is an iterator, the returned iterator yields values
        directly from nbunch, becoming exhausted when nbunch is exhausted.

        To test whether nbunch is a single node, one can use
        "if nbunch in self:", even after processing with this routine.

        If nbunch is not a node or a (possibly empty) sequence/iterator
        or None, a NetworkXError is raised. Also, if any object in
        nbunch is not hashable, a NetworkXError is raised.
        """
        if nbunch is None: # include all nodes via iterator
            bunch = iter(self.nodes())
        elif not hasattr(nbunch, '__iter__'):
            if ((nbunch in self.nei) or (nbunch in self.rev_nei)): # if nbunch is a single node
                bunch = iter([nbunch])
            else:
                bunch = iter([])
        else: # if nbunch is a sequence of nodes
            def bunch_iter(nlist,adj):
                for n in nlist:
                    if n in adj:
                        yield n
            bunch = bunch_iter(nbunch,Set(self.nei.keys() + self.rev_nei.keys()))
        return bunch

if __name__ == "__main__":
    d = DiGraph()
    d.add_node("hola")
    d.add_edge("hola", "adios")
    d.add_edges_from([("p", "q"), ("q", "r")])
    print d.nei
    print d.rev_nei
    print d.nodes()
    print "neighbors of q :", d.predecessors("q"), d.successors("q")
    print d.edges()
    d.del_node("adios")
    print d.nodes(), d.edges()
