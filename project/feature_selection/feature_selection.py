from sklearn.feature_selection import VarianceThreshold
import numpy as np

# load into array

test = "/var/storage/miteyan/Dissertation/project/data/month_datasets/test.csv"
train = "/var/storage/miteyan/Dissertation/project/data/month_datasets/train.csv"
valid = "/var/storage/miteyan/Dissertation/project/data/month_datasets/valid.csv"

def get_array(file):
    arr = []
    with open(file, encoding='utf-16') as f:
        read_data = f.read()
        for line in read_data.splitlines():
            features = [np.float32(x) for x in line.split(",")]

            arr.append(features)
    f.close()
    return np.array(arr)

test_dataset = get_array(test)
train_dataset = get_array(train)
valid_dataset = get_array(valid)

test_dataset = np.concatenate((test_dataset, train_dataset, valid_dataset))
print(len(test_dataset))
print(len(test_dataset[0]))
sel = VarianceThreshold(threshold=(.9 * (1 - .9)))
a = sel.fit_transform(test_dataset)

print(len(a[0]))
