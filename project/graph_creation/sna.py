import os
from collections import Counter
from os.path import join

import networkx as nx
import pandas as pd


class SNA(object):

    def __init__(self, viz):
        self.data =viz.data
        self.graphs = None 
        self.options=viz.options
        self.graphfolder = './month_graphs'
        self.edgefolder = './month_edge_lists/'

    def edgeList_to_txt(self):
        graphfolder = self.graphfolder
        edgefolder =  self.edgefolder
        print('graphfolder {0}'.format(graphfolder))
        if not os.path.exists(self.graphfolder):
            os.makedirs(self.graphfolder)
        for cnt,fn in enumerate(os.listdir(graphfolder)):
            if os.path.isfile(os.path.join(graphfolder, fn)):
                inputfile = os.path.join(graphfolder, fn)
                print(inputfile)
                if not fn.startswith('.'):
                    g = nx.read_gexf(inputfile)
                    print('g edges : ', g.edges(data=True), '\n\n\n')
                    g = nx.convert_node_labels_to_integers(g)
                    nx.write_weighted_edgelist(g, edgefolder +"/%s" %(fn.split('.')[0]))
        return


    def edgeList_to_txt_from_gexf_with_node_features(self):
        print('graphs with node features ')
        graphfolder = self.graphfolder
        edgefolder = self.edgefolder
        for cnt,fn in enumerate(os.listdir(graphfolder)):
            if os.path.isfile(os.path.join(graphfolder, fn)):
                inputfile = os.path.join(graphfolder, fn)
                if not fn.startswith('.'):
                    g = nx.read_gexf(inputfile)
                    g = nx.convert_node_labels_to_integers(g)
                    nx.write_weighted_edgelist(g, edgefolder + "/%s" %(fn.split('.')[0]))
        return


    def parse_into_dn(self, clusters):
    # parse into directed network (networkx)
        Graphs={}
        for key, value in clusters.items():
            if not value.empty and value.shape[0]>1:
                print("D")
                adj_list = zip(value['grid'], value['grid'][1:])
                adj_list_cnts = [(v[0], v[1], w) for v, w in Counter(adj_list).items()]
                H=nx.DiGraph()
                H.add_weighted_edges_from(adj_list_cnts)
                nx.set_node_attributes(H, 'weight', 0)
                H = nx.convert_node_labels_to_integers(H)
                self.graphfolder = "graphs_" + self.options['frequency']
                self.edgefolder = "edgelists_" + self.options['frequency']
                print('inside graphfolder')
                if not os.path.exists(self.graphfolder):
                    os.makedirs(self.graphfolder)
                if not os.path.exists(self.edgefolder):
                    os.makedirs(self.edgefolder)
                graph_filename = self.graphfolder + "/" + ''.join(key.split(".")[:-1]) + ".gexf"
                nx.write_gexf(H, graph_filename)
                Graphs[key]=H
            else:
                print("nothing")
        self.graphs= Graphs
        return 


    def parse_into_dn_split_in_two_by_length(self, clusters):
    # parse into directed network (networkx)
        GraphsTrain={}; GraphsTest={};
        for key, value in clusters.items():
            value_train = value.head(n=int(round(len(clusters)/2)))
            value_test = value.tail(n=int(round(len(clusters)/2)))
            #print(value.head(n=10))
            #print(value.tail(n=10))
            #print(value.shape, value_train.shape, value_test.shape)

            if not value_train.empty and value_train.shape[0]>1 and not value_test.empty and value_test.shape[0]>1: 
                adj_list = zip(value_train['grid'], value_train['grid'][1:])
                adj_list_cnts = [(v[0], v[1], w) for v, w in Counter(adj_list).items()]
                H=nx.DiGraph()
                H.add_weighted_edges_from(adj_list_cnts)
                nx.set_node_attributes(H, 'weight', 0)
                H = nx.convert_node_labels_to_integers(H)
                GraphsTrain[key.split('.')[0]]=H

                adj_list = zip(value_test['grid'], value_test['grid'][1:])
                adj_list_cnts = [(v[0], v[1], w) for v, w in Counter(adj_list).items()]
                H=nx.DiGraph()
                H.add_weighted_edges_from(adj_list_cnts)
                nx.set_node_attributes(H, 'weight', 0)
                H = nx.convert_node_labels_to_integers(H)
                GraphsTest[key.split('.')[0]]=H                
        return (GraphsTrain, GraphsTest)




    def parse_into_dn_split_in_two(self, clusters, split_date = '2010-03-01'):
    # parse into directed network (networkx)
        GraphsTrain={}; GraphsTest={};
        for key, value in clusters.items():
            value_train = value[value.datetime<split_date]
            value_test = value[value.datetime>=split_date]
            #print(value.head(n=10))
            #print(value.tail(n=10))
            #print(value.shape, value_train.shape, value_test.shape)

            if not value_train.empty and value_train.shape[0]>1 and not value_test.empty and value_test.shape[0]>1: 
                adj_list = zip(value_train['grid'], value_train['grid'][1:])
                adj_list_cnts = [(v[0], v[1], w) for v, w in Counter(adj_list).items()]
                H=nx.DiGraph()
                H.add_weighted_edges_from(adj_list_cnts)
                nx.set_node_attributes(H, 'weight', 0)
                H = nx.convert_node_labels_to_integers(H)
                GraphsTrain[key.split('.')[0]]=H

                adj_list = zip(value_test['grid'], value_test['grid'][1:])
                adj_list_cnts = [(v[0], v[1], w) for v, w in Counter(adj_list).items()]
                H=nx.DiGraph()
                H.add_weighted_edges_from(adj_list_cnts)
                nx.set_node_attributes(H, 'weight', 0)
                H = nx.convert_node_labels_to_integers(H)
                GraphsTest[key.split('.')[0]]=H                
        return (GraphsTrain, GraphsTest)




    def parse_into_dn_with_node_features(self, clusters):
    # parse into directed network (networkx)
        Graphs={}
        for key, value in clusters.items():
            if not value.empty and value.shape[0]>1:
                adj_list = zip(value['grid'], value['grid'][1:])
                adj_list_cnts = [(v[0], v[1], w) for v, w in Counter(adj_list).items()]
                H=nx.DiGraph()
                H.add_weighted_edges_from(adj_list_cnts)
                node_locations = pd.Series([{'lat':lat, 'lon':lon} for (lat, lon) in zip(value.lat.values, value.lon.values)], index=value.grid).to_dict()
                nx.set_node_attributes(H, 'location', node_locations)
                H = nx.convert_node_labels_to_integers(H)
                print('new graph! \n')
                self.graphfolder = "graphs_with_node_features_" + self.options['frequency']
                self.edgefolder = "edgelists_with_node_features_" + self.options['frequency']
                if not os.path.exists(self.graphfolder):
                    os.makedirs(self.graphfolder)
                if not os.path.exists(self.edgefolder):
                    os.makedirs(self.edgefolder)
                graph_filename = self.graphfolder + "/" + ''.join(key.split(".")[:-1]) + ".gexf"
                nx.write_gexf(H, graph_filename)
                Graphs[key]=H
        self.graphs= Graphs
        return 

    def read_clusters(self):
        n_clusters = []
        user_ids = []
        C = {}
        for key, value in self.data.items():
            user = key.split()[0]
            l = [tuple(x) for x in value[['lat', 'lon']].values]
            locations = []
            for i,j in zip(l, l[1:]):
                locations.append([i,j])
            if os.path.isfile(join(self.options['clusterfolder'], key)): 
                clusters = pd.read_csv(join(self.options['clusterfolder'], key))
                if not clusters.empty:
                    cl = [tuple(x) for x in clusters[['lat', 'lon']].values]
                    n_clusters.append(len(cl))
                    cluster_locations = []
                    for i,j in zip(cl, cl[1:]):
                        cluster_locations.append([i,j])
                else:
                    n_clusters.append(0)  
                user_ids.append(user)
                C[key]=clusters
        return C
