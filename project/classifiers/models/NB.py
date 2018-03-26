from sklearn.naive_bayes import GaussianNB

from classifiers.models.model import k_fold_hyper_parameter_averages

# dataset = ["/var/storage/miteyan/Dissertation/project/data/emotion_sense_dataset.csv", "/var/storage/miteyan/Dissertation/project/data/age_datasets/dataset.csv", "/var/storage/miteyan/Dissertation/project/data/genderdata/weekly_dataset.csv",]
dataset = ["/var/storage/miteyan/Dissertation/project/data/synthetic_graphs/d"]

clf = GaussianNB()
print(clf.get_params().keys())

# specify parameters and distributions to sample from
param = { }

for i in range(0, len(dataset)):
    k_fold_hyper_parameter_averages(dataset[i], clf, params=param)
