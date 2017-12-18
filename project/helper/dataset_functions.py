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
    if test+valid < 1 and test >= 0 and valid >= 0:
        return np.split(array, [int(1-(test+valid) * len(array)), int((1-valid) * len(array))])
    else:
        raise Exception('Train, test, valid percents do not add to 100')


def get_data(file, feature_threshold, test_split, valid_split):
    array = get_array(file)
    np.random.shuffle(array)
    return split_train_test_valid(remove_features(scale_array(array), feature_threshold), test_split, valid_split)

def get_all_data(file, feature_threshold):
    array = get_array(file)
    np.random.shuffle(array)
    return remove_features(scale_array(array), feature_threshold)


def get_k_fold_validation(file, k):
    array = get_array(file)
    l = len(array)
    print(l)
    block_size = int(l / k)
    k_fold_array = []
    for i in range(0, k):
        k_fold_array.insert(i,array[i*block_size:(i+1)*block_size])
    # add remaining to first block
    for j in range(k*block_size, l):
        k_fold_array[0].append(array[j])
    return k_fold_array


def get_k_train(array, k_to_exclude):
    ret = []
    k = 0
    for i in range(0, len(array)):
        if i != k_to_exclude:
            for j in range(0,len(array[i])):
                ret[k] = array[i][j]
                k += 1
    return ret



def get_random_test_data(file, split):
    array = get_array(file)
    np.random.shuffle(array)
    return array[:int(len(array)*split)]


def get_labels_and_features(dataset):
    labels = get_labels(dataset)
    features = dataset[:, 1:]
    return labels, features


# utility function to calculate accuracy
def accuracy(predictions, test_labels):
    correctly_predicted = 0
    for i in range(0, len(test_labels)):
        if predictions[i] == test_labels[i]:
            correctly_predicted += 1

    return correctly_predicted*100/predictions.shape[0]

