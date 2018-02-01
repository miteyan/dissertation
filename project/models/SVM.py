from sklearn import svm
from models.model import model
from models.model import k_fold_hyper_parameter

dataset = "/var/storage/miteyan/Dissertation/project/data/genderdata/weekly_dataset.csv"
dataset2 = "/var/storage/miteyan/Dissertation/project/data/emotion_sense_dataset.csv"

clf = svm.SVC()

print(clf.get_params().keys())

# specify parameters and distributions to sample from
param = {"kernel": ['linear', 'poly', 'rbf', 'sigmoid'],
          "degree": range(1, 8),
          "probability": [True, False],
          "decision_function_shape": ["ovo", "ovr"]
         }

k_fold_hyper_parameter(dataset2, clf, params=param)
