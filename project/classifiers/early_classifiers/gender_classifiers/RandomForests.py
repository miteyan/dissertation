from sklearn.ensemble import RandomForestClassifier

import dataset_tools.dataset_functions as ds

# dataset = "/var/storage/miteyan/Dissertation/project/data/genderdata/weekly_dataset.csv"
dataset = "/var/storage/miteyan/Dissertation/project/data/age_datasets/week_clustered_dataset.csv"

train_dataset, test_dataset, valid_dataset = ds.get_data(dataset, 0.05, 0.2, 0.2)

train_labels, train_dataset = ds.get_labels_and_features(train_dataset)
test_labels, test_dataset = ds.get_labels_and_features(test_dataset)
valid_labels, valid_dataset = ds.get_labels_and_features(valid_dataset)

clf = RandomForestClassifier(max_depth=6, random_state=2)

clf.fit(train_dataset, train_labels.ravel())

predictions = clf.predict(test_dataset)
acc = ds.accuracy(predictions, test_labels)

print(acc)