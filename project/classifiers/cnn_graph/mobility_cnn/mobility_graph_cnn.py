import os
import sys

from numpy.random import RandomState

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

# set median or nodes per subgraph depending on structure/histogram of the graphs
MEDIAN = 49
# FOLDER2 = '/var/storage/miteyan/Dissertation/project/graph_creation_lib/edgelists_month/*'
# FOLDER2 = '/var/storage/sandra/mdc_analysis/mdc_data/lausanne/nkYear/edgelists_year/*'
# MEDIAN = 30

FOLDER2 = '/var/storage/miteyan/Dissertation/project/cluster/src/clustering/week_clusters/*'
CLASSES = '/var/storage/miteyan/Dissertation/project/data/gender_classes/genderclasses'

# FOLDER2 = '/var/storage/miteyan/Dissertation/project/data/emotionsense/*'
# FOLDER2 = '/var/storage/miteyan/Dissertation/project/graph_creation_lib/edgelists_month/*'
# CLASSES = '/var/storage/miteyan/Dissertation/project/data/age_classes/age_classes'
folder0 = '/var/storage/miteyan/Dissertation/project/cnn_graph/data/graphs0/*'
folder1 = '/var/storage/miteyan/Dissertation/project/cnn_graph/data/graphs1/*'
# FOLDER2 = '/var/storage/miteyan/Dissertation/project/data/emotionsense/*'
# CLASSES = '/var/storage/miteyan/Dissertation/project/data/emotion_sense_classes.txt'

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
        # print(central_nodes)
        return np.array(central_nodes)


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
        central_nodes = sorted(nx.current_flow_betweenness_centrality(G).items(), key=operator.itemgetter(1))[
                        :min_no_nodes]
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


def create_synthetic(input_folder1, input_folder2, num_nodes):
    edge_list_files = glob.glob(input_folder1)
    file_count = len(edge_list_files)

    graphs = []
    labels = []
    graphs2 = []

    for i in range(0, file_count):
        label = 0
        try:
            G = nx.read_weighted_edgelist(edge_list_files[i])
            sg = get_centrality(num_nodes, G)
            sg2 = get_scipy_subgraph(num_nodes, G)
            if sg is not None:
                labels.append(label)
                # print(sg)
                graphs.append(sg)
                graphs2.append(sg2)
        except nx.NetworkXError:
            continue
            # print("Unconnected graph: ", userid)

    edge_list_files = glob.glob(input_folder2)
    for i in range(0, file_count):
        label = 1
        try:
            G = nx.read_weighted_edgelist(edge_list_files[i])
            sg = get_centrality(num_nodes, G)
            sg2 = get_scipy_subgraph(num_nodes, G)
            if sg is not None:
                labels.append(label)
                graphs.append(sg)
                graphs2.append(sg2)
        except nx.NetworkXError:
            continue
    shuffleDataAndLabelsInPlace(graphs, graphs2, labels)

    return np.array(graphs), np.array(graphs2), np.array(labels)


def shuffleDataAndLabelsInPlace(arr1, arr2, arr3):
    seed = 3432
    prng = RandomState(seed)
    prng.shuffle(arr1)
    prng = RandomState(seed)
    prng.shuffle(arr2)
    prng = RandomState(seed)
    prng.shuffle(arr3)


def create_datasets(input_folder, num_nodes):
    edge_list_files = glob.glob(input_folder)
    file_count = len(edge_list_files)
    classes = get_classes(CLASSES)

    sett = set(range(0, file_count))

    graphs = []
    labels = []
    graphs2 = []
    label0 = 0
    label1 = 0

    for i in range(0, file_count):
        userid = edge_list_files[i][73:77]
        label = get_users_class(userid, classes)
        if label == 0:
            label0 += 1
        if label == 1:
            label1 += 1
    labelMin = min(label0, label1)
    if label0 == label:
        firstClass = True
    else:
        firstClass = False
    labelCount = 0
    for i in range(0, file_count):
        index = rd.sample(sett, 1)[0]
        sett.remove(index)
        userid = edge_list_files[index][73:77]
        print(userid)
        # userid = edge_list_files[index][60:75]
        # print(userid)
        label = get_users_class(userid, classes)
        # filter away graphs without any demographic data in the dataset
        if label == 0 or label == 1:
            if labelCount <= labelMin:
                if firstClass and label == 1:
                    labelCount += 1
                elif not firstClass and label == 0:
                    labelCount += 1
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
                    continue
                    # print("Unconnected graph: ", userid)

    return np.array(graphs), np.array(graphs2), np.array(labels)


