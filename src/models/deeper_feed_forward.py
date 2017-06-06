import tensorflow as tf
from tensorflow.contrib import learn
from learn.python.learn.estimators import model_fn
from feature_loader import FeatureTensorLoader

learning_rate = 0.001
batch_size = 100
n = m = 300
lags = 3

feature_loader = FeatureTensorLoader(lags=lags,
                                     check_integrity=True,
                                     batch_size=batch_size)


def init_weights(shape):
    weights = tf.random_normal(shape, stddev=0.1)
    return tf.Variable(weights)


X = tf.placeholder(tf.float32, [None, n, m, lags])
Y = tf.placeholder(tf.float32, [None, n, m])


def luminosity_network(features, target, mode):
    input_layer = tf.reshape(features,
                             [batch_size, n, m, lags])
    first_layer = tf.layers.dense(inputs=input_layer,
                                  units=n,
                                  activation=tf.nn.relu,
                                  name='first_layer')
    second_layer = tf.layers.dense(inputs=first_layer,
                                   units=m,
                                   activation=tf.nn.relu,
                                   name='second_layer')
    third_layer = tf.layers.dense(inputs=second_layer,
                                  units=90,
                                  activation=tf.nn.relu,
                                  name='third_layer')
    fourth_layer = tf.layers.dense(inputs=third_layer,
                                   units=1,
                                   activation=tf.nn.relu,
                                   name='fourth_layer')
    output_layer = tf.reshape(tf.nn.sigmoid(fourth_layer, name='output_layer'),
                              [batch_size, n, m])
    if mode != learn.ModeKeys.INFER:
        square_errors = tf.squared_difference(output_layer, Y)
        loss = tf.reduce_mean(tf.cast(square_errors, tf.float32))

    if mode == learn.ModeKeys.TRAIN:
        train_op = tf.contrib.layers.optimize_loss(
            loss=loss,
            global_step=tf.contrib.framework.get_global_step(),
            learning_rate=learning_rate,
            optimizer="Adam")

    predictions = {
        'raster': output_layer
    }

    return model_fn.ModelFnOps(mode=mode,
                               predictions=predictions,
                               loss=loss,
                               train_op=train_op)


deeper_feed_forward = learn.Estimator(
    model_fn=luminosity_network,
    model_dir="/models/deeper_feed_forward")


deeper_feed_forward.fit(
    x=feature_loader.batch_x_iterator,
    y=feature_loader.batch_y_iterator,
    batch_size=batch_size,
    steps=20000)


metrics = {
    "mse": learn.MetricSpec(metric_fn=tf.metrics.mean_squared_error,
                            prediction_key="raster")
}

test_features, test_targets = feature_loader.load_batch(100)
eval_results = deeper_feed_forward.evaluate(
    x=test_features, y=test_targets, metrics=metrics)
print(eval_results)
