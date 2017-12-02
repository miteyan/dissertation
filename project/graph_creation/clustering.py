import os
from os import listdir
from os.path import isfile, join
import pandas as pd
from pandas.tslib import Timestamp 
import sys 
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random
import csv
from collections import defaultdict, Counter 
import math
from math import ceil
from sklearn.cluster import KMeans
from datetime import timedelta, datetime 
from itertools import groupby
import operator
from operator import itemgetter
# auxiliary functions for clustering


def add_point_to_cluster(cl, point):
    cl['lat'], cl['lon'] = (cl['n_points']*cl['lat'] + point['lat'])/((1+cl['n_points'])*1.0), (cl['n_points']*cl['lon'] + point['lon'])/((1+cl['n_points'])*1.0) # update mean
    cl['n_points'] = cl['n_points']+1 # increase num of points in the cluster
    cl['datetime_last'] = point['datetime'] # update last datapoint in the cluster
    return cl

def square_grids(value, gridWidth=30, gridHeight=30, R=6.371*10**6):
    th0 = min(value['lat'])
    th1 = max(value['lat'])
    ph0 = min(value['lon'])
    ph1 = max(value['lon'])
    # if min/max latitude or longitude fall onto one another, slightly perturb them to define square grids without problems
    if (th0==th1) or (ph0==ph1):
        th0 = th0-1
        ph0 = ph0-1
    d1 = 2*math.pi*R*((ph1-ph0)*2*math.pi/360)/(2*math.pi)
    d2 = 2*math.pi*(R*math.sin(math.pi/2-ph1*2*math.pi/360))*((th1-th0)*2*math.pi/360)/(2*math.pi)
    d3 = 2*math.pi*(R*math.sin(math.pi/2-ph0*2*math.pi/360))*((th1-th0)*2*math.pi/360)/(2*math.pi)
    x_v = [0]*len(value['lat'])
    y_v = [0]*len(value['lon'])
    w1 = (value['lat']-ph0)/(ph1-ph0)
    w2 = (value['lon']-th0)/(th1-th0)
    y_v = w1*math.fabs(d3-d2)/2+w2*(d3*(1-w1)+d2*w1)
    x_v = w1*d1*math.sin(math.acos(math.fabs((d3-d2)/(2*d1))))
    value['y_v'] = w1*math.fabs(d3-d2)/2+w2*(d3*(1-w1)+d2*w1)
    value['x_v'] = w1*d1*math.sin(math.acos(math.fabs((d3-d2)/(2*d1))))
    #########################################################################
    xmin = min(x_v)
    xmax = max(x_v)
    ymin = min(y_v)
    ymax = max(y_v)
    gridWidth = float(gridWidth)
    gridHeight = float(gridHeight)
    # get rows
    rows = ceil((ymax-ymin)/gridHeight)
    # get columns
    cols = ceil((xmax-xmin)/gridWidth)
    value['x_id'] = (value['x_v']-xmin)//gridWidth + 0 # to convert it to +0 
    value['y_id'] = (value['y_v']-ymin)//gridWidth + 0 # to convert it to +0
    value['grid'] = list(zip(value.x_id, value.y_id))
    return value


