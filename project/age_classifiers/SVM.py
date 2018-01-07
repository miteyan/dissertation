import numpy as np
from sklearn.feature_selection import VarianceThreshold
from sklearn.preprocessing import StandardScaler
from sklearn import svm

dataset = "/var/storage/miteyan/Dissertation/project/data/age_datasets/dataset.csv"

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
    return split_train_test_valid(remove_features(scale_array(np.random.shuffle(np.array(get_array(file)))),
                                                  feature_threshold), test_split, valid_split)

def get_labels(array):
    x = np.zeros(shape=(len(array), 1))
    for i in range(0,len(array)):
        if array[i][0] > 0:
            x[i] = 1
        else:
            x[i] = 0
    return x

def get_labels_and_features(dataset):
    labels = get_labels(dataset)
    features = dataset[:, 1:]
    return labels, features

# 2D array of labels and features
data = get_array(dataset)
np.random.shuffle(np.array(data))
# Scale the data to have a 0 mean
data = scale_array(data)
# Remove feature through feature selection that have a low variance of 5% between data
data = remove_features(data, threshold=0.00)
data_size = len(data[0])
# number of features - first column is the label
num_features = data_size-1
# number of target labels
num_labels = 2
# learning rate (alpha)
learning_rate = 0.05

train_dataset, test_dataset, valid_dataset = split_train_test_valid(data, 0.2, 0.1)

test_labels = get_labels(test_dataset)
test_dataset = test_dataset[:, 1:]

train_labels = get_labels(train_dataset)
train_dataset = train_dataset[:, 1:]

valid_labels = get_labels(valid_dataset)
valid_dataset = valid_dataset[:, 1:]

train_size = len(train_dataset)


clf = svm.SVC()
clf.fit(train_dataset, train_labels)

predictions = clf.predict(test_dataset)

# utility function to calculate accuracy
def accuracy(predictions, labels):
    correctly_predicted = 0
    for i in range(0, len(labels)):
        if predictions[i] == labels[i]:
            correctly_predicted += 1

    return correctly_predicted*100/predictions.shape[0]


acc = accuracy(predictions, test_labels)
print(acc)