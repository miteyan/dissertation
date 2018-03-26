from sklearn.ensemble import RandomForestClassifier

from classifiers.models.model import k_fold_hyper_parameter_averages

# dataset = "/var/storage/miteyan/Dissertation/project/data/genderdata/weekly_dataset.csv"
# dataset = "/var/storage/miteyan/Dissertation/project/data/emotion_sense_dataset.csv"
# dataset = "/var/storage/miteyan/Dissertation/project/data/age_datasets/dataset.csv"
# dataset = "/var/storage/miteyan/Dissertation/project/data/synthetic_graphs/dataset"
# dataset = "/var/storage/miteyan/Dissertation/project/data/emotion_sense__multiclass_dataset.csv"
# dataset = ["/var/storage/miteyan/Dissertation/project/data/emotion_sense_dataset.csv", "/var/storage/miteyan/Dissertation/project/data/age_datasets/dataset.csv", "/var/storage/miteyan/Dissertation/project/data/genderdata/weekly_dataset.csv",]
dataset = ["/var/storage/miteyan/Dissertation/project/data/synthetic_graphs/d"]
clf = RandomForestClassifier(n_estimators=4)
# specify parameters and distributions to sample from
param = {"n_estimators": [20,30],
              "max_depth": [6, 9, 12],
              "max_features": [5, 10, 15],
              "bootstrap": [True, False],
              "criterion": ["gini", "entropy"]}

for i in range(0, len(dataset)):
    k_fold_hyper_parameter_averages(dataset[i], clf, params=param)
# k_fold_hyper_parameter(dataset2, clf, params=param)
