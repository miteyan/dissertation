from lib import models, graph, coarsening, utils

import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
# %matplotlib inline

print("Imported")
d = 5  # Dimensionality.
n = 100  # Number of samples.
# number of clusters in the graph
c = 5  # Number of feature communities.

# Data matrix, structured in communities (feature-wise).
# generate 1000000 floats from 0 to 1.
# X is a n length array consisting of d length arrays = nd 2d array
X = np.random.normal(0, 1, (n, d)).astype(np.float32)
# Return evenly spaced numbers over a specified interval 20 times.
X += np.linspace(0, 1, c).repeat(d // c)


# Noisy non-linear target. w is an array of d floats [0,0.02]
w = np.random.normal(0, .02, d)
# t = wX + b, a n length array to determine which class to put the graphs in.
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

print(X)

X_train = X[:n_train]
X_val = X[n_train:n_train + n_val]
X_test = X[n_train + n_val:]

y_train = y[:n_train]
y_val = y[n_train:n_train + n_val]
y_test = y[n_train + n_val:]

dist, idx = graph.distance_scipy_spatial(X_train.T, k=5, metric='euclidean')
print(dist)
A = graph.adjacency(dist, idx).astype(np.float32)

print(A.shape, type(A))
assert A.shape == (d, d)
print('d = |V| = {}, k|V| < |E| = {}'.format(d, A.nnz))
# print(A)

graphs, perm = coarsening.coarsen(A, levels=3, self_connections=False)

X_train = coarsening.perm_data(X_train, perm)
X_val = coarsening.perm_data(X_val, perm)
X_test = coarsening.perm_data(X_test, perm)
# Xtrain type is <class 'numpy.ndarray'>
L = [graph.laplacian(A, normalized=True) for A in graphs]


params = dict()
params['dir_name']       = 'demo'
params['num_epochs']     = 40
params['batch_size']     = 100
params['eval_frequency'] = 200

# Building blocks.
params['filter']         = 'chebyshev5'
params['brelu']          = 'b1relu'
params['pool']           = 'apool1'

# Number of classes.
C = y.max() + 1
assert C == np.unique(y).size

# Architecture.
params['F']              = [32, 64]  # Number of graph convolutional filters.
params['K']              = [20, 20]  # Polynomial orders.
params['p']              = [4, 2]    # Pooling sizes.
params['M']              = [512, C]  # Output dimensionality of fully connected layers.

# Optimization.
params['regularization'] = 5e-4
params['dropout']        = 1
params['learning_rate']  = 1e-3
params['decay_rate']     = 0.95
params['momentum']       = 0.9
params['decay_steps']    = n_train / params['batch_size']


model = models.cgcnn(L, **params)
accuracy, loss, t_step = model.fit(X_train, y_train, X_val, y_val)


print('Time per step: {:.2f} ms'.format(t_step*1000))


res = model.evaluate(X_test, y_test)
print(res[0])