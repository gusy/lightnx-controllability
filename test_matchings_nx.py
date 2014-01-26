import networkx as lightnx
from nose.tools import *
import matchings

#Epiloaded=False
#Gepi=None

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
        self.K3.add_edges_from([(0, 1), (1, 2), (0, 2)])
        #self.K4=cnlti(nx.complete_graph(4), first_label=1)
        #self.K5=cnlti(nx.complete_graph(5), first_label=1)
        #self.K10=cnlti(nx.complete_graph(10), first_label=1)
        #self.G=nx.Graph
    #    if not Epiloaded:
            #import urllib,gzip,StringIO
            #compr = StringIO.StringIO()
            #compr.write(urllib.urlopen(
            #"http://snap.stanford.edu/data/soc-Epinions1.txt.gz").read())
            #compr.seek(0)
            #dcom = gzip.GzipFile(fileobj=compr, mode='rb')
            #self.Gepi = lightnx.DiGraph()
            #for line in dcom:
                #if line[0]=="#":
                    #continue
                #nodes = map(int,line.split("\t"))
                #self.Gepi.add_edge(nodes[0],nodes[1])
            #Epiloaded=True
            #self.Gepi = Gepi

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
        assert_equal(sorted(bip['0+']), sorted(['1-','2-']))

    def test_matching(self):
        G = lightnx.DiGraph()
        G.add_edges_from([(1, 2), (2, 3), (3, 1), (1, 4), (1, 5), (1, 6)])
        matching = matchings.matching(G)
        assert_equal(self.isMatching(matching),True)
        assert_equal(3,len(matching))

    def test_matchings2(self):
        G = lightnx.DiGraph()
        G.add_edges_from([(1, 2), (2, 1), (2, 3), (3, 4), (4, 5), (5, 3), (5, 6)])
        G.add_node(7)
        matching = matchings.matching(G)
        assert_equal(self.isMatching(matching),True)
        assert_equal(5,len(matching))

    def test_matching_self_loop(self):
        G = lightnx.DiGraph()
        G.add_edges_from([(1, 1), (1, 2), (2, 2)])
        matching = matchings.matching(G)
        assert_equal(self.isMatching(matching),True)
        assert_equal(2,len(matching))
        assert_equal(sorted(matching),sorted([('2','2'),('1','1')]))

