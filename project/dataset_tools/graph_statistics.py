import random as rd
import networkx as nx
import glob
from dataset_tools.feature_extraction import  get_features

MONTH_EDGELISTS = '/var/storage/miteyan/Dissertation/project/graph_creation/edgelists_month/*'
CLASSES = '/var/storage/miteyan/Dissertation/project/data/age_classes/age_classes'


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


def create_datasets(input_folder):
    edge_list_files = glob.glob(input_folder)
    classes = get_classes(CLASSES)

    file_count = len(edge_list_files)

    sett = set(range(0, file_count))

    nodes_list = []

    nodes_lt5 = 0
    nodes_lt10 = 0
    nodes_lt20 = 0
    nodes_lt30 = 0
    nodes_lt40 = 0
    nodes_lt50 = 0
    nodes_mt50 = 0

    for i in range(0, 5):
        index = rd.sample(sett, 1)[0]
        sett.remove(index)
        # User id for monthly graphs and yearly graphs are different
        userid = edge_list_files[index][73:77]
        label = get_users_class(userid, classes)
        # filter away graphs without any demographic data in the dataset
        if label == 0 or label == 1:
            # Get graph Features
            G = nx.read_weighted_edgelist(edge_list_files[index])
            S = G.subgraph(nx.nodes(G))
            print('Subgraph: ', S)

            features = get_features(label, G)
            # print(features)
            nodes = features[1]
            nodes_list.insert(0, nodes)
            if nodes < 5:
                nodes_lt5 += 1
            elif nodes < 10:
                nodes_lt10 += 1
            elif nodes < 20:
                nodes_lt20 += 1
            elif nodes < 30:
                nodes_lt30 += 1
            elif nodes < 40:
                nodes_lt40 += 1
            elif nodes < 50:
                nodes_lt50 += 1
            else:
                nodes_mt50 += 1
    print(nodes_lt5, nodes_lt10, nodes_lt20, nodes_lt30, nodes_lt40, nodes_lt50, nodes_mt50)
    nodes_list.sort()
    print(nodes_list)
    print(nodes_list[int(len(nodes_list)/2)])

create_datasets(MONTH_EDGELISTS)