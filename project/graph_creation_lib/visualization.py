import os
from os import listdir
from os.path import isfile, join
import pandas as pd
import sys 
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random
import csv
from collections import defaultdict
import matplotlib.pyplot as plt 
from sklearn.cluster import KMeans
import networkx as nx
from datetime import timedelta
from datetime import datetime
from pandas.tslib import Timestamp 
import math
from math import ceil
from collections import Counter
from itertools import groupby
from operator import itemgetter
import folium
from graph_creation_lib import pygmaps


class Visualizer(object):

    # class used for visualising the clustered dataframes on a folium interactive map
    # graph representation of the data is not implemented here
    # clustered data are saved in data/clusters

    def __init__(self, options):
        self.data = None
        self.graphs = None 
        self.options=options

    def read_data(self):
        options=self.options
        data ={}
        for cnt,fn in enumerate(os.listdir(options['datafolder'])):
            if os.path.isfile(os.path.join(options['datafolder'], fn)):
                inputfile = os.path.join(options['datafolder'], fn)
                if not fn.startswith('.'):
                    df = pd.read_csv(inputfile)
                    df['datetime'] = pd.to_datetime(df['datetime'])
                    data[fn]=df
        self.data = data
        return

    def visualize(self):
        for key, value in self.data.items():
            print('inside visualize')
            l = [tuple(x) for x in value[['lat', 'lon']].values]
            locations = []
            for i,j in zip(l, l[1:]):
                locations.append([i,j])
            
            if os.path.isfile(join(self.options['clusterfolder'], key)): # if clusterfile exists (clustering may give an empty dataframe in some cases)
                clusters = pd.read_csv(join(self.options['clusterfolder'], key))
                if not clusters.empty:
                    cl = [tuple(x) for x in clusters[['lat', 'lon']].values]
                    cluster_locations = []
                    for i,j in zip(cl, cl[1:]):
                        cluster_locations.append([i,j])            
                    cc = folium.MultiPolyLine(locations=cluster_locations, color='green', weight=5, opacity=10)
                ll = folium.MultiPolyLine(locations=locations, color='red', weight=5, opacity=10)
                mapa = folium.Map(location=[locations[0][0][0], locations[0][0][1]], zoom_start=14)
                mapa.add_children(ll)
                if not clusters.empty:
                    mapa.add_children(cc)
                folium_folder = self.options['folium_visualization']
                if not os.path.exists(folium_folder):
                    os.makedirs(folium_folder) 
                mapa.save(folium_folder + "/" + self.options['dataset'] + str(key)[:-4]+'.html')
                print('inside not_subsample branch')
        return 


    def visualize2(self):
        # visualize using markers instead of lines
        for key, value in self.data.items():
            l = np.array(value[['lat', 'lon']])
            mymap = pygmaps.maps(l[0][0], l[0][1], 14)
            for (i,j) in zip(l, l[1:]):
                [x1,x2]=[i[0], i[1]]
                [x3,x4]=[j[0], j[1]]
                lat1=float(x1)
                lon1=float(x2)
                lat2=float(x3)
                lon2=float(x4)
                mymap.addpoint(lat2,lon2)
                path=[(lat1,lon1),(lat2,lon2)]
            pygmaps_folder = self.options['pygmaps_visualization']
            if not os.path.exists(pygmaps_folder):
                os.makedirs(pygmaps_folder)
            mymap.draw(pygmaps_folder + '/' + self.options['dataset'] + str(key)+'.html')
        return mymap

