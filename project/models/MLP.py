import tensorflow as tf
import numpy as np
from sklearn.feature_selection import VarianceThreshold
from sklearn.preprocessing import StandardScaler


# dataset = "/var/storage/miteyan/Dissertation/project/data/age_datasets/dataset.csv"
# dataset2 = "/var/storage/miteyan/Dissertation/project/data/emotion_sense_dataset.csv"
dataset = "/var/storage/miteyan/Dissertation/project/data/genderdata/weekly_dataset.csv"

def get_array(file):
    arr = []
    with open(file, encoding='utf-16') as f:
        read_data = f.read()
        for line in read_data.splitlines():
            features = [np.float32(x) for x in line.split(",")]

            arr.append(features)
    f.close()
    return arr


def scale_array(array):
    scaler = StandardScaler()
    return np.float32(scaler.fit_transform(array))


def remove_features(array, threshold):
    if threshold>1 or threshold < 0:
        raise Exception('Threshold should be within [0,1]')
    return VarianceThreshold(threshold=(threshold*(1-threshold))).fit_transform(array)


def split_train_test_valid(array, test, valid):
    if test+valid < 1 and test>0 and valid > 0:
        return np.split(array, [int(1-(test+valid) * len(array)), int((1-valid) * len(array))])
    else:
        raise Exception('Train, test, valid percents do not add to 100')


def get_labels(array):
    x = np.zeros(shape=(len(array), 2))
    for i in range(0,len(array)):
        if array[i][0] < 0:
            x[i] = np.array([1, 0])
        else:
            x[i] = np.array([0, 1])
    return x

# utility function to calculate accuracy
def accuracy(predictions, labels):
    correctly_predicted = np.sum(np.argmax(predictions, 1) == np.argmax(labels, 1))
    accu = (100.0 * correctly_predicted) / predictions.shape[0]
    return accu

# 2D array of labels and features
data = get_array(dataset)
np.random.shuffle(np.array(data))
# Scale the data to have a 0 mean
data = scale_array(data)
# Remove feature through feature selection that have a low variance of 5% between data
data = remove_features(data, threshold=0.05)
data_size = len(data[0])
# number of features - first column is the label
num_features = 19
# number of target labels
num_labels = 2
# learning rate (alpha)
learning_rate = 0.04

train_dataset, test_dataset, valid_dataset = split_train_test_valid(data, 0.2, 0.2)

test_labels = get_labels(test_dataset)
test_dataset = test_dataset[:, 1:]

train_labels = get_labels(train_dataset)
train_dataset = train_dataset[:, 1:]

valid_labels = get_labels(valid_dataset)
valid_dataset = valid_dataset[:, 1:]

train_size = len(train_dataset)

# initialize a tensorflow graph
graph = tf.Graph()

# Create model
def multilayer_perceptron(x):
    # Network Parameters
    n_hidden_1 = 10  # 1st layer number of neurons
    n_hidden_2 = 5  # 2nd layer number of neurons
    n_input = 19  # MNIST data input (img shape: 28*28)
    n_classes = 2  # MNIST total classes (0-9 digits)
    weights = {
        'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
        'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
        'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes]))
    }
    biases = {
        'b1': tf.Variable(tf.random_normal([n_hidden_1])),
        'b2': tf.Variable(tf.random_normal([n_hidden_2])),
        'out': tf.Variable(tf.random_normal([n_classes]))
    }
    # Hidden fully connected layer with 256 neurons
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    # Hidden fully connected layer with 256 neurons
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    # Output fully connected layer with a neuron for each class
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer

with graph.as_default():
    """
    defining all the nodes
    """
    # Inputs
    tf_train_dataset = tf.placeholder(tf.float32, shape=(train_size, num_features))
    tf_train_labels = tf.placeholder(tf.float32, shape=(train_size, num_labels))
    tf_valid_dataset = tf.constant(valid_dataset)
    tf_valid_labels = tf.constant(valid_labels)
    tf_test_dataset = tf.constant(test_dataset)
    tf_test_labels = tf.constant(test_labels)

    # Variables.
    # Training computation.
    logits = multilayer_perceptron(tf_train_dataset)
    # logits = tf.matmul(tf_train_dataset, weights) + biases
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
        labels=tf_train_labels, logits=logits))
    # Optimizer.
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)

    # Predictions for the training, validation, and test data.
    train_prediction = tf.nn.softmax(logits)

with tf.Session(graph=graph) as session:
    # initialize weights and biases
    tf.global_variables_initializer().run()
    print("Initialized")
    # Prepare the feed dict
    feed_dict = {tf_train_dataset: train_dataset,
                 tf_train_labels: train_labels}
    # run one step of computation
    _, l, predictions = session.run([optimizer, loss, train_prediction],
                                    feed_dict=feed_dict)
    # Training cycle
    for epoch in range(11):
        # Loop over all batches
        # Run optimization op (backprop) and cost op (to get loss value)
        _, l, predictions = session.run([optimizer, loss, train_prediction],
                                        feed_dict=feed_dict)
        # Compute average loss
        print("\n loss at step {0}: {1}".format(0, l))
        print("Train accuracy: {:.1f}%".format(accuracy(predictions, train_labels)))

    print("Optimization Finished!")
    # print("\nTest accuracy: {:.1f}%".format(accuracy(test_prediction.eval(), test_labels)))
    # print("Validation accuracy: {:.1f}%".format(accuracy(valid_prediction.eval(), valid_labels)))

    pred = tf.nn.softmax(logits)  # Apply softmax to logits
    correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(tf_train_labels, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print("Train Accuracy:", accuracy.eval({tf_train_dataset: train_dataset, tf_train_labels: train_labels}))
    correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(tf_test_labels, 1))

