from scipy.stats import randint as sp_randint
from sklearn.ensemble import RandomForestClassifier

from models.model import model
from models.model import k_fold_hyper_parameter

dataset = "/var/storage/miteyan/Dissertation/project/data/genderdata/weekly_dataset.csv"
# dataset2 = "/var/storage/miteyan/Dissertation/project/data/emotion_sense_dataset.csv"

clf = RandomForestClassifier(n_estimators=20)
num_iter = 20
# specify parameters and distributions to sample from
param = {"n_estimators": [20,30,40,50],
              "max_depth": [3, 6, 9, 12],
              "max_features": [5, 10, 12],
              "bootstrap": [True, False],
              "criterion": ["gini", "entropy"]}


k_fold_hyper_parameter(dataset, clf, params=param)
# k_fold_hyper_parameter(dataset2, clf, params=param)