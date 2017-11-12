import time

# from visualization import Visualizer
from Clustering import Cluster
from joblib import Parallel, delayed

# code to read the data from hdf5 format
# and parse them into networkx graphs

if __name__ == '__main__':
    optionsList = [
        # {'datafolder':'data/Seattle/year', 'clusterfolder':'data/Seattle/yearclusters', 'dataset':'Seattle', 'datetime':True, 'clustering':True, 'zoom_start':17, 'folium_visualization':'yearfolium_visualization', 'pygmaps_visualization':'yearpygmaps_visualization'},
        # {'datafolder':'data/Geolife_Trajectories_1.3/year', 'clusterfolder':'data/Geolife_Trajectories_1.3/yearclusters', 'dataset':'Beijing', 'datetime':True, 'clustering':True, 'zoom_start':17, 'folium_visualization':'yearfolium_visualization', 'pygmaps_visualization':'yearpygmaps_visualization'},\
        # {'datafolder':'data/ios_app_data/year', 'clusterfolder':'data/ios_app_data/yearclusters', 'dataset':'ios_app', 'datetime':True, 'clustering':True, 'zoom_start':15, 'folium_visualization':'yearfolium_visualization', 'pygmaps_visualization':'yearpygmaps_visualization'},\
        # {'datafolder':'data/android_app_data/year', 'clusterfolder':'data/android_app_data/yearclusters', 'dataset':'android_app', 'datetime':True, 'clustering':True, 'zoom_start':15, 'folium_visualization':'yearfolium_visualization', 'pygmaps_visualization':'yearpygmaps_visualization'},\
        {'datafolder': '../mdc_data/year', 'clusterfolder': '../mdc_data/yearclusters', 'dataset': 'lausanne',
         'datetime': True, 'clustering': True, 'zoom_start': 15, 'folium_visualization': 'yearfolium_visualization',
         'pygmaps_visualization': 'yearpygmaps_visualization'},
		# {'datafolder':'../mdc_data/year', 'clusterfolder':'../mdc_data/yearclusters', 'dataset':'full_lausanne', 'datetime':True, 'clustering':True, 'zoom_start':15, 'folium_visualization':'yearfolium_visualization', 'pygmaps_visualization':'yearpygmaps_visualization'},\
        # {'datafolder':'../mdc_data/week',  'clusterfolder':'../mdc_data/weekclusters', 'dataset':'lausanne', 'datetime':True, 'clustering':True, 'zoom_start':15, 'folium_visualization':'yearfolium_visualization', 'pygmaps_visualization':'yearpygmaps_visualization'},\
        # {'datafolder':'../mdc_data/week', 'clusterfolder':'../mdc_data/weekclusters', 'dataset':'full_lausanne', 'datetime':True, 'clustering':True, 'zoom_start':15, 'folium_visualization':'yearfolium_visualization', 'pygmaps_visualization':'yearpygmaps_visualization'},\
        #  {'datafolder':'../mdc_data/day',  'clusterfolder':'../mdc_data/dayclusters', 'dataset':'lausanne', 'datetime':True, 'clustering':True, 'zoom_start':15, 'folium_visualization':'yearfolium_visualization', 'pygmaps_visualization':'yearpygmaps_visualization'},\
        # {'datafolder':'../mdc_data/day', 'clusterfolder':'../mdc_data/dayclusters', 'dataset':'full_lausanne', 'datetime':True, 'clustering':True, 'zoom_start':15, 'folium_visualization':'yearfolium_visualization', 'pygmaps_visualization':'yearpygmaps_visualization'},\
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
