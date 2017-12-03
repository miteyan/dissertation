import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
G = nx.read_weighted_edgelist('/var/storage/sandra/mdc_analysis/mdc_data/lausanne/nkYear/edgelists_year/54480')
# G = nx.DiGraph()
# G.add_weighted_edges_from([(1,2, 0.5), (2,3, 0.75)])

print(nx.info(G))
print(nx.is_directed(G))

# Clustering
# for i in nx.clustering(G).items():
# 	print (i)
# print (nx.average_clustering(G))
# print ("Density is: ", nx.density(G))
# print ("Diameter is: ", nx.diameter(G))

nx.draw(G, with_labels=True)
plt.show()
plt.savefig('./foo.png')

print("Done")
