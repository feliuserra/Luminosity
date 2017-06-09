import tensorflow as tf
from lagged_feature_loader import LaggedFeatureLoader, WrongImageSize


learning_rate = 0.005
max_iter = 400000 * 10
batch_size = 100
display_batch = 5
n = m = 200
lags = 3

feature_loader = LaggedFeatureLoader(lags=lags, img_shape=(n, m),
                                     check_integrity=True,
                                     batch_size=batch_size)


def init_weights(shape):
    weights = tf.random_normal(shape, stddev=0.1)
    return tf.Variable(weights)


X = tf.placeholder(tf.float32, [None, n, m, lags])
Y = tf.placeholder(tf.float32, [None, n, m])


def create_network(features):
    input_layer = tf.reshape(features,
                             [batch_size, n, m, lags])
    first_layer = tf.layers.dense(inputs=input_layer,
                                  units=3,
                                  activation=tf.nn.sigmoid,
                                  name='first_layer')
    output_layer = tf.layers.dense(inputs=first_layer,
                                   units=1,
                                   activation=tf.nn.relu,
                                   name='output_layer')
    return output_layer


network = create_network(X)
square_errors = tf.squared_difference(network, Y)
cost = tf.reduce_mean(tf.cast(square_errors, tf.float32))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
init = tf.global_variables_initializer()


log_path = 'models/simple_feed_forward/log'
open(log_path, 'w').close()
with tf.Session() as sess:
    saver = tf.train.Saver()
    sess.run(init)
    batch = 1
    while batch * batch_size < max_iter:
        try:
            batch_features, batch_targets = feature_loader.load_batch()
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
                with open(log_path, 'a') as log:
                    print(loss, file=log)
        except WrongImageSize as e:
            print(e)
            pass
        except IndexError as e:
            print(e)
            batch = max_iter
            pass

        batch += 1
    print("Optimization Finished!")
