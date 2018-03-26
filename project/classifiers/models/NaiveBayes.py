from sklearn.model_selection import KFold
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB

import dataset_tools.dataset_functions as ds

dataset = ["/var/storage/miteyan/Dissertation/project/data/age_datasets/dataset.csv","/var/storage/miteyan/Dissertation/project/data/genderdata/weekly_dataset.csv", "/var/storage/miteyan/Dissertation/project/data/emotion_sense_dataset.csv", "/var/storage/miteyan/Dissertation/project/data/age_datasets/dataset.csv","/var/storage/miteyan/Dissertation/project/data/emotion_sense__multiclass_dataset.csv"]

clf = GaussianNB()

print(clf.get_params().keys())
# specify parameters and distributions to sample from

for i in range(0, len(dataset)):

    train_dataset = ds.get_all_data(dataset[i], 0.0)
    y, X = ds.get_labels_and_features(train_dataset)

    k = 10
    kf = KFold(n_splits=k)
    sum = 0

    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        # Carry out train and test here
        clf = BernoulliNB()

        clf.fit(X_train, y_train.ravel())

        predictions = clf.predict(X_test)
        acc = ds.accuracy(predictions, y_test)
        sum += acc

    print(dataset[i] + " " +str(sum/(k)))