class Cluster(object):

    def __init__(self):
        self.data = None
        self.options=None
        self.clusters=None

    # return the discovered clusters
    def get_clusters(data):
        return self.clusters

    # compute haversine distance between two pairs of coordinates
    def _distance(self, p1, p2, type='haversine'):
        if type=='haversine':
            R = 6371 # radius of earth
            lat_dist = math.radians(p2['lat'] - p1['lat'])
            lon_dist = math.radians(p2['lon']- p1['lon'])
            a = (math.sin(lat_dist/2))**2 + math.cos(math.radians(p1['lat']))*math.cos(math.radians(p2['lat']))*(math.sin(lon_dist/2))**2
            c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
            distance = (R*c*1000)**2 # to convert to meters
        return np.sqrt(distance)


    def read_csv_to_df(self, options):
        self.options=options
        data ={}
        for cnt,fn in enumerate(os.listdir(options['datafolder'])):
            #if cnt < 100:
                if os.path.isfile(os.path.join(options['datafolder'], fn)):
                    inputfile = os.path.join(options['datafolder'], fn)
                    if not fn.startswith('.'):
                        df = pd.read_csv(inputfile)
                        df['datetime'] = pd.to_datetime(df['datetime'])
                        data[fn]=df
        self.data = data
        return


    # in case we have the option to sample the initial dataframe
    # keep a certain percentage of the initial value
    # and change the option for the clusterfolder where the new clusters will be saved
    def undersample(self, f=0.30):
        self.options['clusterfolder'] = self.options['clusterfolder']+'_sampled'+str(int(f*100))
        self.options['folium_visualization'] = self.options['folium_visualization']+'_sampled'+str(int(f*100))
        self.options['pygmaps_visualization'] = self.options['pygmaps_visualization']+'_sampled'+str(int(f*100))
        self.options['datafolder'] = self.options['datafolder']+'_sampled'+str(int(f*100))
        for key, data, in self.data.items(): self.data[key] = data.sample(frac = f).sort_values(by=['datetime'])
        self.save_as_csv()
        return

    def save_as_csv(self):
        for key, value in self.data.items():
            csv_dir =self.options['datafolder']+'/'
            if not os.path.exists(csv_dir):
                os.makedirs(csv_dir) 
            value.to_csv(join(csv_dir, key), index=False)
        return 

    def time_based_cluster_places(self, time_param = timedelta(minutes=10), dist_param=100):
        stay_regions = {}
        options = self.options
        for key, data in self.data.items():
            # 1. Get stay points 
            places = []
            cl = dict(data.iloc[0]) 
            cl['datetime_last']=cl['datetime']
            cl['n_points']=0
            label=0
            ploc={}
            for idx, row in data.iterrows():
                row=dict(row)
                if self._distance(cl, row) < dist_param:
                    cl=add_point_to_cluster(cl, row)
                    ploc={}
                else:
                    if ploc:
                        if cl['datetime_last'] - cl['datetime']  > time_param:
                            places.append(cl)
                        cl={}
                        cl=ploc 
                        cl['datetime_last']=ploc['datetime']
                        cl['n_points']=1
                        if self._distance(cl, row) < dist_param:
                            cl=add_point_to_cluster(cl, row)
                            ploc={}
                        else:
                            ploc=row
                    else:
                        ploc=row

            # 2. Get stay regions
            places = pd.DataFrame(places)
            if not(places.empty) and places.shape[0]>1:
                places['sr']=-1
                cond=True    
                N=[(0,0),(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
                cnt=-1
                while (cond):
                    cnt+=1
                    l = [(k, len(g.index)) for (k,g) in square_grids(places, gridWidth=square_grid_length, gridHeight=square_grid_length).groupby(['grid', 'sr']) if k[1]==-1 ]
                    if (l):
                        g_i = max(l, key=itemgetter(1))[0][0]
                        for n in N:
                            k = tuple(sum(t) for t in zip(g_i,n))
                            k = tuple(map(operator.add, k, (+0.0, +0.0))) # remove -0.0 for the significant places ids
                            if not(places.loc[places['grid']==k, 'sr'].empty) and (max(places.loc[places['grid']==k, 'sr'])==-1):
                                places.loc[places['grid']==k, 'sr']=cnt
                    else:
                        cond=False
                merg_cl_seq = places.copy()
                merg_cl_seq['lat'] = merg_cl_seq['lat']*merg_cl_seq['n_points']/(merg_cl_seq.groupby('sr').n_points.transform('sum'))
                merg_cl_seq['lat'] = merg_cl_seq.groupby('sr').lat.transform('sum')
                merg_cl_seq['lon'] = merg_cl_seq['lon']*merg_cl_seq['n_points']/(merg_cl_seq.groupby('sr').n_points.transform('sum'))
                merg_cl_seq['lon'] = merg_cl_seq.groupby('sr').lon.transform('sum')
                stay_regions[key] = merg_cl_seq
                csv_dir =self.options['clusterfolder']+'/'
                if not os.path.exists(csv_dir):
                    os.makedirs(csv_dir) 
                merg_cl_seq.to_csv(join(csv_dir, key ))
        self.clusters = stay_regions 
        return stay_regions



    def idiap_time_based_cluster_places(self, time_param = timedelta(minutes=10), dist_param=100, square_grid_length=30):
        stay_regions = {}
        options = self.options
        for key, data in self.data.items():
            print('trajectory key : ', key)

            # 1. Get stay points 
            places = []
            cl = dict(data.iloc[0]) 
            cl['datetime_last']=cl['datetime']
            cl['n_points']=0
            label=0
            ploc={}
            for idx, row in data.iterrows():
                row=dict(row)
                if self._distance(cl, row) < dist_param:
                    cl=add_point_to_cluster(cl, row)
                    ploc={}
                else:
                    if ploc:
                        if cl['datetime_last'] - cl['datetime']  > time_param:
                            places.append(cl)
                        cl={}; cl=ploc; 
                        cl['datetime_last']=ploc['datetime']
                        cl['n_points']=1
                        if self._distance(cl, row) < dist_param:
                            cl=add_point_to_cluster(cl, row)
                            ploc={}
                        else:
                            ploc=row
                    else:
                        ploc=row

            # 2. Get stay regions
            places = pd.DataFrame(places)
            if not(places.empty) and places.shape[0]>1:
                places['sr']=-1
                cond=True    
                N=[(0,0),(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1),(-2,2),(-2,1),(-2,0),(-2,-1),(-2,-2),(-1,2),(0,2),(1,2),(2,2),(2,1),(2,0),(2,-1),(2,-2),(1,-2),(0,-2),(-1,-2)] # 5x5 grid as proposed in Gatica-Perez et al
                cnt=-1
                while (cond):
                    cnt+=1
                    l = [(k, len(g.index)) for (k,g) in square_grids(places).groupby(['grid', 'sr']) if k[1]==-1 ]
                    if (l):
                        g_i = max(l, key=itemgetter(1))[0][0]
                        # optimize with respect to the number of stay points in the cluster we make
                        max_sum_grid_points=-1;idx=0;
                        for (i, _n) in enumerate(N):
                            sum_grid_points=0
                            NewN = [map(operator.add, _n, n) for n in N]
                            for n in NewN:
                                k = tuple(sum(t) for t in zip(g_i,n))
                                k = tuple(map(operator.add, k, (+0.0, +0.0))) # remove -0.0 for the significant places ids
                                if not(places.loc[places['grid']==k, 'sr'].empty) and (max(places.loc[places['grid']==k, 'sr'])==-1):
                                    sum_grid_points +=len(places.loc[places['grid']==k, 'sr'])
                            if sum_grid_points > max_sum_grid_points:
                                idx = i # index of optimal permutaion with respect to 
                                max_sum_grid_points = sum_grid_points
                        # print("max grid points : ", max_sum_grid_points)
                        NewN = [map(operator.add, N[idx], n) for n in N]
                        for n in NewN:
                            k = tuple(sum(t) for t in zip(g_i,n))
                            k = tuple(map(operator.add, k, (+0.0, +0.0))) # remove -0.0 for the significant places ids
                            if not(places.loc[places['grid']==k, 'sr'].empty) and (max(places.loc[places['grid']==k, 'sr'])==-1):
                                places.loc[places['grid']==k, 'sr']=cnt
                    else:
                        cond=False
                merg_cl_seq = places.copy()
                merg_cl_seq['lat'] = merg_cl_seq['lat']*merg_cl_seq['n_points']/(merg_cl_seq.groupby('sr').n_points.transform('sum'))
                merg_cl_seq['lat'] = merg_cl_seq.groupby('sr').lat.transform('sum')
                merg_cl_seq['lon'] = merg_cl_seq['lon']*merg_cl_seq['n_points']/(merg_cl_seq.groupby('sr').n_points.transform('sum'))
                merg_cl_seq['lon'] = merg_cl_seq.groupby('sr').lon.transform('sum')
                stay_regions[key] = merg_cl_seq
                csv_dir =self.options['clusterfolder']+'/'
                if not os.path.exists(csv_dir):
                    os.makedirs(csv_dir) 
                merg_cl_seq.to_csv(join(csv_dir, key ))
        self.clusters = stay_regions 
        return stay_regions