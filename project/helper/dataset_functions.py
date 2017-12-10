import numpy as np
from sklearn.feature_selection import VarianceThreshold
from sklearn.preprocessing import StandardScaler


def get_labels(array):
    x = np.zeros(shape=(len(array), 1))
    for i in range(0,len(array)):
        if array[i][0] > 0:
            x[i] = 1
        else:
            x[i] = 0
    return x

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
    return scaler.fit_transform(array)


def remove_features(array, threshold):
    if threshold>1 or threshold < 0:
        raise Exception('Threshold should be within [0,1]')
    return VarianceThreshold(threshold=(threshold*(1-threshold))).fit_transform(array)


def split_train_test_valid(array, test, valid):
    if test+valid < 1 and test>0 and valid > 0:
        return np.split(array, [int(1-(test+valid) * len(array)), int((1-valid) * len(array))])
    else:
        raise Exception('Train, test, valid percents do not add to 100')


def get_data(file, feature_threshold, test_split, valid_split):
    array = get_array(file)
    np.random.shuffle(array)
    return split_train_test_valid(remove_features(scale_array(array), feature_threshold), test_split, valid_split)


def get_labels_and_features(dataset):
    print(dataset)
    labels = get_labels(dataset)
    print(labels)
    features = dataset[:, 1:]
    return labels, features


# utility function to calculate accuracy
def accuracy(predictions, test_labels):
    correctly_predicted = 0
    for i in range(0, len(test_labels)):
        if predictions[i] == test_labels[i]:
            correctly_predicted += 1

    return correctly_predicted*100/predictions.shape[0]

