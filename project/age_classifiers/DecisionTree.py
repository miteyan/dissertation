from sklearn import tree
import helper.dataset_functions as ds

dataset = "/var/storage/miteyan/Dissertation/project/data/age_datasets/dataset.csv"

train_dataset, test_dataset, valid_dataset = ds.get_data(dataset, 0.2, 0.2, 0.05)

train_labels, train_dataset = ds.get_labels_and_features(train_dataset)
valid_labels, valid_dataset = ds.get_labels_and_features(valid_dataset)
test_labels, test_dataset = ds.get_labels_and_features(test_dataset)

clf = tree.DecisionTreeClassifier()

clf.fit(train_dataset, train_labels.ravel())

# Cross validation
cv_prediction = clf.predict(valid_dataset)
cv_acc = ds.accuracy(cv_prediction, valid_labels)
print(cv_acc)

# Test error
test_prediction = clf.predict(test_dataset)
test_acc = ds.accuracy(test_prediction, test_labels)
print(test_acc)

# k fold validation
k = 5

sum = 0

for i in range(0,k):
    train_dataset, test_dataset, valid_dataset = ds.get_data(dataset, 0.2, 0.2, 0.05)

    train_labels, train_dataset = ds.get_labels_and_features(train_dataset)
    valid_labels, valid_dataset = ds.get_labels_and_features(valid_dataset)
    test_labels, test_dataset = ds.get_labels_and_features(test_dataset)

    clf = tree.DecisionTreeClassifier()

    clf.fit(train_dataset, train_labels.ravel())

    # Cross validation
    cv_prediction = clf.predict(valid_dataset)
    cv_acc = ds.accuracy(cv_prediction, valid_labels)
    print(cv_acc)

    # Test error
    test_prediction = clf.predict(test_dataset)
    test_acc = ds.accuracy(test_prediction, test_labels)
    print(test_acc)
    sum += test_acc

print(sum/k)
