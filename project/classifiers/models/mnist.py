import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

x = tf.placeholder(tf.float32, [None, 784])

n_nodes_hl1 = 70
n_nodes_hl2 = 35
n_classes = 10
num_features = 784
y_ = tf.placeholder(tf.float32, [None, 10])


def neural_network_model(data):
    hidden_1_layer = {'weights': tf.Variable(tf.random_normal([num_features, n_nodes_hl1])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl1]))}

    hidden_2_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl1, n_nodes_hl2])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl2]))}
    output_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl2, n_classes])),
                    'biases': tf.Variable(tf.random_normal([n_classes]))}
    l1 = tf.add(tf.matmul(data, hidden_1_layer['weights']),
                hidden_1_layer['biases'])
    l1 = tf.nn.relu(l1)
    l2 = tf.add(tf.matmul(l1, hidden_2_layer['weights']),
                hidden_2_layer['biases'])
    l2 = tf.nn.relu(l2)
    output = tf.add(tf.matmul(l2, output_layer['weights']),
                    output_layer['biases'])
    return output


def train_neural_network(x):
    prediction = neural_network_model(x)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y_))
    optimizer = tf.train.GradientDescentOptimizer(0.05).minimize(cost)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        loss = 0
        for _ in range(30):
            for _ in range(1000):
                batch_xs, batch_ys = mnist.train.next_batch(100)
                _, l = sess.run([optimizer, cost], feed_dict={x: batch_xs, y_: batch_ys})
                loss += l
        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))

        test_dataset, test_labels = mnist.test.next_batch(1000)
        print('Test Accuracy:',  accuracy.eval({x: test_dataset, y_: test_labels}))

train_neural_network(x)