from sklearn.tree import DecisionTreeClassifier

from classifiers.models.model import k_fold_hyper_parameter_averages

dataset = ["/var/storage/miteyan/Dissertation/project/data/emotion_sense_dataset.csv", "/var/storage/miteyan/Dissertation/project/data/age_datasets/dataset.csv", "/var/storage/miteyan/Dissertation/project/data/genderdata/weekly_dataset.csv",]
# dataset = ["/var/storage/miteyan/Dissertation/project/data/emotion_sense__multiclass_dataset.csv"]
# dataset = ["/var/storage/miteyan/Dissertation/project/data/synthetic_graphs/d"]
# dataset = "/var/storage/miteyan/Dissertation/project/data/emotion_sense_dataset.csv"
clf = DecisionTreeClassifier()
print(clf.get_params().keys())

# specify parameters and distributions to sample from

param = {"max_depth": [3, 6, 9, 12],
              "max_features": [5, 10, 15, 19],
              "min_samples_leaf": [3, 6, 9, 12, 15],
              "criterion": ["gini", "entropy"]}
for i in range(0, len(dataset)):
    k_fold_hyper_parameter_averages(dataset[i], clf, params=param)