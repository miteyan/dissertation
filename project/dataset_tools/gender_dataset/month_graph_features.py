import networkx as nx
import glob
import dataset_tools.dataset_utils as du

# FOLDER = '/var/storage/sandra/mdc_analysis/mdc_data/lausanne/nkYear/edgelists_year/*'
MONTHS = '/var/storage/miteyan/Dissertation/project/graph_creation_lib/edgelists_month/*'
DATASET = '../data/month_features/month_features.csv'

def create_adjacency_matrices(folder):
    edge_list_files = glob.glob(folder)
    file_count = len(edge_list_files)

    file = open(DATASET, 'x')
    for i in range(0, file_count):
        G = nx.read_weighted_edgelist(edge_list_files[i])

        # common_edges = [(u, v, d) for (u, v, d) in G.edges(data=True) if d['weight'] > 1.5]

        # Graph Features
        nodes = nx.number_of_nodes(G)
        edges = nx.number_of_edges(G)

        density = nx.density(G)
        diameter = nx.diameter(G)
        degrees = nx.degree(G)
        min_degree, max_degree = du.get_min_max_degrees(degrees)

        eccentricity = nx.eccentricity(G)
        radius, max_radius = du.get_min_max(eccentricity)
        centre_size = sum(x == radius for x in eccentricity.values())
        mean_eccentricity, var_eccentricity = du.get_mean_variance(eccentricity)
        average_shortest_path_length = nx.average_shortest_path_length(G)

        clustering_coefficient = nx.clustering(G)
        mean_clustering_coefficient, var_clustering_coefficient = du.get_mean_variance(clustering_coefficient)
        shortest_path_length = nx.shortest_path_length(G)
        mean_shortest_path_length, var_shortest_path_length, shortest_path, longest_path = \
            du.get_shortest_path_length_stats(shortest_path_length)
        betweeness_centrality = nx.betweenness_centrality(G)
        mean_betweeness_centrality, var_betweeness_centrality = du.get_mean_variance(betweeness_centrality)

        edge_betweeness_centrality = nx.edge_betweenness_centrality(G)
        node_betweeness_centrality = nx.betweenness_centrality(G)
        mean_edge_betweeness_centrality, var_edge_betweeness_centrality = du.get_mean_variance(edge_betweeness_centrality)
        mean_node_betweeness_centrality, var_node_betweeness_centrality = du.get_mean_variance(node_betweeness_centrality)

        pagerank = nx.pagerank(G)
        mean_pagerank, var_pagerank = du.get_mean_variance(pagerank)

        # A = nx.adjacency_matrix(G)
        # assert A.shape == (nodes,nodes)
        line = ('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'
              .format(edge_list_files[i][73:77], nodes, edges, min_degree, max_degree, density,
                      diameter, radius, max_radius, centre_size, mean_eccentricity, var_eccentricity,
                      average_shortest_path_length, mean_clustering_coefficient, var_clustering_coefficient,
                      mean_betweeness_centrality, var_betweeness_centrality, mean_shortest_path_length,
                      var_shortest_path_length, shortest_path, longest_path, mean_edge_betweeness_centrality,
                      var_node_betweeness_centrality, mean_node_betweeness_centrality, var_node_betweeness_centrality,
                      mean_pagerank, var_pagerank))

        file.write(line)


create_adjacency_matrices(MONTHS)