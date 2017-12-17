import operator
import sys
import random as rd
import networkx as nx
import glob

FOLDER = '/var/storage/sandra/mdc_analysis/mdc_data/lausanne/nkYear/edgelists_year/*'


# Get all features of a graph G
def get_subgraph(min_no_nodes, G):
    nodes = nx.number_of_nodes(G)
    if nodes > min_no_nodes:
        central_nodes = sorted(nx.degree_centrality(G).items(), key=operator.itemgetter(1))[:min_no_nodes]
        subgraph = [idx for idx, val in central_nodes]
        sg = nx.subgraph(G, subgraph)
        edgelist = nx.to_edgelist(sg)
        print(edgelist)


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


def create_datasets(input_folder):
    edge_list_files = glob.glob(input_folder)
    file_count = len(edge_list_files)

    sett = set(range(0, file_count))
    for i in range(0, file_count):
        index = rd.sample(sett, 1)[0]
        sett.remove(index)

        G = nx.read_weighted_edgelist(edge_list_files[index])
        get_subgraph(65, G)

create_datasets(FOLDER)