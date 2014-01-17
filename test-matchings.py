import digraph as lightnx
from nose.tools import *
import matchings


class TesterDigraph:
    def __init__(self):
        self.is_setup = False

    def tearDown(self):
        assert self.is_setup
        self.is_setup = False

    def setUp(self):
        assert not self.is_setup
        self.is_setup = True
        #self.null=nx.null_graph()
        #self.P1=cnlti(nx.path_graph(1), first_label=1)
        #self.P3=cnlti(nx.path_graph(3), first_label=1)
        #self.P10=cnlti(nx.path_graph(10), first_label=1)
        #self.K1=cnlti(nx.complete_graph(1), first_label=1)
        self.K3 = lightnx.DiGraph()
        self.K3.add_edges([(0, 1), (1, 2), (0, 2)])
        #self.K4=cnlti(nx.complete_graph(4), first_label=1)
        #self.K5=cnlti(nx.complete_graph(5), first_label=1)
        #self.K10=cnlti(nx.complete_graph(10), first_label=1)
        #self.G=nx.Graph

    def isMatching(self,edges):
        origins=set([])
        destinations=set([])
        for edge in edges:
            if edge[0] in origins:
                return False
            if edge[1] in destinations:
                return False
            origins.add(edge[0])
            destinations.add(edge[1])
        return True

    def test_bipartite(self):
        G = self.K3
        bip = matchings.getBipartite(G)
        print bip
        assert_equal(bip['0+'], set(['1-','2-']))

    def test_matching(self):
        G = lightnx.DiGraph()
        G.add_edges([(1, 2), (2, 3), (3, 1), (1, 4), (1, 5), (1, 6)])
        matching = matchings.matching(G)
        assert_equal(self.isMatching(matching),True)
        assert_equal(3,len(matching))

    def test_matchings2(self):
        G = lightnx.DiGraph()
        G.add_edges([(1, 2), (2, 1), (2, 3), (3, 4), (4, 5), (5, 3), (5, 6)])
        G.add_node(7)
        matching = matchings.matching(G)
        assert_equal(self.isMatching(matching),True)
        assert_equal(5,len(matching))

    def test_matching_self_loop(self):
        G = lightnx.DiGraph()
        G.add_edges([(1, 1), (1, 2), (2, 2)])
        matching = matchings.matching(G)
        assert_equal(self.isMatching(matching),True)
        assert_equal(2,len(matching))
        assert_equal(sorted(matching),sorted([('2','2'),('1','1')]))
