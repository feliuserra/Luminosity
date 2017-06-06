import numpy as np
import tensorflow as tf
from feature_loader import FeatureTensorLoader, WrongImageSize


learning_rate = 0.001
max_iter = 10
batch_size = 2
display_batch = 5
n = m = 300
lags = 3

feature_loader = FeatureTensorLoader(lags=lags,
                                     check_integrity=True,
                                     batch_size=batch_size)


def init_weights(shape):
    weights = tf.random_normal(shape, stddev=0.1)
    return tf.Variable(weights)


X = tf.placeholder(tf.float32, [n, m, lags])
Y = tf.placeholder(tf.float32, [n, m])


def create_network(features):
    input_layer = tf.reshape(features,
                             [-1, n, m, lags])
    first_layer = tf.layers.dense(inputs=input_layer,
                                  units=n*m,
                                  activation=tf.nn.relu,
                                  name='first_layer')
    second_layer = tf.layers.dense(inputs=first_layer,
                                   units=n*m,
                                   activation=tf.nn.relu,
                                   name='second_layer')
    output_layer = tf.reshape(tf.nn.sigmoid(second_layer, name='output'),
                              [n, m])
    return output_layer


network = create_network(X)
square_errors = tf.nn.l2_loss(t=network)
cost = tf.reduce_mean(tf.cast(square_errors, tf.float32))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
init = tf.global_variables_initializer()


with tf.Session() as sess:
    saver = tf.train.Saver()
    sess.run(init)
    batch = 1
    while batch < max_iter:
        try:
            batch_features, batch_targets = feature_loader.load(batch)
            sess.run(optimizer, feed_dict={X: batch_features,
                                           Y: batch_targets})
            if batch % display_batch == 0:
                # Calculate batch loss and accuracy
                loss = sess.run(cost, feed_dict={X: batch_features,
                                                 Y: batch_targets})
                saver.save(sess,
                           'models/simple_feed_forward/' +
                           'simple_feed_forward_session')
                print("Batch = {}, Loss = {:.2f}".format(batch, loss))
        except WrongImageSize:
            print('Image was not consistent with required dimension')
            pass

        batch += 1
    print("Optimization Finished!")
    test_features, test_targets = feature_loader.load(max(max_iter, batch))
    np.save('models/simple_feed_forward/' +
            'simple_feed_forward_prediction.npy',
            np.array(network.eval(feed_dict={X: test_features}).tolist()))
