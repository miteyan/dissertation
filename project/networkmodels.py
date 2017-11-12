import glob
import json
import math
import os
from datetime import timedelta, datetime
from os import listdir
from os.path import join

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize

from timezone_converter import to_local_time


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
        #for key, value in data.iteritems():
        #    value = [f for f in value in len(f)>thres]
        #return data

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
        timesplit_data={}
        if (self.options['frequency']=='day'):
            for key, value in data.items():
                for k, group in value.groupby([value.set_index('datetime').index.year, value.set_index('datetime').index.week, value.set_index('datetime').index.day]):
                    if len(group.index)>20:
                        timesplit_data[str(key).replace(".","") + '_' + '_'.join(str(i) for i in k)] = group 
        elif (self.options['frequency']=='week'):
            for key, value in data.items():
                for k, group in value.groupby([value.set_index('datetime').index.year, value.set_index('datetime').index.week]):
                    if len(group.index)>50:
                        timesplit_data[str(key).replace(".", "") + '_' + '_'.join(str(i) for i in k)] = group 
        elif (self.options['frequency']=='year'):
            for key, value in data.items():
                #for k, group in value.groupby([value.set_index('datetime').index.year]):
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


class BeijingNetworks(NetworkModel):
    """ class for networks from the Geolife dataset """

    def __init__(self, options):
        super(BeijingNetworks, self).__init__('beijing', options)

    def _to_datetime(self, data):
        # concatenate date and time and return them into a datetime format
        return [datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in data['date'] + ' ' + data['time']]

    def preprocess(self, organize=None):
        # preprocess according to the requirements of the dataset
        data_dir = os.path.join(self.options['datafolder'], 'Data')
        print('data directory', str(data_dir))
        users_ids = self._get_immediate_subdirectories(data_dir)
        users_dirs = [data_dir + '/' + u for u in users_ids]
        users_files = [[join(self.options['datafolder']+'/Data/' + u + '/Trajectory', f)
                    for f in listdir(self.options['datafolder'] + '/Data/' + u + '/Trajectory') 
                    if 'plt' in (join(self.options['datafolder'] + '/Data/' + u + '/Trajectory', f))]
                    for u in users_ids ]
        data={}
        print(len(users_files))
        peruser_data = dict.fromkeys(users_ids)
        for (uif, uf) in zip(users_ids, users_files):
            print('user', uif)
            peruserdf=pd.DataFrame()
            cnt=0
            for f in uf:
                cnt+=1
                userdata = pd.read_csv(f, skiprows=6, sep=',', header=None)[[0,1,5,6]]
                userdata.columns =['lat', 'lon', 'date', 'time']
                userdata['datetime'] = self._to_datetime(userdata)
                userdata=userdata[['datetime', 'lat', 'lon']]
                data[str(uif)+'_'+str(cnt)]=userdata
                peruserdf = pd.concat([peruserdf, data[str(uif)+'_'+str(cnt)]])
            peruser_data[uif]=peruserdf
        print('data keys', peruser_data)       
        return peruser_data

    def _get_immediate_subdirectories(self, a_dir):
        return [name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name))]


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
        data = data.drop_duplicates().sort_values('datetime', ascending=True) # drop dublicates of the drows over the dataframe and order logs over time
        data_groups = data.groupby('user_id')
        data_dict = {}
        for user, group in data_groups:
            data_dict[user]=group[['datetime', 'lat', 'lon']]  
        return data_dict


class SeattleNetworks(NetworkModel):
    """ class for networks from the Seattle dataset """

    def __init__(self, options):
        super(SeattleNetworks, self).__init__('seattle', options)
        
    def _to_datetime(self, data):
        # concatenate date and time and return them into a datetime format
        return [datetime.strptime(d, '%m/%d/%Y %I:%M:%S %p') for d in data['date'] + ' ' + data['time']]

    def preprocess(self, organize=None):
        # preprocess according to the requirements of the dataset
        n_users=21
        data={}
        for cnt,fn in enumerate(os.listdir(self.options['datafolder'])):
            if os.path.isfile(os.path.join(self.options['datafolder'], fn)):
                inputfile = os.path.join(self.options['datafolder'], fn)
                if not fn.startswith('.'):
                    print(inputfile)
                    userdata = pd.read_csv(inputfile, sep="\t")
                    userdata.columns=['date', 'time', 'lat', 'lon']
                    if self.options['datetime']:
                        userdata['datetime'] = self._to_datetime(userdata)
                        userdata=userdata[['datetime', 'lat', 'lon']]
                    data[cnt]=userdata
        return data

class IosNetworks(NetworkModel):
    """ class for networks from the dataset collected by the iOS app """

    def __init__(self, options):
        super(IosNetworks, self).__init__('ios_app', options)

    def preprocess(self, organize=None):
        directory_name = self.options['datafolder']
        n_users = len(glob.glob(os.path.join(directory_name,'*.locdat')))
        data_dict={}
        for filename in glob.glob(os.path.join(directory_name,'*.locdat')):
            print('filename : ', filename)
            data = "["
            with open(filename, 'r') as json_data:
                for line in json_data:
                    if line[0] == '}':
                        line = '},'
                    elif line[0] == '[':
                        line = ''
                    elif line[0] == ']':
                        line = ''
                    data += line
                data = data[:-1]+']'
                data = data.replace("longtitude", "longitude")
                df=json_normalize(json.loads(data, strict=False))
            df['timestamp'] = pd.to_datetime(df['timestamp'],unit='s') 
            df = df[['timestamp', 'location.latitude', 'location.longitude']]
            df.columns = ['datetime', 'lat', 'lon']
            df = df.drop_duplicates().sort_values('datetime', ascending=True) # drop dublicates of the drows over the dataframe and order logs over time
            data_dict[filename.split('.')[0][-5:]]=df
        return data_dict
        


class AndroidNetworks(NetworkModel):
    """ class for networks from the Seattle dataset """

    def __init__(self, options):
        super(AndroidNetworks, self).__init__('android_app', options)
        
    def preprocess(self, organize=None):
        directory_name = self.options['datafolder']
        n_users = len(glob.glob(os.path.join(directory_name,'*.log')))
        data_dict={}
        for filename in glob.glob(os.path.join(directory_name,'*.log')):
            with open(filename, 'r') as json_file:
                json_data=[json.loads(line) for line in json_file]
                df = pd.DataFrame(json_normalize(json_data))
            df['timestamp'] = pd.to_datetime(df['timestamp'],unit='ms')
            df = df[['timestamp', 'location.latitude', 'location.longitude']]
            df.columns = ['datetime', 'lat', 'lon']
            df = df.drop_duplicates().sort_values('datetime', ascending=True) # drop dublicates of the drows over the dataframe and order logs over time
            print('file after preprocessing : ', df.head(n=10))
            data_dict[filename.split('/')[2][:5]]=df
        return data_dict

    