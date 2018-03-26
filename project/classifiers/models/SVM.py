from sklearn import svm

from classifiers.models.model import k_fold_hyper_parameter_averages

# dataset2 = "/var/storage/miteyan/Dissertation/project/data/genderdata/weekly_dataset.csv"
# dataset2 = "/var/storage/miteyan/Dissertation/project/data/emotion_sense_dataset.csv"
# dataset2 = "/var/storage/miteyan/Dissertation/project/data/age_datasets/dataset.csv"
# dataset = "/var/storage/miteyan/Dissertation/project/data/synthetic_graphs/dataset"
# dataset = "/var/storage/miteyan/Dissertation/project/data/emotion_sense__multiclass_dataset.csv"
# dataset = ["/var/storage/miteyan/Dissertation/project/data/emotion_sense_dataset.csv", "/var/storage/miteyan/Dissertation/project/data/age_datasets/dataset.csv", "/var/storage/miteyan/Dissertation/project/data/genderdata/weekly_dataset.csv",]
dataset = ["/var/storage/miteyan/Dissertation/project/data/synthetic_graphs/d"]

clf = svm.SVC()

print(clf.get_params().keys())

# specify parameters and distributions to sample from
param = {"kernel": ['linear', 'poly', 'rbf', 'sigmoid'],
          "degree": range(3, 8),
          "probability": [True, False],
          "decision_function_shape": ["ovo", "ovr"]
         }

for i in range(0, len(dataset)):
    k_fold_hyper_parameter_averages(dataset[i], clf, params=param)