def get_data_in_format(data):
    # print(len(data))
    # print(len(data[0]))
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
    if test + valid < 1 and test > 0 and valid > 0:
        return np.split(array, [int(1 - (test + valid) * len(array)), int((1 - valid) * len(array))])
    else:
        raise Exception('Train, test, valid percents do not add to 100')

print("Creating: ")
graphs, graphs2, labels = create_synthetic(folder0, folder1, MEDIAN)
# np.savetxt("./data/graphs.npy", graphs, fmt='%1.17f')
# np.save("./data/graphs2.npy", graphs2)
# np.savetxt("./data/labels.npy", labels, fmt='%1.8f')
#
# graphs = np.loadtxt("./data/graphs.npy", dtype="f")
# graphs22 = np.load("./data/graphs2.npy")
# labels = np.loadtxt("./data/labels.npy", dtype="f")
# save to file
# split into train, test, valid
# train_data, test_data, val_data = split_train_test_valid(graphs, 0.25, 0.25)
# train_labels, test_labels, val_labels = split_train_test_valid(labels, 0.25, 0.25)
length = len(graphs)

train_data = graphs[:int(length / 2)]
train_labels = labels[:int(length / 2)]

test_data = graphs[int(length / 2):int(3 * length / 4)]
test_labels = labels[int(length / 2):int(3 * length / 4)]

print(test_labels)
val_data = graphs[int(3 * length / 4):]
val_labels = labels[int(3 * length / 4):]

train_data = get_data_in_format(train_data)
test_data = get_data_in_format(test_data)
val_data = get_data_in_format(val_data)

flags = tf.app.flags
FLAGS = flags.FLAGS

# Graphs parameters from 20news dataset.
flags.DEFINE_integer('number_edges', 16, 'Graph: minimum number of edges per vertex.')
flags.DEFINE_string('metric', 'cosine', 'Graph: similarity measure (between features).')
flags.DEFINE_bool('normalized_laplacian', True, 'Graph Laplacian: normalized.')
flags.DEFINE_integer('coarsening_levels', 0, 'Number of coarsened graphs.')
flags.DEFINE_string('dir_data', os.path.join('..', 'data', '20news'), 'Directory to store data.')
flags.DEFINE_integer('val_size', 400, 'Size of the validation set.')

# Fetch dataset. Scikit-learn already performs some cleaning.
remove = ('headers', 'footers', 'quotes')  # (), ('headers') or ('headers','footers','quotes')

L = [graph.laplacian(A, normalized=True) for A in graphs2]

t_start = time.process_time()

if True:
    utils.baseline(train_data, train_labels, test_data, test_labels)

common = {}
common['dir_name'] = 'nokia/'
common['num_epochs'] = 100
common['batch_size'] = 50
common['decay_steps'] = len(train_labels) / common['batch_size']
common['eval_frequency'] = 5 * common['num_epochs']
common['filter'] = 'chebyshev5'
common['brelu'] = 'b1relu'
common['pool'] = 'mpool1'
C = max(train_labels) + 1  # number of classes

model_perf = utils.model_perf()

start = time.time()
if True:
    name = 'softmax'
    params = common.copy()
    params['dir_name'] += name
    params['regularization'] = 0
    params['dropout'] = 1
    params['learning_rate'] = 1e3
    params['decay_rate'] = 0.95
    params['momentum'] = 0.9
    params['F'] = []
    params['K'] = []
    params['p'] = []
    params['M'] = [C]
    model = models.cgcnn(L, **params)
    model_perf.test(model, name, params, train_data, train_labels, val_data, val_labels, test_data, test_labels)
print(time.time()-start)