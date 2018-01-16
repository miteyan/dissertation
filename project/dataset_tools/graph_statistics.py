import operator
import random as rd
import networkx as nx
import glob

MONTH_EDGELISTS = '/var/storage/miteyan/Dissertation/project/graph_creation/edgelists_month/*'
CLASSES = '/var/storage/miteyan/Dissertation/project/data/age_classes/age_classes'
# FOLDER = '/var/storage/sandra/mdc_analysis/mdc_data/lausanne/nkYear/edgelists_year/*'
FOLDER = '/var/storage/miteyan/Dissertation/project/cluster/src/clustering/week_clusters/*'

def get_classes(file):
    with open(file) as f:
        content = f.readlines()
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


def print_info(input_folder):
    edge_list_files = glob.glob(input_folder)
    file_count = len(edge_list_files)
    sett = set(range(0, file_count))
    nodes_list = []

    for i in range(0, len(edge_list_files)):
        index = rd.sample(sett, 1)[0]
        sett.remove(index)
        G = nx.read_weighted_edgelist(edge_list_files[index])
        nodes = nx.number_of_nodes(G)
        nodes_list.insert(0, nodes)
    nodes_list = sorted(nodes_list)
    print(nodes_list)
    length = len(nodes_list)
    print(length/2)
    median = nodes_list[int(len(nodes_list)/2)]
    print(median)

print_info(FOLDER)
