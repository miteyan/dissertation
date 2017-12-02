import numpy as np
import tensorflow as tf

test = "/var/storage/miteyan/Dissertation/project/data/genderdata/test"
train = "/var/storage/miteyan/Dissertation/project/data/genderdata/train"
test_data = np.genfromtxt(test, delimiter='\t')
train_data = np.genfromtxt(train, delimiter='\t')

# Create the model
x = tf.placeholder(tf.float32, [None, 26])
W = tf.Variable(tf.zeros([26, 2]))
b = tf.Variable(tf.zeros([2]))
y = tf.matmul(x, W) + b

y_ = tf.placeholder(tf.float32, [None, 2])

cross_entropy = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

sess = tf.InteractiveSession()
tf.global_variables_initializer().run()
# Train
for _ in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

# Test trained model
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print(sess.run(accuracy, feed_dict={x: .test.images,
                                    y_: mnist.test.labels}))
