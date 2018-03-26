import time
import importlib
# from visualization import Visualizer
from graph_creation_lib.clustering import Cluster
from joblib import Parallel, delayed

# code to read the data from hdf5 format
# and parse them into networkx graphs

# STEP 2 takes each users time split data to clustered data (3) which is turned to edge data (4).

if __name__ == '__main__':
    optionsList = [
        {'datafolder': '/var/storage/miteyan/Dissertation/project/graph_creation_lib/full_data',
         'clusterfolder': './month_clusters', 'dataset': 'full_lausanne', 'datetime': True,
         'clustering': True,
         'zoom_start': 15, 'folium_visualization': 'yearfolium_visualization',
         'pygmaps_visualization': 'yearpygmaps_visualization'},
        # {'datafolder': '/var/storage/sandra/mdc_analysis/mdc_data/full_lausanne/nkWeek/week',
        #  'clusterfolder': './week_clusters', 'dataset': 'full_lausanne', 'datetime': True,
        #  'clustering': True,
        #  'zoom_start': 15, 'folium_visualization': 'yearfolium_visualization',
        #  'pygmaps_visualization': 'yearpygmaps_visualization'},
    ]

    start = time.time()

    def cluster_data(options):
        clus = Cluster()
        print('read csv to df')
        clus.read_csv_to_df(options)
        print('starting spatiotemporal clustering')
        clus.idiap_time_based_cluster_places()

    Parallel(n_jobs=-1)(map(delayed(cluster_data), optionsList))
    end = time.time()
    print('finished in ', end - start)
