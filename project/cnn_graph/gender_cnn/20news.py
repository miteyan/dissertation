import sys, os
sys.path.insert(0, '..')
from lib import models, graph, coarsening, utils

import tensorflow as tf
import scipy.sparse
import numpy as np
import time

flags = tf.app.flags
FLAGS = flags.FLAGS

# Graphs.
flags.DEFINE_integer('number_edges', 16, 'Graph: minimum number of edges per vertex.')
flags.DEFINE_string('metric', 'cosine', 'Graph: similarity measure (between features).')
# TODO: change cgcnn for combinatorial Laplacians.
flags.DEFINE_bool('normalized_laplacian', True, 'Graph Laplacian: normalized.')
flags.DEFINE_integer('coarsening_levels', 0, 'Number of coarsened graphs.')

flags.DEFINE_string('dir_data', os.path.join('..', 'data', '20news'), 'Directory to store data.')
flags.DEFINE_integer('val_size', 400, 'Size of the validation set.')


# Fetch dataset. Scikit-learn already performs some cleaning.
remove = ('headers','footers','quotes')  # (), ('headers') or ('headers','footers','quotes')
train = utils.Text20News(data_home=FLAGS.dir_data, subset='train', remove=remove)

# Pre-processing: transform everything to a-z and whitespace.
train.clean_text(num='substitute')

# Analyzing / tokenizing: transform documents to bags-of-words.
#stop_words = set(sklearn.feature_extraction.text.ENGLISH_STOP_WORDS)
# Or stop words from NLTK.
# Add e.g. don, ve.
train.vectorize(stop_words='english')

# Remove short documents.
train.data_info(True)
wc = train.remove_short_documents(nwords=20, vocab='full')
train.data_info()
# plt.figure(figsize=(17,5))
# plt.semilogy(wc, '.');

# Remove encoded images.
def remove_encoded_images(dataset, freq=1e3):
    widx = train.vocab.index('ax')
    wc = train.data[:,widx].toarray().squeeze()
    idx = np.argwhere(wc < freq).squeeze()
    dataset.keep_documents(idx)
    return wc
wc = remove_encoded_images(train)
train.data_info()


# Word embedding
if True:
    train.embed()
else:
    train.embed(os.path.join('..', 'data', 'word2vec', 'GoogleNews-vectors-negative300.bin'))
train.data_info()
# Further feature selection. (TODO)


# Feature selection.
# Other options include: mutual information or document count.
freq = train.keep_top_words(1000, 20)
train.data_info()
train.show_document(1)
# plt.figure(figsize=(17,5))
# plt.semilogy(freq);

# Remove documents whose signal would be the zero vector.
wc = train.remove_short_documents(nwords=5, vocab='selected')
train.data_info(True)

train.normalize(norm='l1')
train.show_document(1);


test = utils.Text20News(data_home=FLAGS.dir_data, subset='test', remove=remove)
test.clean_text(num='substitute')
test.vectorize(vocabulary=train.vocab)
test.data_info()
wc = test.remove_short_documents(nwords=5, vocab='selected')
test.data_info(True)
test.normalize(norm='l1')

train_data = train.data.astype(np.float32)
test_data = test.data.astype(np.float32)
train_labels = train.labels
test_labels = test.labels


graph_data = train.embeddings.astype(np.float32)

#del train, test


t_start = time.process_time()
dist, idx = graph.distance_sklearn_metrics(graph_data, k=FLAGS.number_edges, metric=FLAGS.metric)
A = graph.adjacency(dist, idx)
# print("{} > {} edges".format(A.nnz//2, FLAGS.number_edges*graph_data.shape[0]//2))
A = graph.replace_random_edges(A, 0)
graphs, perm = coarsening.coarsen(A, levels=FLAGS.coarsening_levels, self_connections=False)
L = [graph.laplacian(A, normalized=True) for A in graphs]
# print('Execution time: {:.2f}s'.format(time.process_time() - t_start))

# print(type(graphs))
# print(type(graphs[0]))
# print("A SHAPE")
# print(type(A))
# <class 'scipy.sparse.csr.csr_matrix'>
# print(A[0])
#   (0, 130)	0.203579
#   (0, 376)	0.264287
#   (0, 468)	0.138664 ...
# print(type(A[0]))
# <class 'scipy.sparse.csr.csr_matrix'>
# print(A[0].shape) (1,1000)
# print("TRAIN DATA TYPE")
# print(type(train_data))    <class 'scipy.sparse.csr.csr_matrix'>
# print(type(train_data[0]))    <class 'scipy.sparse.csr.csr_matrix'>
# print(train_data[0].shape) (1,1000)
x = train_data.toarray()
# print("TRAIN DATA.toArray TYPE")
# print(type(x))  <class 'numpy.ndarray'>
# print("TRAIN DATA.toArray[0] TYPE")
# print(type(x[0])) <class 'numpy.ndarray'>
# print(x[0].shape) (1000,)
y = coarsening.perm_data(x, perm)
# print("COARSENED TYPE")
# print(y.shape) (9922, 1000)
# print(type(y)) <class 'numpy.ndarray'>
# print(type(y[0])) <class 'numpy.ndarray'>
# print(y[0].shape) (1000,)
train_data = scipy.sparse.csr_matrix(y)
# print("TRAIN DATA")
# print(train_data.shape) (9922, 1000)
# print(train_labels.shape) (9922,)

test_data = scipy.sparse.csr_matrix(coarsening.perm_data(test_data.toarray(), perm))
del perm
# #
# # print(type(train_data))
# # print(type(test_data))
# # print(type(test_labels))
# # print(type(train_labels))
# #
# # print(train_data)
# # print(train_labels)
# #
# # print(train_data.shape)
# # print(train_labels.shape)
#
# #
# # Validation set.
if False:
    val_data = train_data[:FLAGS.val_size,:]
    val_labels = train_labels[:FLAGS.val_size]
    train_data = train_data[FLAGS.val_size:,:]
    train_labels = train_labels[FLAGS.val_size:]
else:
    val_data = test_data
    val_labels = test_labels
#
#
# print("TRAIN BASELINE")
#
# print(train_data.shape)
# print(test_data.shape)
# print(val_data.shape)
#
# print()
# print(train_data[0].shape)
#
# print(type(train_data))
# print(type(test_data[0]))

if True:
    utils.baseline(train_data, train_labels, test_data, test_labels)

common = {}
common['dir_name']       = '20news/'
common['num_epochs']     = 80
common['batch_size']     = 100
common['decay_steps']    = len(train_labels) / common['batch_size']
common['eval_frequency'] = 5 * common['num_epochs']
common['filter']         = 'chebyshev5'
common['brelu']          = 'b1relu'
common['pool']           = 'mpool1'
C = max(train_labels) + 1  # number of classes

model_perf = utils.model_perf()



if True:
    name = 'softmax'
    params = common.copy()
    params['dir_name'] += name
    params['regularization'] = 0
    params['dropout']        = 1
    params['learning_rate']  = 1e3
    params['decay_rate']     = 0.95
    params['momentum']       = 0.9
    params['F']              = []
    params['K']              = []
    params['p']              = []
    params['M']              = [C]
    model_perf.test(models.cgcnn(L, **params), name, params,
                    train_data, train_labels, val_data, val_labels, test_data, test_labels)