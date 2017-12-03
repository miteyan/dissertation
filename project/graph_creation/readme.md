# 1. preprocess.py :
		* does sanity checks and data cleaning
		* splits into chunks of desired frequency (e.g. weekly)
		* saves gps datafiles as csv with standardized column names

# 2. (undersample_)cluster_and_visualize_with_folium
		* reads csv into pandas dataframe
		* samples the raw data
		* cluster applying Kang's algorithm
		* visualizes the clustering using folium and pygmaps

# 3. graphStats
		* reads the clusters
		* generates edgelist txt files to be read into networkx graphs
		* generates gexf files corresponding to directed networkx graphs, after relabelling the nodes to integers

# 4. plotGraphs
		* plots the generated graphs using matplotlib

# 5. seqloc
		* plot dwelling times on the nodes of the graph

# 6. plot_timespan
		* code to plot the timespan of the data groupped in weeks

# 7. network_feature_extraction
		* extract topological features of the networks

# 8. train_model
		* train supervised learning problems to eventually estimate the likelihoods of the identities


