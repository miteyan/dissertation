import helper.dataset_functions as ds
from sklearn.ensemble import RandomForestClassifier

# dataset = "/var/storage/miteyan/Dissertation/project/data/age_datasets/dataset.csv"
dataset = "/var/storage/miteyan/Dissertation/project/data/age_datasets/week_clustered_dataset.csv"

train_dataset, test_dataset, valid_dataset = ds.get_data(dataset, 0.1, 0.2, 0.2)

train_labels, train_dataset = ds.get_labels_and_features(train_dataset)
test_labels, test_dataset = ds.get_labels_and_features(test_dataset)
valid_labels, valid_dataset = ds.get_labels_and_features(valid_dataset)

clf = RandomForestClassifier(max_depth=6, random_state=2)

clf.fit(train_dataset, train_labels.ravel())

test_predictions = clf.predict(test_dataset)
test_acc = ds.accuracy(test_predictions, test_labels)

val_predictions = clf.predict(valid_dataset)

cv_acc = ds.accuracy(val_predictions, test_labels)

print(cv_acc)
print(test_acc)