from sklearn import tree
import helper.dataset_functions as ds

dataset = "/var/storage/miteyan/Dissertation/project/data/genderdata/weekly_dataset.csv"

train_dataset, test_dataset, valid_dataset = ds.get_data(dataset, 0.8, 0.2, 0.05)

print(len(test_dataset[0]))
print(test_dataset[0])
train_labels, train_dataset = ds.get_labels_and_features(train_dataset)
test_labels, test_dataset = ds.get_labels_and_features(test_dataset)
valid_labels, valid_dataset = ds.get_labels_and_features(valid_dataset)

clf = tree.DecisionTreeClassifier()

clf.fit(train_dataset, train_labels.ravel())

predictions = clf.predict(test_dataset)
acc = ds.accuracy(predictions, test_labels)

print(acc)