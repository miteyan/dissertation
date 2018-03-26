import math
import os
from datetime import timedelta, datetime
from os.path import join

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from graph_creation_lib.timezone_converter import to_local_time


class NetworkModel(object):

    """ superclass for each dataset's networks"""
    def __init__(self, network_name, options):
        self.network_name = network_name
        self.options=options

    # removed to grid.py    
    def remove_short_trajectories(self, data, thres=20):
        for key, value in data.items():
            value = [f for f in value if len(f)>thres]
        return data

    # removed to grid.py
    def check_range_latlon(self, data, minlat=-90, maxlat=90, minlon=-180, maxlon=180):
        for key, value in data.items():
            value=value[(value.lat>minlat) & (value.lat<maxlat) & (value.lon>minlon) & (value.lon<maxlon)]
        return data 

    def eda(self, data):
        # exploratory data analysis, visualisation etc. 
        for key, value in data.items():
            plt.scatter(value['lat'], value['lon'])
            plt.show()        
        return

    # compute haversine distance between two pairs of coordinates
    def _distance(self, p1, p2, type='haversine'):
        if type=='haversine':
            R = 6371 # radius of earth
            lat_dist = math.radians(p2['lat'] - p1['lat'])
            lon_dist = math.radians(p2['lon']- p2['lon'])
            a = (math.sin(lat_dist/2))**2 + math.cos(math.radians(p1['lat']))*math.cos(math.radians(p2['lat']))*(math.sin(lon_dist/2))**2
            c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
            distance = (R*c*1000)**2 # to convert to meters
        return np.sqrt(distance)

    def convert_to_local_time(self, data):
        for key, value in data.items():
            if key is not None and value is not None:
                td=to_local_time(coords = value.iloc[0][['lat', 'lon']])['time_difference']
                value['datetime']=value['datetime'] + timedelta(hours=td)
            # print ('key ', key, 'value ', value.head(n=10))
        return data 

    def parse_into_wdn(self, data):
    # parse into weighted directed network 
        for key, value in data.items():
            adj_list = zip(value['labels'], value['labels'][1:])
            H=nx.DiGraph()
            H.add_edges_from(adj_list[:])
            nx.draw(H)
            # plt.show()
        return         

    def parse_into_udn(self, data):
    # parse into unweighted directed network 
        for key, value in data.items():
            adj_list = zip(value['labels'], value['labels'][1:])
            H=nx.DiGraph()
            H.add_edges_from(adj_list[:], weight=1)
            for i, n in enumerate(H.nodes()):
                H.nodes()[i]['weight'] = list(value['labels']).count(n)
        return 

    def split_over_time(self, data):
        """

        :type data: object
        """
        timesplit_data={}
        if self.options['frequency'] == 'day':
            for key, value in data.items():
                for k, group in value.groupby([value.set_index('datetime').index.year, value.set_index('datetime').index.week, value.set_index('datetime').index.day]):
                    if len(group.index)>20:
                        timesplit_data[str(key).replace(".","") + '_' + '_'.join(str(i) for i in k)] = group
        elif self.options['frequency'] == 'week':
            for key, value in data.items():
                for k, group in value.groupby([value.set_index('datetime').index.year, value.set_index('datetime').index.week]):
                    if len(group.index)>50:
                        timesplit_data[str(key).replace(".", "") + '_' + '_'.join(str(i) for i in k)] = group
        elif self.options['frequency'] == 'month':
            for key, value in data.items():
                print(key, "\n")
                print(value)
                for k, group in value.groupby(
                        [value.set_index('datetime').index.year, value.set_index('datetime').index.week]):
                    if len(group.index) > 50:
                        timesplit_data[str(key).replace(".", "") + '_' + '_'.join(str(i) for i in k)] = group
        elif self.options['frequency'] == 'year':
            for key, value in data.items():
                # for k, group in value.groupby([value.set_index('datetime').index.year]):
                if len(value.index)>50:
                    timesplit_data[str(key).replace(".", "") ] = value

        return timesplit_data

    def save_as_csv(self, data):
        for key, value in data.items():
            csv_dir =self.options['datafolder']+'/'+self.options['frequency']+'/'
            if not os.path.exists(csv_dir):
                os.makedirs(csv_dir) 
            value.to_csv(join(csv_dir, key+'.csv'), index=False)
        return 

    def hist_dt(self, data):
        for key, value in data.items():
            dts = [x.total_seconds() for x in value['datetime'].diff()][1:]
            plt.hist(dts, bins=50)
        return



class LausanneNetworks(NetworkModel):
    """ class for networks from the Nokia MDC dataset """

    def __init__(self, options):
        super(LausanneNetworks, self).__init__('lausanne', options)

    def _to_datetime(self, data):
        # return the timestamps into a datetime format
        return [datetime.fromtimestamp(d) for d in data['datetime']]

    def preprocess(self, organize=None):
        # preprocess according to the requirements of the dataset
        datafile = os.path.join(self.options['datafolder'], 'nokia_data_gps.csv')
        data=pd.read_csv(datafile)
        data.columns = ['user_id', 'datetime', 'lon', 'lat']
        data['datetime']=self._to_datetime(data)
        data = data.drop_duplicates().sort_values('datetime', ascending=True) # drop dublicates of the drows over the dataframe and order logs over time
        data_groups = data.groupby('user_id')
        data_dict ={}
        for user, group in data_groups:
            data_dict[user]=group[['datetime', 'lat', 'lon']]  
        return data_dict

class fullLausanneNetworks(NetworkModel):
    """ class for networks from the Nokia MDC dataset  (combined gps and wlan) """

    def __init__(self, options):
        super(fullLausanneNetworks, self).__init__('fulllausanne', options)

    def _to_datetime(self, data):
        # return the timestamps into a datetime format
        return [datetime(1970, 1, 1) + timedelta(seconds=d) for d in data['datetime']]

    def preprocess(self, organize=None):
        # preprocess according to the requirements of the dataset
        datafile = os.path.join(self.options['datafolder'], 'nokia_data_full.csv')
        data=pd.read_csv(datafile)
        data.columns = ['user_id', 'datetime', 'lon', 'lat']
        print('datashape : ', data.shape[0])
        data.dropna(inplace =True)     #drop all rows that have any NaN values
        print('datashape after removal of nans : ', data.shape[0])
        data['datetime']=self._to_datetime(data.head(n=data.shape[0]))
        print('to date time')
        data = data.drop_duplicates().sort_values('datetime', ascending=True) # drop dublicates of the drows over the dataframe and order logs over time
        print('sorted')
        data_groups = data.groupby('user_id')
        data_dict = {}
        for user, group in data_groups:
            data_dict[user]=group[['datetime', 'lat', 'lon']]  
        return data_dict
