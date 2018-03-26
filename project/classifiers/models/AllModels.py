from sklearn.tree import DecisionTreeClassifier

from classifiers.models.model import k_fold_hyper_parameter

# dataset = "/var/storage/miteyan/Dissertation/project/data/genderdata/weekly_dataset.csv"
# dataset = "/var/storage/miteyan/Dissertation/project/data/emotion_sense_dataset.csv"
# dataset = "/var/storage/miteyan/Dissertation/project/data/synthetic_graphs/dataset"
# dataset = "/var/storage/miteyan/Dissertation/project/data/age_datasets/dataset.csv"
dataset = "/var/storage/miteyan/Dissertation/project/data/emotion_sense__multiclass_dataset.csv"

clf = DecisionTreeClassifier()
print(clf.get_params().keys())

# specify parameters and distributions to sample from
param = {"max_depth": [3, 6, 9, 12],
              "max_features": [5, 10,],
              "min_samples_leaf": [3, 6, 9, 12, 15],
              "criterion": ["gini", "entropy"]}

k_fold_hyper_parameter(dataset, clf, params=param)

from sklearn.ensemble import RandomForestClassifier

from classifiers.models.model import k_fold_hyper_parameter

clf = RandomForestClassifier(n_estimators=4)
num_iter = 4
# specify parameters and distributions to sample from
param = {"n_estimators": [20,30,40,50],
              "max_depth": [3, 6, 9, 12],
              "max_features": [5, 10, 12],
              "bootstrap": [True, False],
              "criterion": ["gini", "entropy"]}

k_fold_hyper_parameter(dataset, clf, params=param)
# k_fold_hyper_parameter(dataset2, clf, params=param)

from sklearn import svm
from classifiers.models.model import k_fold_hyper_parameter

clf = svm.SVC()

print(clf.get_params().keys())

# specify parameters and distributions to sample from
param = {"kernel": ['linear', 'poly', 'rbf', 'sigmoid'],
          "degree": range(1, 8),
          "probability": [True, False],
          "decision_function_shape": ["ovo", "ovr"]
         }

k_fold_hyper_parameter(dataset, clf, params=param)