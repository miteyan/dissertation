from sklearn.naive_bayes import GaussianNB
from scipy.stats import randint as sp_randint
from models.model import model

dataset = "/var/storage/miteyan/Dissertation/project/data/genderdata/weekly_dataset.csv"

clf = GaussianNB()

print(clf.get_params().keys())
# specify parameters and distributions to sample from


