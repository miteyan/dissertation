from time import time

import numpy as np
import tensorflow as tf
from sklearn.feature_selection import VarianceThreshold
from sklearn.preprocessing import StandardScaler

import dataset_tools.dataset_functions as ds

# dataset2 = "/var/storage/miteyan/Dissertation/project/data/age_datasets/dataset.csv"
# dataset2 = "/var/storage/miteyan/Dissertation/project/data/emotion_sense_dataset.csv"
# dataset2 = "/var/storage/miteyan/Dissertation/project/data/genderdata/weekly_dataset.csv"
dataset = "/var/storage/miteyan/Dissertation/project/data/synthetic_graphs/d"

learning_rate = 0.01
# Network Parameters
n_hidden_1 = 15
n_hidden_2 = 5
num_input = 19
num_classes = 2


def scale_array(array):
    scaler = StandardScaler()
    return np.float32(scaler.fit_transform(array))


def remove_features(array, threshold):
    if threshold > 1 or threshold < 0:
        raise Exception('Threshold should be within [0,1]')
    return VarianceThreshold(threshold=(threshold * (1 - threshold))).fit_transform(array)


def split_train_test_valid(array, test, valid):
    if test + valid < 1 and test > 0 and valid > 0:
        return np.split(array, [int(1 - (test + valid) * len(array)), int((1 - valid) * len(array))])
    else:
        raise Exception('Train, test, valid percents do not add to 100')


def get_labels(array):
    x = np.zeros(shape=(len(array), 2))
    for i in range(0, len(array)):
        if array[i][0] < 0:
            x[i] = np.array([1, 0])
        else:
            x[i] = np.array([0, 1])
    return x


def confusion_matrix(predictions, labels):
    matrix = np.zeros((2, 2))
    for i in range(0, len(predictions)):
        if labels[i][0] == 1:
            label = 0
        else:
            label = 1
        if predictions[i][0] > predictions[i][1]:
            prediction = 0
        else:
            prediction = 1
        if label == 1 and prediction == 1:
            matrix[1][1] += 1
        elif label == 0 and prediction == 0:
            matrix[0][0] += 1
        elif label == 0 and prediction == 1:
            matrix[0][1] += 1
        else:
            matrix[1][0] += 1
    return matrix


# 2D array of labels and features
data = ds.get_balanced_data(dataset)
# Scale the data to have a 0 mean
data = scale_array(data)
# Remove feature through feature selection that have a low variance of 5% between data
data = remove_features(data, 0)
data_size = len(data[0])
# number of features - first column is the label
num_features = data_size - 1
# number of target labels
data = np.array(data)
np.random.shuffle(data)

train_dataset, test_dataset, valid_dataset = split_train_test_valid(data, 0.2, 0.2)

test_labels = get_labels(test_dataset)
test_dataset = test_dataset[:, 1:]

train_labels = get_labels(train_dataset)
train_dataset = train_dataset[:, 1:]

valid_labels = get_labels(valid_dataset)
valid_dataset = valid_dataset[:, 1:]

train_size = len(train_dataset)
n_nodes_hl1 = 15
n_nodes_hl2 = 10
n_nodes_hl3 = 5

n_classes = 2

x = tf.placeholder('float', [None, num_features])
y = tf.placeholder('float')


# def print_shape(obj):
#     print(obj.get_shape().as_list())


def neural_network_model(data):
    hidden_1_layer = {'weights': tf.Variable(tf.random_normal([num_features, n_nodes_hl1])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl1]))}

    hidden_2_layer = {'weights':
                          tf.Variable(tf.random_normal([n_nodes_hl1, n_nodes_hl2])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl2]))}

    hidden_3_layer = {'weights':
                          tf.Variable(tf.random_normal([n_nodes_hl2, n_nodes_hl3])),
                      'biases':
                          tf.Variable(tf.random_normal([n_nodes_hl3]))}

    output_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl3,
                                                             n_classes])),
                    'biases': tf.Variable(tf.random_normal([n_classes]))}
    l1 = tf.add(tf.matmul(data, hidden_1_layer['weights']),
                hidden_1_layer['biases'])
    l1 = tf.nn.relu(l1)
    l2 = tf.add(tf.matmul(l1, hidden_2_layer['weights']),
                hidden_2_layer['biases'])
    l2 = tf.nn.relu(l2)

    l3 = tf.add(tf.matmul(l2, hidden_3_layer['weights']),
                hidden_3_layer['biases'])
    l3 = tf.nn.relu(l3)

    output = tf.add(tf.matmul(l3, output_layer['weights']),
                    output_layer['biases'])

    return output


def train_neural_network(x):
    prediction = neural_network_model(x)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits
                          (logits=prediction, labels=y))
    optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)
    hm_epochs = 15
    start = time()

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        for epoch in range(hm_epochs):
            loss = 0
            for _ in range(train_size):
                _, l = sess.run([optimizer, cost], feed_dict={x: train_dataset, y: train_labels})
                loss += l
            # print('Epoch', epoch, 'completed out of', hm_epochs, 'loss:',
            #       loss)
        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))


        print('Train Accuracy:', accuracy.eval({x: train_dataset, y: train_labels}))
        print('Valid Accuracy:', accuracy.eval({x: valid_dataset, y: valid_labels}))
        print('Test Accuracy:', accuracy.eval({x: test_dataset, y: test_labels}))
        predictions = sess.run(prediction, {x: test_dataset})
        # print(time()-start)
        # print(predictions)
        return confusion_matrix(predictions, test_labels)
        # recall, recall_op = tf.metrics.recall(labels=test_labels, predictions=predictions)
        # sess.run(recall_op, )


def prf(confusion):
    tp = confusion[1][1]
    tn = confusion[0][0]
    fp = confusion[0][1]
    fn = confusion[1][0]
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    f1 = 2*precision*recall/(precision+recall)
    return recall, precision, f1

ps = []
rs = []
fs = []
for i in range (5):
    confusion = train_neural_network(x)
    r, p, f = precision_recall_f1 = prf(confusion)
    ps.append(p)
    rs.append(r)
    fs.append(f)
print([np.mean(rs), np.sqrt(np.var(rs))])
print([np.mean(ps), np.sqrt(np.var(ps))])
print([np.mean(fs), np.sqrt(np.var(fs))])