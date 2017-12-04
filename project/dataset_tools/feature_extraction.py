import sys
import networkx as nx


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

    return [label, nodes, edges, max_degree, density,diameter, radius, max_radius, centre_size, mean_eccentricity, var_eccentricity,average_shortest_path_length, mean_clustering_coefficient, var_clustering_coefficient, mean_betweeness_centrality, var_betweeness_centrality, mean_shortest_path_length, var_shortest_path_length, shortest_path, longest_path, mean_edge_betweeness_centrality, var_node_betweeness_centrality, mean_node_betweeness_centrality, var_node_betweeness_centrality, mean_pagerank, var_pagerank]
