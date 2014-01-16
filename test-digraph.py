import digraph as lightnx
from nose.tools import *

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
        #self.P1=cnlti(nx.path_graph(1),first_label=1)
        #self.P3=cnlti(nx.path_graph(3),first_label=1)
        #self.P10=cnlti(nx.path_graph(10),first_label=1)
        #self.K1=cnlti(nx.complete_graph(1),first_label=1)
        self.K3 = lightnx.DiGraph()
        self.K3.add_edges([(0, 1),(1, 2), (0, 2)])
        #self.K4=cnlti(nx.complete_graph(4),first_label=1)
        #self.K5=cnlti(nx.complete_graph(5),first_label=1)
        #self.K10=cnlti(nx.complete_graph(10),first_label=1)
        #self.G=nx.Graph

    def test_has_successor(self):
        G = self.K3
        assert_equal(G.has_successor(0, 1), True)
        assert_equal(G.has_successor(0, -1), False)

    def test_successors(self):
        G = self.K3
        assert_equal(sorted(list(G.successors(0))), [1, 2])

    def test_successors_iter(self):
        G = self.K3
        assert_equal(sorted(G.successors_iter(0)), [1, 2])

    def test_has_predecesor(self):
        G = self.K3
        assert_equal(G.has_predecesor(1, 0), True)
        assert_equal(G.has_predecesor(0, -1), False)

    def test_predecesors(self):
        G = self.K3
        assert_equal(sorted(list(G.predecesors(2))), [0, 1])

    def test_predecesors_iter(self):
        G = self.K3
        assert_equal(sorted(G.predecesors_iter(2)), [0, 1])

    def test_add_remove_node(self):
        G=lightnx.DiGraph()
        G.add_node('A')
        assert_true('A' in G.nodes())
        G.remove_node('A')
        assert_false('A' in G.nodes())

    def test_add_edge(self):
        G=lightnx.DiGraph()
        assert_raises(TypeError,G.add_edge,'A')

        G.add_edge('A','B')     # testing add_edge()
        G.add_edge('A','B') # should fail silently
        assert_true(G.has_edge('A','B'))
        assert_false(G.has_edge('A','C'))
        assert_true(G.has_edge( *('A','B') ))
        if G.is_directed():
            assert_false(G.has_edge('B','A'))
        else:
            # G is undirected, so B->A is an edge
            assert_true(G.has_edge('B','A'))


        G.add_edge('A','C')  # test directedness
        G.add_edge('C','A')
        G.remove_edge('C','A')
        if G.is_directed():
            assert_true(G.has_edge('A','C'))
        else:
            assert_false(G.has_edge('A','C'))
        assert_false(G.has_edge('C','A'))

    def test_self_loop(self):
        G=lightnx.DiGraph()
        G.add_edge('A','A') # test self loops
        assert_true(G.has_edge('A','A'))
        G.remove_edge('A','A')
        G.add_edge('X','X')
        assert_true(G.has_node('X'))
        G.remove_node('X')
        G.add_edge('A','Z') # should add the node silently
        assert_true(G.has_node('Z'))

    def test_neighbors(self):
        G=lightnx.DiGraph()
        G.add_edges([('A', 'B'), ('A', 'C'), ('B', 'D'),
                          ('C', 'B'), ('C', 'D')])
        G.add_nodes('GJK')
        assert_equal(sorted(G.neighbors('A')),['B', 'C'])
        assert_equal(sorted(G.neighbors('G')),[])

    def read_from_nx(self)
        import networkx




