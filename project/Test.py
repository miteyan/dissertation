from cnn_graph.lib import graph

import networkx as nx
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
G = nx.read_weighted_edgelist('/var/storage/sandra/mdc_analysis/mdc_data/lausanne/nkYear/edgelists_year/54480')
G = nx.DiGraph()
G.add_weighted_edges_from([(1,2, 0.5), (2,3, 0.75)])
nx.draw(G, with_labels=True)
plt.show()
plt.savefig('./foo.png')
d = 100  # Dimensionality.
n = 10000  # Number of samples.
c = 5  # Number of feature communities.

# Data matrix, structured in communities (feature-wise).
X = np.random.normal(0, 1, (n, d)).astype(np.float32)
X += np.linspace(0, 1, c).repeat(d // c)


# Noisy non-linear target.
w = np.random.normal(0, .02, d)
t = X.dot(w) + np.random.normal(0, .001, n)
t = np.tanh(t)

# # Classification.
y = np.ones(t.shape, dtype=np.uint8)
y[t > t.mean() + 0.4 * t.std()] = 0
y[t < t.mean() - 0.4 * t.std()] = 2
print('Class imbalance: ', np.unique(y, return_counts=True)[1])

# Then split this dataset into training, validation and testing sets.

n_train = n // 2
n_val = n // 10

X_train = X[:n_train]
X_val = X[n_train:n_train + n_val]
X_test = X[n_train + n_val:]

y_train = y[:n_train]
y_val = y[n_train:n_train + n_val]
y_test = y[n_train + n_val:]


print("Done")

#
dist, idx = graph.distance_scipy_spatial(X_train.T, k=10, metric='euclidean')
A = graph.adjacency(dist, idx).astype(np.float32)

assert A.shape == (d, d)
print('d = |V| = {}, k|V| < |E| = {}'.format(d, A.nnz))
print(A)

def show_graph(adjacency_matrix):
    g = nx.to_networkx_graph(adjacency_matrix)
    nx.draw(g)
    plt.savefig('./graph2.png')

# show_graph(A)
