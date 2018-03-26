from itertools import cycle

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve
from sklearn.naive_bayes import GaussianNB

import dataset_tools.dataset_functions as ds

# dataset = "/var/storage/miteyan/Dissertation/project/data/genderdata/dataset.csv"
dataset = "/var/storage/miteyan/Dissertation/project/data/genderdata/weekly_dataset.csv"

train_dataset, test_dataset, valid_dataset = ds.get_data(dataset, 0.0, 0.2, 0.2)

train_labels, train_dataset = ds.get_labels_and_features(train_dataset)
test_labels, test_dataset = ds.get_labels_and_features(test_dataset)
valid_labels, valid_dataset = ds.get_labels_and_features(valid_dataset)

clf = GaussianNB()

print(train_labels.size)
print(len(train_dataset[0]))
clf.fit(train_dataset, train_labels.ravel())

predictions = clf.predict(test_dataset)
acc = ds.accuracy(predictions, test_labels)
print(acc)

predictions = clf.predict(valid_dataset)
acc = ds.accuracy(predictions, valid_labels)
print(acc)

fpr, tpr, thresholds = roc_curve(valid_labels, predictions)

# Plot all ROC curves
n_classes = 2

plt.figure()
roc_auc = dict()
plt.plot(fpr["micro"], tpr["micro"],
         label='micro-average ROC curve (area = {0:0.2f})'
               ''.format(roc_auc["micro"]),
         color='deeppink', linestyle=':', linewidth=4)

plt.plot(fpr["macro"], tpr["macro"],
         label='macro-average ROC curve (area = {0:0.2f})'
               ''.format(roc_auc["macro"]),
         color='navy', linestyle=':', linewidth=4)

lw = 2
colors = cycle(['aqua', 'darkorange', 'cornflowerblue'])
for i, color in zip(range(n_classes), colors):
    plt.plot(fpr[i], tpr[i], color=color, lw=lw,
             label='ROC curve of class {0} (area = {1:0.2f})'
             ''.format(i, roc_auc[i]))

plt.plot([0, 1], [0, 1], 'k--', lw=lw)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
# plt.xlabel('False Positive Rate')
# plt.ylabel('True Positive Rate')
# plt.title('Some extension of Receiver operating characteristic to multi-class')
# plt.legend(loc="lower right")

# plt.savefig("./roc.png")