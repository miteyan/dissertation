import sys
import random as rd
import networkx as nx
import glob

# FOLDER = '/var/storage/sandra/mdc_analysis/mdc_data/lausanne/nkYear/edgelists_year/*'
MONTH_EDGELISTS = '/var/storage/miteyan/Dissertation/project/graph_creation/edgelists_month/*'
MONTH_WRITE_FOLDER = './month_datasets'
CLASSES = '/var/storage/miteyan/Dissertation/project/data/genderclasses'


def get_mean_variance(dict):
    count = 0
    sum = 0
    sum2 = 0
    for i in dict:
        sum += dict[i]
        sum2 += dict[i]**2
        count +=1
    EX2 = sum2/count
    mean = sum/count
    return mean, EX2-mean**2


def get_min_max(dict):
    maximum = -sys.maxsize
    minimum = sys.maxsize
    for i in dict.keys():
        maximum = max(maximum, dict[i])
        minimum = min(minimum, dict[i])
    return minimum, maximum


def get_min_max_degrees(degree_view):
    maximum = -sys.maxsize
    minimum = sys.maxsize
    for i in degree_view:
        maximum = max(maximum, i[1])
        minimum = min(minimum, i[1])
    return minimum, maximum


# Create an array of edgelists from the folder containing edgelists
def get_shortest_path_length_stats(shortest_path_length):
    sum = 0
    sum2 = 0
    count = 0
    minimum = 0
    maximum = 0
    for i in shortest_path_length:
        for j in i[1]:
            path_length = i[1][j]
            sum += path_length
            sum2 += path_length*path_length
            count +=1
            minimum = min(minimum, path_length)
            maximum = max(maximum, path_length)
    EX2 = sum2/count
    mean = sum/count
    var = EX2 - mean**2
    return mean, var, minimum, maximum


# Get all features of a graph G
def get_features(label, G):
    nodes = nx.number_of_nodes(G)
    edges = nx.number_of_edges(G)

    density = nx.density(G)
    diameter = nx.diameter(G)
    degrees = nx.degree(G)
    min_degree, max_degree = get_min_max_degrees(degrees)

    eccentricity = nx.eccentricity(G)
    radius, max_radius = get_min_max(eccentricity)
    centre_size = sum(x == radius for x in eccentricity.values())
    mean_eccentricity, var_eccentricity = get_mean_variance(eccentricity)
    average_shortest_path_length = nx.average_shortest_path_length(G)

    clustering_coefficient = nx.clustering(G)
    mean_clustering_coefficient, var_clustering_coefficient = get_mean_variance(clustering_coefficient)
    shortest_path_length = nx.shortest_path_length(G)
    mean_shortest_path_length, var_shortest_path_length, shortest_path, longest_path = \
        get_shortest_path_length_stats(shortest_path_length)
    betweeness_centrality = nx.betweenness_centrality(G)
    mean_betweeness_centrality, var_betweeness_centrality = get_mean_variance(betweeness_centrality)

    edge_betweeness_centrality = nx.edge_betweenness_centrality(G)
    node_betweeness_centrality = nx.betweenness_centrality(G)
    mean_edge_betweeness_centrality, var_edge_betweeness_centrality = get_mean_variance(edge_betweeness_centrality)
    mean_node_betweeness_centrality, var_node_betweeness_centrality = get_mean_variance(node_betweeness_centrality)

    pagerank = nx.pagerank(G)
    mean_pagerank, var_pagerank = get_mean_variance(pagerank)

    return ('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'
          .format(label, nodes, edges, max_degree, density,
                  diameter, radius, max_radius, centre_size, mean_eccentricity, var_eccentricity,
                  average_shortest_path_length, mean_clustering_coefficient, var_clustering_coefficient,
                  mean_betweeness_centrality, var_betweeness_centrality, mean_shortest_path_length,
                  var_shortest_path_length, shortest_path, longest_path, mean_edge_betweeness_centrality,
                  var_node_betweeness_centrality, mean_node_betweeness_centrality, var_node_betweeness_centrality,
                  mean_pagerank, var_pagerank))


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


def create_datasets(input_folder, train_percent, test_percent, valid_percent):
    edge_list_files = glob.glob(input_folder)
    classes = get_classes(CLASSES)
    s = round(train_percent + test_percent + valid_percent, 2)
    if s != 1.0:
        raise ValueError("Invalid percentages: Do not add to 1: ", s)

    file_count = len(edge_list_files)
    train_data = round(train_percent*file_count)
    test_data = round(test_percent*file_count)
    valid_data = round(valid_percent*file_count)

    lengths = [train_data, test_data, valid_data]
    file_names = [MONTH_WRITE_FOLDER + "/train.csv", MONTH_WRITE_FOLDER + "/test.csv", MONTH_WRITE_FOLDER + "/valid.csv"]
    print("Writing: ", lengths)


    sett = set(range(0, file_count))
    seen = 0
    for j in range(0, 3):
        # with open(file_names[j], 'wt') as resultFile:
        #     wr = csv.writer(resultFile)
        file = open(file_names[j], 'wt', encoding='utf-16')
        for i in range(seen, seen+lengths[j]):
            index = rd.sample(sett, 1)[0]
            sett.remove(index)

            userid = edge_list_files[index][-5:-1]
            label = get_users_class(userid, classes)
            # filter away graphs without any demographic data in the dataset
            if label == 0 or label == 1:

                # Get graph Features
                G = nx.read_weighted_edgelist(edge_list_files[index])
                features = get_features(label, G)
                print(features)
                # common_edges = [(u, v, d) for (u, v, d) in G.edges(data=True) if d['weight'] > 1.5]
                # write into csv file for either male or female
                file.write(features)
                print(features)
        seen += lengths[j]


create_datasets(MONTH_EDGELISTS, 0.7, 0.2, 0.1)