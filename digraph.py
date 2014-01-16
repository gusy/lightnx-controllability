from sets import Set


class DiGraph:
    nei = {}
    rev_nei = {}

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

    def add_edges(self, t):
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

    def predecesors(self, node):
        if node in self.rev_nei:
            return self.rev_nei[node]
        return set([])

    def has_predecesor(self, node, target):
        if node in self.rev_nei:
            if target in self.rev_nei[node]:
                return True
        return False

    def predecesors_iter(self, node):
        if node in self.rev_nei:
            return self.rev_nei[node].__iter__()

    def neighbors(self, node):
        return self.predecesors(node).union(self.successors(node))

    def has_edge(self, source, target):
        return self.has_successor(source, target)

    def remove_edge(self, source, target):
        if source in self.nei:
            self.nei[source].remove(target)
        if target in self.rev_nei:
            self.rev_nei[target].remove(source)

if __name__ == "__main__":
    d = DiGraph()
    d.add_node("hola")
    d.add_edge("hola", "adios")
    d.add_edges([("p", "q"), ("q", "r")])
    print d.nei
    print d.rev_nei
    print d.nodes()
    print "neighbors of q :", d.predecesors("q"), d.successors("q")
    print d.edges()
    d.del_node("adios")
    print d.nodes(), d.edges()
