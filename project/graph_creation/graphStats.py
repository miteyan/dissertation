import time
import importlib
from graph_creation.visualization import Visualizer
from graph_creation.grid import *
from eda import *
# from clustering import Cluster
from graph_creation.sna import SNA

# code to read the data from hdf5 format
# and parse them into networkx graphs

if __name__ == '__main__':

    optionsList = [
        # {'datafolder':'../mdc_data/year',  'clusterfolder':'../mdc_data/yearclusters', 'dataset':'lausanne', 'datetime':True, 'clustering':True, 'zoom_start':15, 'node_features':False, 'frequency':'year'},\
        # {'datafolder': '../graph_creation/full_data', 'clusterfolder': '../graph_creation/month_edge_lists',
        #  'dataset': 'full_lausanne', 'datetime': True, 'clustering': True, 'zoom_start': 15, 'node_features': True,
        #  'frequency': 'month'},
        {'datafolder': './full_data', 'clusterfolder': './month_clusters', 'dataset': 'lausanne',
         'datetime': True, 'clustering': True, 'zoom_start': 15, 'node_features': False, 'frequency': 'year'}, \
        # {'datafolder':'../mdc_data/year',  'clusterfolder':'../mdc_data/yearclusters', 'dataset':'full_lausanne', 'datetime':True, 'clustering':True, 'zoom_start':15, 'node_features':False, 'frequency':'year'},\
    ]

    start = time.time()
    for options in optionsList:
        vis = Visualizer(options)
        print("Visualizer")
        vis.read_data()
        print("read data")
        nets = SNA(vis)
        print("nets sna")
        clusters = nets.read_clusters()
        print('read clusters')
        if options['node_features']:
            nets.parse_into_dn_with_node_features(clusters)
            nets.edgeList_to_txt_from_gexf_with_node_features()
        else:
            nets.parse_into_dn(clusters)
            nets.edgeList_to_txt()
