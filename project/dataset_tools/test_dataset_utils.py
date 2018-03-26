from unittest import TestCase
import dataset_tools.dataset_utils as du
import networkx as nx
class test_dataset_utils(TestCase):
    foo = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6}

    def test_get_mean_variance(self):
        mean, var = du.get_mean_variance(test_dataset_utils.foo)
        print(mean)
        print(var)
        assert mean == 3.5
        assert var == 2.916666666666666

    def test_get_min_max(self):
        min, max = du.get_min_max(test_dataset_utils.foo)
        assert min == 1
        assert max == 6


    def test_get_features(self):
        G = nx.Graph()
        G.add_nodes_from([1,10])
        G.add_edges_from([(1, 2), (1, 3),(1, 4), (1, 5),(1, 6), (1, 7),(1, 8), (1, 9),(10, 2), (10, 3),(10, 2), (10, 3),(10, 2), (10, 3),
                          (3,4),(4,6),(5,6),(7,8),(9,8),(2,6),(5,1), (7,2),(6,3),(5,2),(7,9),(3,9)])
        features = du.get_features(0,G)
        featuresTrue = "0	10	21	8	0.4666666666666667	3	2	3	8	2.2	0.15999999999999925	1.5555555555555556	0.6126190476190476	0.09702046485260768	0.06944444444444445	0.008722350823045262	1.4	0.4800000000000002	0	3	0.07407407407407407	0.008722350823045262	0.06944444444444445	0.008722350823045262	0.1	0.0011165036793561456\n"
        assert features == featuresTrue