#    def no_test_epinions(self):
        #import urllib,gzip,StringIO
        #compr = StringIO.StringIO()
        #compr.write(urllib.urlopen(
        #"http://snap.stanford.edu/data/soc-Epinions1.txt.gz").read())
        #compr.seek(0)
        #dcom = gzip.GzipFile(fileobj=compr, mode='rb')
        #G = lightnx.DiGraph()
        #for line in dcom:
            #if line[0]=="#":
                #continue
            #nodes = map(int,line.split("\t"))
            #G.add_edge(nodes[0],nodes[1])
        #assert_equal(len(G.nodes()),75879) #http://www4.ncsu.edu/~qge2/Files/[2a]Controllability%20of%20complex%20networks.pdf
        #matching = matchings.matching(G)
        #assert_equal(self.isMatching(matching),True)
        #assert_equal(len(G.nodes())-41627,len(matching))
    def test_scc(self):
        G = self.K3
        sccs = matchings.strongly_connected_components(G)
        assert_equal(len(sccs),3)
    def test_non_top(self):
        G = lightnx.DiGraph()
        G.add_edges_from([(1,2),(2,1),(2,3),(3,4),(4,3),(5,4),(5,6),(6,5),(7,6)])
        sccs = matchings.strongly_connected_components(G)
        for scc in sccs:
            if matchings.is_non_top_linked(G,scc):
                assert_equal(sorted(scc) in [[1,2],[7]],True)
    def test_control_set(self):
        G = lightnx.DiGraph()
        G.add_edges_from([(1,2),(2,1),(2,3),(3,4),(4,3),(5,4),(5,6),(6,5),(7,6)])
        drivers = matchings.controller_set(G)
        assert_equal(set(['1','7']),drivers)
    def test_is_perfect_matchable(self):
        G = lightnx.DiGraph()
        G.add_edges_from([(1,2),(2,1),(2,3),(3,2)])
        sccs=matchings.strongly_connected_components(G)
        is_p_m=matchings.is_perfect_matchable(G,sccs[0])
        assert_equal(is_p_m,False)
        G= lightnx.DiGraph()
        G.add_edges_from([(1,2),(2,1),(2,3),(3,4),(4,3),(5,4),(5,6),(6,5)])
        sccs=matchings.strongly_connected_components(G)
        for scc in sccs:
            is_p_m=matchings.is_perfect_matchable(G,scc)
            assert_equal(is_p_m,True)

    def test_controllers_dilation(self):
        G = lightnx.DiGraph()
        G.add_edges_from([(1,2),(2,1),(2,3),(3,4),(4,3),(5,4),(5,6),(6,5),(7,6)])
        mm=matchings.matching(G)
        contr = matchings.controllers_dilation(mm,G.nodes())
        assert_equal(contr,set(['7']))

    def test_is_perfect_matchable(self):
        G1=lightnx.DiGraph()
        G1.add_edges_from([('A','B'),('B','A')])
        G2=lightnx.DiGraph()
        G2.add_edges_from([('A','B'),('B','A'),('A','C')])
        G3=lightnx.DiGraph()
        G3.add_edges_from([('C','C')])
        assert_equal(matchings.is_perfect_matchable(G1),True)
        assert_equal(matchings.is_perfect_matchable(G2),False)
        assert_equal(matchings.is_perfect_matchable(G3),True)



    def test_get_S_nt_rm_Gprime(self):
        G= lightnx.DiGraph()
        G.add_edges_from([(1,2),(2,1),(2,3),(3,4),(4,3),(5,4),(5,6),(6,5),(7,6),(7,7),(7,5)])
        scc_pm_nt,gprime = matchings.get_S_nt_rm_Gprime(G)
        assert_equals(len(scc_pm_nt),2)
        def check_results(scc_pm_nt):
            assert_equals(set(scc_pm_nt[0].graph.nodes()),set([1,2]))
            assert_equals(set(scc_pm_nt[1].graph.nodes()),set([7]))
            assert_equals(scc_pm_nt[0].outnodes,set([3]))
            assert_equals(set(scc_pm_nt[0].outlinks),set([(2,3)]))
            assert_equals(scc_pm_nt[1].outnodes,set([6,5]))
            assert_equals(set(scc_pm_nt[1].outlinks),set([(7,6),(7,5)]))

        if len(scc_pm_nt[0].graph.nodes())==2:
            check_results(scc_pm_nt)
        else:
            check_results(scc_pm_nt[1:0])
        assert_equals(set(gprime.nodes()),set([3,4,5,6]))
        assert_equals(set(gprime.predecessors(3)),set([4]))
        assert_equals(set(gprime.successors(3)),set([4]))


    def test_is_assignable_std(self):
        scenario = [
            [(1, 2), (2, 1), (2, 3), (4, 3), (5, 4), (5, 6), (6, 5), (7, 6), (7, 7), (7, 5)],
            [[2, 1], [7]],
            [[3], [6]]
        ]
        G = lightnx.DiGraph()
        G.add_edges_from(scenario[0])
        scc_pm_nt, Gprime = matchings.get_S_nt_rm_Gprime(G)
        assignable_sorted = map(sorted, scenario[1])
        msize = len(matchings.matching(Gprime))
        for scc in scc_pm_nt:
            back_edges = Gprime.edges()[:]
            if matchings.is_assignable(scc, Gprime, msize):
                try:
                    idx = assignable_sorted.index(sorted(scc.graph.nodes()))
                except:
                    idx = None
                aseert_equals = (sorted(back_edges) ,sorted(Gprime.edges()))
                assert_equals(idx is None, False)
                assert_equals(scc.assignable_points, set(scenario[2][idx]))



    #def test_control_set_epinions(self):
        #import urllib,gzip,StringIO
        #compr = StringIO.StringIO()
        #compr.write(urllib.urlopen(
        #"http://snap.stanford.edu/data/soc-Epinions1.txt.gz").read())
        #compr.seek(0)
        #dcom = gzip.GzipFile(fileobj=compr, mode='rb')
        #G = lightnx.DiGraph()
        #for line in dcom:
            #if line[0]=="#":
                #continue
            #nodes = map(int,line.split("\t"))
            #G.add_edge(nodes[0],nodes[1])
        #assert_equal(len(G.nodes()),75879) #http://www4.ncsu.edu/~qge2/Files/[2a]Controllability%20of%20complex%20networks.pdf
        #mm=matchings.matching(G)
        #contr = matchings.controller_set(G)
        #assert_equal(len(contr)>=41627,True)

