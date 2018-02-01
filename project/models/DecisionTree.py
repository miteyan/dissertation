from models.model import model
from models.model import k_fold_hyper_parameter
from sklearn.tree import DecisionTreeClassifier

dataset = "/var/storage/miteyan/Dissertation/project/data/genderdata/weekly_dataset.csv"
dataset2 = "/var/storage/miteyan/Dissertation/project/data/emotion_sense_dataset.csv"

clf = DecisionTreeClassifier()
print(clf.get_params().keys())
#
# # specify parameters and distributions to sample from

param = {"max_depth": [3, 6, 9, 12],
              "max_features": [5, 10, 15, 19],
              "min_samples_leaf": [3, 6, 9, 12, 15],
              "criterion": ["gini", "entropy"]}
k_fold_hyper_parameter(dataset2, clf, params=param)