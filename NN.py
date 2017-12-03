import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import numpy as np

TRAIN_FILE = "train.csv"
TEST_FILE = "validate.csv"


def train(training_set):
    # Specify that all features have real-value data
    feature_columns = [tf.feature_column.numeric_column("x", shape=[5])]

    # Build 3 layer DNN with 10, 20, 10 units respectively.
    classifier = tf.estimator.DNNClassifier(feature_columns=feature_columns,
                                            hidden_units=[10, 20, 10],
                                            n_classes=2,
                                            model_dir="/save/model")
    # Define the training inputs
    train_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": np.array(training_set.data)},
        y=np.array(training_set.target),
        num_epochs=None,
        shuffle=True)

    # Train model.
    classifier.train(input_fn=train_input_fn, steps=2000)


def test(test_file):
    test_set = tf.contrib.learn.datasets.base.load_csv_with_header(
        filename=test_file,
        target_dtype=np.int,
        features_dtype=np.float32)

    # Specify that all features have real-value data
    feature_columns = [tf.feature_column.numeric_column("x", shape=[5])]

    # Build 3 layer DNN with 10, 20, 10 units respectively.
    classifier = tf.estimator.DNNClassifier(feature_columns=feature_columns,
                                            hidden_units=[10, 20, 10],
                                            n_classes=2,
                                            model_dir="/save/model")

    # Define the test inputs
    test_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": np.array(test_set.data)},
        y=np.array(test_set.target),
        num_epochs=1,
        shuffle=False)

    # Evaluate accuracy.
    accuracy_score = classifier.evaluate(input_fn=test_input_fn)["accuracy"]

    print("\nTest Accuracy: {0:f}\n".format(accuracy_score))


def predict(sample):
    predict_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": sample},
        num_epochs=1,
        shuffle=False)

    feature_columns = [tf.feature_column.numeric_column("x", shape=[5])]
    classifier = tf.estimator.DNNClassifier(feature_columns=feature_columns,
                                            hidden_units=[10, 20, 10],
                                            n_classes=2,
                                            model_dir="/save/model")

    predictions = list(classifier.predict(input_fn=predict_input_fn))
    #predicted_classes = [p["classes"] for p in predictions]
    return predictions[0]['probabilities'][1]

if __name__ == '__main__':
    # Load datasets.
    training_set = tf.contrib.learn.datasets.base.load_csv_with_header(
        filename=TRAIN_FILE,
        target_dtype=np.int,
        features_dtype=np.float32)


    train(training_set)
    test(TEST_FILE)
