from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

import dataset_tools.dataset_functions as ds

dataset = "/var/storage/miteyan/Dissertation/project/data/age_datasets/dataset.csv"
# dataset = "/var/storage/miteyan/Dissertation/project/data/age_datasets/week_clustered_dataset.csv"

train_dataset, test_dataset, valid_dataset = ds.get_data(dataset, 0.1, 0.2, 0.2)
# a = ds.get_balanced_data(dataset)
print(len(ds.get_all_data(dataset, 0)))
train_labels, train_dataset = ds.get_labels_and_features(train_dataset)
test_labels, test_dataset = ds.get_labels_and_features(test_dataset)
valid_labels, valid_dataset = ds.get_labels_and_features(valid_dataset)

# clf = RandomForestClassifier(max_depth=6, random_state=2)
clf = RandomForestClassifier(bootstrap= False, max_depth= 3, criterion = 'gini', max_features = 5)

clf.fit(train_dataset, train_labels.ravel())

test_predictions = clf.predict(test_dataset)
test_acc = ds.accuracy(test_predictions, test_labels)

val_predictions = clf.predict(valid_dataset)

cv_acc = ds.accuracy(val_predictions, test_labels)

print(cv_acc)
print(test_acc)

micro = f1_score(test_labels, test_predictions, average='micro')
macro = f1_score(test_labels, test_predictions, average='macro')
weighted = f1_score(test_labels, test_predictions, average='weighted')

print(micro, macro, weighted)