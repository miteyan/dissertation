import random as rd
import tempfile
from tempfile import NamedTemporaryFile

import networkx as nx
import glob
import csv
from dataset_tools.feature_extraction import  get_features

# EDGE_LISTS = '/var/storage/sandra/location2017/emotionsense/data/graphs/edges/*'
EDGE_LISTS = '/var/storage/miteyan/Dissertation/project/data/emotionsense/*'
# TEST = '/Users/miteyan/dissertation/project/emotionsense_data/data/*'
WRITE_FOLDER = '/var/storage/miteyan/Dissertation/project/data/emotionsense_edge_lists/'
CLASSES = '/var/storage/miteyan/Dissertation/project/data/emotion_sense_classes.txt'

WRITE_FILE = "/var/storage/miteyan/Dissertation/project/data/emotion_sense_dataset.csv"

def get_classes(file):
    with open(file) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    classes = []
    for i in content:
        single_class = i.split(' ')
        classes.append(set(single_class))
    return classes

def create_edgelists(directory):
    edge_list_files = glob.glob(directory)
    file_count = len(edge_list_files)
    for i in range(0, file_count):
        with open(WRITE_FOLDER + edge_list_files[i].split("/")[-1], 'wt') as file:
            csvwriter = csv.writer(file, delimiter=' ')
            with open(edge_list_files[i], "r") as f:
                for line in f.readlines()[1:]:
                    print(line)
                    line = line.split()
                    csvwriter.writerow([line[1], line[2], line[4]])

# create_edgelists(EDGE_LISTS)

def get_users_class(userid, classes):
    if userid in classes[0]:
        return 0
    elif userid in classes[1]:
        return 1
    else:
        return "ERROR with id: ", userid

# No of labels 0 = , 1 =
def create_datasets(input_folder):
    edge_list_files = glob.glob(input_folder)
    classes = get_classes(CLASSES)
    file_count = len(edge_list_files)
    print(file_count)
    # with open(file_names[j], 'wt') as resultFile:
    #     wr = csv.writer(resultFile)
    # file = open(FILE_NAMES[j], 'wt', encoding='utf-16')
    with open(WRITE_FILE, 'wt', encoding='utf-16') as file:
        error = 0
        nonerror = 0
        csvwriter = csv.writer(file, delimiter=',')
        for i in range(0, file_count):
            # User id for monthly graphs and yearly graphs are different
            # print(edge_list_files[index])
            userid = edge_list_files[i][60:75]
            # print(userid)
            label = get_users_class(userid, classes)
            # filter away graphs without any demographic data in the dataset
            if label == 0 or label == 1:
                # Get graph Features
                G = nx.read_weighted_edgelist(edge_list_files[i])
                number_nodes = nx.number_of_nodes(G)
                if (number_nodes > 5):
                    try:
                        features = get_features(label, G)
                        print(features)
                        csvwriter.writerow(features)
                        nonerror+=1
                    except ValueError:
                        error+=1
                        continue
        print(error, nonerror)

create_datasets(EDGE_LISTS)