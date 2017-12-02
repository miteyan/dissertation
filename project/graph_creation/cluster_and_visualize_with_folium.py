import time
import importlib
# from visualization import Visualizer
from graph_creation.clustering import Cluster
from joblib import Parallel, delayed

# code to read the data from hdf5 format
# and parse them into networkx graphs

if __name__ == '__main__':
    optionsList = [
        {'datafolder': '/var/storage/miteyan/Dissertation/project/graph_creation/full_data',
         'clusterfolder': './month_clusters', 'dataset': 'full_lausanne', 'datetime': True,
         'clustering': True,
         'zoom_start': 15, 'folium_visualization': 'yearfolium_visualization',
         'pygmaps_visualization': 'yearpygmaps_visualization'},
    ]

    start = time.time()

    def cluster_data(options):
        clus = Cluster()
        print('read csv to df')
        clus.read_csv_to_df(options)
        print('starting spatiotemporal clustering')
        clus.idiap_time_based_cluster_places()

    # vis = Visualizer(options)
    # print('read data, i.e. points and clusters')
    # vis.read_data()
    # vis.visualize()
    # vis.visualize2()

    Parallel(n_jobs=-1)(map(delayed(cluster_data), optionsList))
    end = time.time()
    print('finished in ', end - start)
