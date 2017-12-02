import numpy as np
from sklearn.naive_bayes import GaussianNB

train = "/var/storage/miteyan/Dissertation/project/data/train.csv"
test = "/var/storage/miteyan/Dissertation/project/data/test.csv"
valid = "/var/storage/miteyan/Dissertation/project/data/valid.csv"

clf = GaussianNB()


def get_labels(array):
    x = np.zeros(shape=(len(array)))
    for i in range(0,len(array)):
        x[i] = array[i][0]
    return x



# 2D array of labels and features
test_dataset = np.genfromtxt(test, delimiter='	')
test_labels = get_labels(test_dataset)
test_dataset = test_dataset[:, 1:]

train_dataset = np.genfromtxt(train, delimiter='\t')
train_labels = get_labels(train_dataset)
train_dataset = train_dataset[:, 1:]
train_size = len(train_dataset)


valid_dataset = np.genfromtxt(valid, delimiter='\t')
valid_labels = get_labels(valid_dataset)
valid_dataset = valid_dataset[:, 1:]

np.nan_to_num(train_dataset)
np.nan_to_num(train_labels)

clf.fit(train_dataset, train_labels)
print(clf.predict(test_dataset, test_labels))
