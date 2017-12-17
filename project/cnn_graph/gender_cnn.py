from lib import models, graph, coarsening, utils

import matplotlib
import helper.dataset_functions as ds
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
# %matplotlib inline

dataset = "/var/storage/miteyan/Dissertation/project/data/genderdata/dataset.csv"

train_dataset, test_dataset, valid_dataset = ds.get_data(dataset, 0.1, 0.25, 0.25)

train_labels, train_dataset = ds.get_labels_and_features(train_dataset)
test_labels, test_dataset = ds.get_labels_and_features(test_dataset)
valid_labels, valid_dataset = ds.get_labels_and_features(valid_dataset)

print("Imported")
d = len(train_dataset[0])  # Dimensionality.
c = 2  # Number of feature communities.

X_train = train_dataset
X_val = valid_dataset
X_test = test_dataset

y_train = train_labels
y_val = valid_labels
y_test = test_labels

dist, idx = graph.distance_scipy_spatial(X_train.T, k=2, metric='euclidean')
print(dist)
A = graph.adjacency(dist, idx).astype(np.float32)

print(A.shape, type(A))
assert A.shape == (d, d)
print('d = |V| = {}, k|V| < |E| = {}'.format(d, A.nnz))

n_train = len(train_dataset)

graphs, perm = coarsening.coarsen(A, levels=3, self_connections=False)

X_train = coarsening.perm_data(X_train, perm)
X_val = coarsening.perm_data(X_val, perm)
X_test = coarsening.perm_data(X_test, perm)
L = [graph.laplacian(A, normalized=True) for A in graphs]

params = dict()
params['dir_name'] = 'demo'
params['num_epochs'] = 40
params['batch_size'] = 100
params['eval_frequency'] = 200

# Building blocks.
params['filter'] = 'chebyshev5'
params['brelu'] = 'b1relu'
params['pool'] = 'apool1'

# Number of classes.
C = 2

# Architecture.
params['F'] = [32, 64]  # Number of graph convolutional filters.
params['K'] = [20, 20]  # Polynomial orders.
params['p'] = [4, 2]  # Pooling sizes.
params['M'] = [512, C]  # Output dimensionality of fully connected layers.

# Optimization.
params['regularization'] = 5e-4
params['dropout'] = 1
params['learning_rate'] = 1e-3
params['decay_rate'] = 0.95
params['momentum'] = 0.9
params['decay_steps'] = n_train / params['batch_size']

model = models.cgcnn(L, **params)
accuracy, loss, t_step = model.fit(X_train, y_train, X_val, y_val)

print('Time per step: {:.2f} ms'.format(t_step * 1000))

res = model.evaluate(X_test, y_test)
print(res[0])
