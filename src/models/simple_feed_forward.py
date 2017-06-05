import tensorflow as tf
from feature_loader import FeatureTensorLoader


learning_rate = 0.001
max_iter = 20000
batch_size = 200
display_batch = 10
n = m = 300
lags = 3

feature_loader = FeatureTensorLoader(lags=lags, check_integrity=True)


def init_weights(shape):
    weights = tf.random_normal(shape, stddev=0.1)
    return tf.Variable(weights)


X = tf.placeholder(tf.float32, [lags, n, m])
Y = tf.placeholder(tf.float32, [n, m])

# Store layers weight & bias
weights = {
    'w1': tf.Variable(
        tf.random_normal([lags, n, m])),
}

biases = {
    'b1': tf.Variable(tf.random_normal([n, m])),
}


def create_network(X, weights, biases):
    l1 = tf.nn.relu(X)
    l1 = tf.add(tf.matmul(l1, weights['w1']), biases['b1'])
    l1 = tf.nn.sigmoid(l1)
    return l1


network = create_network(X, weights, biases)
square_errors = tf.nn.l2_loss(t=network)
cost = tf.reduce_mean(tf.cast(square_errors, tf.float32))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
init = tf.global_variables_initializer()


with tf.Session() as sess:
    sess.run(init)
    batch = 1
    while batch < max_iter:
        batch_features, batch_targets = feature_loader.load(batch)
        sess.run(optimizer, feed_dict={X: batch_features,
                                       Y: batch_targets})
        if batch % display_batch == 0:
            # Calculate batch loss and accuracy
            loss = sess.run([cost], feed_dict={X: batch_features,
                                               Y: batch_targets})
            print(loss)
            print("Batch = {}, Loss = {:.2f}".format(batch, loss[0]))
        batch += 1
    print("Optimization Finished!")
