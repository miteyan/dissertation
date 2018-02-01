from sklearn.feature_selection import VarianceThreshold
import numpy as np

# load into array

# test = "/var/storage/miteyan/Dissertation/project/data/month_datasets/test.csv"
# train = "/var/storage/miteyan/Dissertation/project/data/month_datasets/train.csv"
# valid = "/var/storage/miteyan/Dissertation/project/data/month_datasets/valid.csv"
dataset = "/var/storage/miteyan/Dissertation/project/data/genderdata/weekly_dataset2.csv"
def get_array(file):
    arr = []
    with open(file, encoding='utf-16') as f:
        read_data = f.read()
        for line in read_data.splitlines():
            features = [np.float32(x) for x in line.split(",")]

            arr.append(features)
    f.close()
    return np.array(arr)

dataset = get_array(dataset)
print(len(dataset[0]))
sel = VarianceThreshold(threshold=(1))
a = sel.fit_transform(dataset)
print(a[0])
print(len(a[0]))
