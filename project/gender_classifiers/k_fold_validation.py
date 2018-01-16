import helper.dataset_functions as ds
from sklearn.model_selection import KFold
from sklearn import tree

dataset = "/var/storage/miteyan/Dissertation/project/data/genderdata/weekly_dataset.csv"

train_dataset = ds.get_all_data(dataset, 0.05)

y, X = ds.get_labels_and_features(train_dataset)

k = 5

kf = KFold(n_splits=k)

sum = 0

batches = 10
for i in range(0, batches):

    for train_index, test_index in kf.split(X):

        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        # Carry out train and test here

        clf = tree.DecisionTreeClassifier()

        clf.fit(X_train, y_train.ravel())

        predictions = clf.predict(X_test)
        acc = ds.accuracy(predictions, y_test)
        sum += acc

print(sum/(k*batches))