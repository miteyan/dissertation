import os
import sys

sys.path.insert(0, '..')
from lib import models, graph, utils

import tensorflow as tf
import scipy.sparse
import time

import operator
import random as rd
import networkx as nx
import glob
import numpy as np

# MEDIAN = 65
# FOLDER = '/var/storage/miteyan/Dissertation/project/graph_creation/edgelists_month/*'
# FOLDER = '/var/storage/sandra/mdc_analysis/mdc_data/lausanne/nkYear/edgelists_year/*'
MEDIAN = 50
FOLDER = '/var/storage/miteyan/Dissertation/project/cluster/src/clustering/week_clusters/*'


CLASSES = '/var/storage/miteyan/Dissertation/project/data/gender_classes/genderclasses'

# Get subgraph of a graph G
def get_subgraph(min_no_nodes, G):
    nodes = nx.number_of_nodes(G)
    if nodes > min_no_nodes:
        central_nodes = sorted(nx.degree_centrality(G).items(), key=operator.itemgetter(1))[:min_no_nodes]
        subgraph = [idx for idx, val in central_nodes]
        sg = G.subgraph(subgraph)
        edgelist = nx.to_edgelist(sg)

        # print(nx.adjacency_matrix(sg))
        return edgelist


# Get subgraph of a graph G
def get_centrality(min_no_nodes, G):
    nodes = nx.number_of_nodes(G)
    if nodes > min_no_nodes:
        central_nodes = sorted(nx.degree_centrality(G).items(), key=operator.itemgetter(1))[:min_no_nodes]
        central_nodes = sorted(central_nodes, key=operator.itemgetter(0))
        central_nodes = [x[1] for x in central_nodes]
        print(central_nodes)
        return np.array(central_nodes)
#
# # Get subgraph of a graph G
# def get_numpy_subgraph(min_no_nodes, G):
#     nodes = nx.number_of_nodes(G)
#     if nodes > min_no_nodes:
#         central_nodes = sorted(nx.current_flow_betweenness_centrality(G).items(), key=operator.itemgetter(1))[
#                         :min_no_nodes]
#         subgraph = [idx for idx, val in central_nodes]
#         sg = G.subgraph(subgraph)
#         return nx.to_numpy_array(sg)


# Get subgraph of a graph G
def get_scipy_subgraph(min_no_nodes, G):
    nodes = nx.number_of_nodes(G)
    if nodes > min_no_nodes:
        central_nodes = sorted(nx.current_flow_betweenness_centrality(G).items(), key=operator.itemgetter(1))[:min_no_nodes]
        subgraph = [idx for idx, val in central_nodes]
        sg = G.subgraph(subgraph)
        return nx.to_scipy_sparse_matrix(sg)

def get_classes(file):
    with open(file) as f:
        content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    classes = []
    for i in content:
        single_class = i.split(' ')
        classes.append(set(single_class))
    return classes


def get_users_class(userid, classes):
    if userid in classes[0]:
        return 0
    elif userid in classes[1]:
        return 1
    else:
        return "ERROR with id: ", userid


def create_datasets(input_folder, num_nodes):
    edge_list_files = glob.glob(input_folder)
    file_count = len(edge_list_files)
    classes = get_classes(CLASSES)

    sett = set(range(0, file_count))

    graphs = []
    labels = []
    graphs2 = []

    for i in range(0, file_count):
        index = rd.sample(sett, 1)[0]
        sett.remove(index)
        # userid = edge_list_files[index][73:77]
        userid = edge_list_files[index][79:83]
        print(userid)
        label = get_users_class(userid, classes)
        # filter away graphs without any demographic data in the dataset
        if label == 0 or label == 1:
            try:
                G = nx.read_weighted_edgelist(edge_list_files[index])
                sg = get_centrality(num_nodes, G)
                sg2 = get_scipy_subgraph(num_nodes, G)
                if sg is not None:
                    labels.append(label)
                    # print(sg)
                    graphs.append(sg)
                    graphs2.append(sg2)
            except nx.NetworkXError:
                print("Unconnected graph: ", userid)
    return np.array(graphs), np.array(graphs2), np.array(labels)


def get_data_in_format(data):
    print(len(data))
    print(len(data[0]))
    return scipy.sparse.csr_matrix(data)


# def get_data_in_format(data):
#     data_tmp = []
#     for i in range(0, len(data)):
#         # need to append an data[i] length array here.
#         print(data[i])
#         data_tmp.append(data[i][0])
#         # sorted order of nodes..
#     return scipy.sparse.csr_matrix(np.array(data_tmp))
# return a matrix of |Nodes| x |Features(no of nodes or median)|


def split_train_test_valid(array, test, valid):
    if test+valid < 1 and test>0 and valid > 0:
        return np.split(array, [int(1-(test+valid) * len(array)), int((1-valid) * len(array))])
    else:
        raise Exception('Train, test, valid percents do not add to 100')

graphs, graphs2, labels = create_datasets(FOLDER, MEDIAN)
np.savetxt("./data/graphs.npy", graphs, fmt='%1.17f')
np.save("./data/graphs2.npy", graphs2)
np.savetxt("./data/labels.npy", labels, fmt='%1.8f')