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

flags = tf.app.flags
FLAGS = flags.FLAGS

# Graphs.
flags.DEFINE_integer('number_edges', 16, 'Graph: minimum number of edges per vertex.')
flags.DEFINE_string('metric', 'cosine', 'Graph: similarity measure (between features).')
# TODO: change cgcnn for combinatorial Laplacians.
flags.DEFINE_bool('normalized_laplacian', True, 'Graph Laplacian: normalized.')
flags.DEFINE_integer('coarsening_levels', 0, 'Number of coarsened graphs.')

flags.DEFINE_string('dir_data', os.path.join('..', 'data', '20news'), 'Directory to store data.')
flags.DEFINE_integer('val_size', 400, 'Size of the validation set.')


# Fetch dataset. Scikit-learn already performs some cleaning.
remove = ('headers','footers','quotes')  # (), ('headers') or ('headers','footers','quotes')


# FOLDER =    '/var/storage/miteyan/Dissertation/project/graph_creation/edgelists_month/*'
FOLDER  = '/var/storage/sandra/mdc_analysis/mdc_data/lausanne/nkYear/edgelists_year/*'
CLASSES = '/var/storage/miteyan/Dissertation/project/data/gender_classes/genderclasses'

# Get subgraph of a graph G
def get_subgraph(min_no_nodes, G):
    nodes = nx.number_of_nodes(G)
    if nodes > min_no_nodes:
        central_nodes = sorted(nx.current_flow_betweenness_centrality(G).items(), key=operator.itemgetter(1))[:min_no_nodes]
        subgraph = [idx for idx, val in central_nodes]
        sg = G.subgraph(subgraph)
        edgelist = nx.to_edgelist(sg)

        # print(nx.adjacency_matrix(sg))
        return edgelist


# Get subgraph of a graph G
def get_numpy_subgraph(min_no_nodes, G):
    nodes = nx.number_of_nodes(G)
    if nodes > min_no_nodes:
        central_nodes = sorted(nx.current_flow_betweenness_centrality(G).items(), key=operator.itemgetter(1))[:min_no_nodes]
        subgraph = [idx for idx, val in central_nodes]
        sg = G.subgraph(subgraph)
        return nx.to_numpy_array(sg)


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
        userid = edge_list_files[index][73:77]
        label = get_users_class(userid, classes)
        # filter away graphs without any demographic data in the dataset
        if label == 0 or label == 1:
            G = nx.read_weighted_edgelist(edge_list_files[index])
            sg = get_numpy_subgraph(num_nodes, G)
            sg2 = get_scipy_subgraph(num_nodes, G)
            labels.append(label)
            if sg is not None:
                # print(sg)
                graphs.append(sg)
                graphs2.append(sg2)

    return np.array(graphs), np.array(graphs2), np.array(labels)


def get_data_in_format(data):
    data_tmp = []
    for i in range(0, len(data)):
        data_tmp.append(data[i][0])
    return scipy.sparse.csr_matrix(np.array(data_tmp))

graphs, graphs2, labels = create_datasets(FOLDER, 65)
# split into train, test, valid
length = len(graphs)
train_data = graphs[:int(length/2)]
train_labels = labels[:int(length/2)]


# print(type(train_data))
# print(type(train_data[0]))
# print(train_data[0].shape)
    # (65, 65)

# train_data2 = []
# for i in range(0, len(train_data)):
#     train_data2.append(train_data[i][0])
# train_data = scipy.sparse.csr_matrix(np.array(train_data2))


test_data = graphs[int(length/2):int(3*length/4)]
test_labels = labels[int(length/2):int(3*length/4)]


# test_data2 = []
# for i in range(0, len(test_data)):
#     train_data2.append(test_data[i].flatten())
# test_data = scipy.sparse.csr_matrix(np.array(test_data2))

val_data = graphs[int(3*length/4):]
val_labels = labels[int(3*length/4):]

L = [graph.laplacian(A, normalized=True) for A in graphs2]


train_data = get_data_in_format(train_data)
test_data = get_data_in_format(test_data)
val_data = get_data_in_format(val_data)

t_start = time.process_time()
print('Execution time: {:.2f}s'.format(time.process_time() - t_start))

# print(type(train_data))
# print(type(test_data[0]))
#
# print(train_data.shape)
# print(test_data.shape)
# print(val_data.shape)
#
# print()
# print(train_data[0].shape)

if True:
    utils.baseline(train_data, train_labels, train_data, train_labels)

common = {}
common['dir_name']       = '20news/'
common['num_epochs']     = 80
common['batch_size']     = 50
common['decay_steps']    = len(train_labels) / common['batch_size']
common['eval_frequency'] = 5 * common['num_epochs']
common['filter']         = 'chebyshev5'
common['brelu']          = 'b1relu'
common['pool']           = 'mpool1'
C = max(train_labels) + 1  # number of classes

model_perf = utils.model_perf()



if True:
    name = 'softmax'
    params = common.copy()
    params['dir_name'] += name
    params['regularization'] = 0
    params['dropout']        = 1
    params['learning_rate']  = 1e3
    params['decay_rate']     = 0.95
    params['momentum']       = 0.9
    params['F']              = []
    params['K']              = []
    params['p']              = []
    params['M']              = [C]

    model = models.cgcnn(L, **params)

    model_perf.test(model, name, params,train_data, train_labels, val_data, val_labels, test_data, test_labels)