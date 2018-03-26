import operator
import sys
import random as rd
import networkx as nx
import glob
import csv
import numpy as np

from scipy.sparse import csr_matrix

# FOLDER =    '/var/storage/miteyan/Dissertation/project/graph_creation_lib/edgelists_month/*'
FOLDER    = '/var/storage/sandra/mdc_analysis/mdc_data/lausanne/nkYear/edgelists_year/*'
# MONTH_EDGELISTS =\
OUTPUT_FOLDER  = '/var/storage/miteyan/Dissertation/project/data/graph_datasets/'
CLASSES = '/var/storage/miteyan/Dissertation/project/data/gender_classes/genderclasses'

# Get subgraph of a graph G
def get_subgraph(min_no_nodes, G):
    nodes = nx.number_of_nodes(G)
    if nodes > min_no_nodes:
        central_nodes = sorted(nx.current_flow_betweenness_centrality(G).items(), key=operator.itemgetter(1))[:min_no_nodes]
        subgraph = [idx for idx, val in central_nodes]
        sg = G.subgraph(subgraph)
        edgelist = nx.to_edgelist(sg)

        print(nx.adjacency_matrix(sg))
        return edgelist


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


def create_datasets(input_folder, output_folder, num_nodes):
    edge_list_files = glob.glob(input_folder)
    file_count = len(edge_list_files)
    classes = get_classes(CLASSES)

    sett = set(range(0, file_count))
    # with open(OUTPUT_FOLDER+'./dataset.csv', 'wt', encoding='utf-16') as file:

    graphs = []


    for i in range(0, 5):
        index = rd.sample(sett, 1)[0]
        sett.remove(index)
        userid = edge_list_files[index][73:77]
        label = get_users_class(userid, classes)
        # filter away graphs without any demographic data in the dataset
        if label == 0 or label == 1:

            G = nx.read_weighted_edgelist(edge_list_files[index])
            sg = get_scipy_subgraph(num_nodes, G)

            if sg is not None:
                print(sg)
                graphs.append(sg)
                # file.write(row)
    print(len(graphs))
    print(graphs[0].shape)
    print(type(graphs))

    nA = np.array(graphs)
    csr_matrix((112,65), dtype=csr_matrix)


create_datasets(FOLDER, OUTPUT_FOLDER, 65)