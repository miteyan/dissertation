import random as rd
import networkx as nx
import glob
import csv
from dataset_tools.feature_extraction import  get_features

YEAR_EDGE_LISTS = '/var/storage/sandra/mdc_analysis/mdc_data/lausanne/nkYear/edgelists_year/*'
WRITE_FOLDER = '/var/storage/miteyan/Dissertation/project/data/genderdata/'
CLASSES = '/var/storage/miteyan/Dissertation/project/data/gender_classes/genderclasses'
FILE_NAME = WRITE_FOLDER + "/dataset.csv"

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
    # with open(file_names[j], 'wt') as resultFile:
    #     wr = csv.writer(resultFile)
    # file = open(FILE_NAMES[j], 'wt', encoding='utf-16')
    with open(FILE_NAME, 'wt', encoding='utf-16') as file:
        csvwriter = csv.writer(file, delimiter=',')
        for i in range(0, file_count):
            index = rd.sample(sett, 1)[0]
            sett.remove(index)
            # User id for monthly graphs and yearly graphs are different
            userid = edge_list_files[index][73:77]
            label = get_users_class(userid, classes)
            # filter away graphs without any demographic data in the dataset
            if label == 0 or label == 1:

                # Get graph Features
                G = nx.read_weighted_edgelist(edge_list_files[index])
                features = get_features(label, G)
                print(features)
                # common_edges = [(u, v, d) for (u, v, d) in G.edges(data=True) if d['weight'] > 1.5]
                # write into csv file for either male or female
                csvwriter.writerow(features)
                print(features)

create_datasets(YEAR_EDGE_LISTS)