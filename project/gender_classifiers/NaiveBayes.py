from sklearn.naive_bayes import GaussianNB
import helper.dataset_functions as ds

# dataset = "/var/storage/miteyan/Dissertation/project/data/genderdata/dataset.csv"
dataset = "/var/storage/miteyan/Dissertation/project/data/genderdata/weekly_dataset.csv"

train_dataset, test_dataset, valid_dataset = ds.get_data(dataset, 0.1, 0.2, 0.2)

train_labels, train_dataset = ds.get_labels_and_features(train_dataset)
test_labels, test_dataset = ds.get_labels_and_features(test_dataset)
valid_labels, valid_dataset = ds.get_labels_and_features(valid_dataset)

clf = GaussianNB()

print(train_labels.size)
clf.fit(train_dataset, train_labels.ravel())

predictions = clf.predict(test_dataset)
acc = ds.accuracy(predictions, test_labels)
print(acc)

predictions = clf.predict(valid_dataset)
acc = ds.accuracy(predictions, valid_labels)
print(acc)