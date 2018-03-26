from time import time

from scipy.stats import randint as sp_randint
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import RandomizedSearchCV

import dataset_tools.dataset_functions as ds

# dataset = "/var/storage/miteyan/Dissertation/project/data/age_datasets/dataset.csv"
file = "/var/storage/miteyan/Dissertation/project/data/genderdata/weekly_dataset.csv"


def model(dataset, clf, params, num_iters):
    train_dataset, test_dataset, valid_dataset = ds.get_data(dataset, 0.1, 0.1,0.1)

    train_labels, train_dataset = ds.get_labels_and_features(train_dataset)
    test_labels, test_dataset = ds.get_labels_and_features(test_dataset)

    valid_labels, valid_dataset = ds.get_labels_and_features(valid_dataset)
    c, r = valid_labels.shape
    valid_labels = valid_labels.reshape(c, )

    clf.fit(train_dataset, train_labels.ravel())

    # run randomized search
    # hyper parameter optimization
    optimized_model = RandomizedSearchCV(clf, param_distributions=params, n_iter=num_iters)

    start = time()
    optimized_model.fit(train_dataset, train_labels.ravel())
    print("RandomizedSearchCV took %.2f seconds for %d candidates"
          " parameter settings." % ((time() - start), 0))
    print(optimized_model.cv_results_)
    best_params = optimized_model.best_params_
    print(best_params)


    # fit with hyper parameters
    train_predictions = optimized_model.predict(train_dataset)
    train_acc = ds.accuracy(train_predictions, train_labels)

    test_predictions = optimized_model.predict(test_dataset)
    test_acc = ds.accuracy(test_predictions, test_labels)

    val_predictions = optimized_model.predict(valid_dataset)
    cv_acc = ds.accuracy(val_predictions, valid_labels)

    micro = f1_score(test_labels, test_predictions, average='micro')
    macro = f1_score(test_labels, test_predictions, average='macro')
    weighted = f1_score(test_labels, test_predictions, average='weighted')

    print("Train: ", train_acc)
    print("Test: ", test_acc)
    print("Validation: ", cv_acc)

    print(micro, macro, weighted)
#

clf = RandomForestClassifier(n_estimators=20)
num_iter = 20
# specify parameters and distributions to sample from
param = {"n_estimators": [20,30,40,50],
              "max_depth": [3, 6, 9, 12],
              "max_features": sp_randint(5,20),
              "bootstrap": [True, False],
              "criterion": ["gini", "entropy"]}


# model(file, clf, params=param, num_iters=100)