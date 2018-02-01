from time import time

from numpy import zeros
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold

import helper.dataset_functions as ds

file = "/var/storage/miteyan/Dissertation/project/data/age_datasets/dataset.csv"
# file = "/var/storage/miteyan/Dissertation/project/data/genderdata/weekly_dataset.csv"



def k_fold_hyper_parameter(file, clf, params):
    dataset = ds.get_all_data(file, 0.00)
    print(len(dataset[0]))

    y, X = ds.get_labels_and_features(dataset)
    k = 5
    kfold_outer = KFold(n_splits=k)
    kfold_inner = KFold(n_splits=k)

    max_params = 0
    max_test = 0
    best_acc = []

    for train_index, test_index in kfold_outer.split(X):

        train_valid_dataset, test_dataset = X[train_index], X[test_index]
        train_valid_labels, test_labels = y[train_index], y[test_index]

        # Carry out train and test here

        clf.fit(train_valid_labels, train_valid_labels.ravel())

        # hyper parameter optimization
        optimized_model = GridSearchCV(clf, param_grid=params, cv=kfold_inner)

        print(optimized_model.cv_results_)
        best_params = optimized_model.best_params_
        print(best_params)
        # fit with hyper parameters


        test_predictions = optimized_model.predict(test_dataset)
        test_acc = ds.accuracy(test_predictions, test_labels)
        print("Test: ", test_acc)

        micro = f1_score(test_labels, test_predictions, average='micro')
        macro = f1_score(test_labels, test_predictions, average='macro')
        weighted = f1_score(test_labels, test_predictions, average='weighted')

        precision_recall_fscore = precision_recall_fscore_support(test_labels, test_predictions, average='weighted')

        print(precision_recall_fscore)

        if test_acc > max_test:
            max_test = test_acc
            max_params = best_params
            best_precision_recall = precision_recall_fscore
            best_acc = [micro, macro, weighted, test_acc, best_precision_recall]
        print(micro, macro, weighted)
        #
    print(max_params)
    print(best_acc)

def k_fold_hyper_parameter(file, clf, params):
    dataset = ds.get_all_data(file, 0.00)
    print(len(dataset))

    y, X = ds.get_labels_and_features(dataset)
    k = 5
    kfold_outer = KFold(n_splits=k)

    max_params = 0
    max_test = 0
    best_precision_recall = 0
    best_acc = []

    for train_index, test_index in kfold_outer.split(X):

        train_valid_dataset, test_dataset = X[train_index], X[test_index]
        train_valid_labels, test_labels = y[train_index], y[test_index]

        # Carry out train and test here
        kfold_inner = KFold(n_splits=k)
        for train_index, valid_index in kfold_inner.split(train_valid_dataset):

            train_dataset, valid_dataset = train_valid_dataset[train_index], train_valid_dataset[valid_index]
            train_labels, valid_labels = train_valid_labels[train_index], train_valid_labels[valid_index]
            c, r = valid_labels.shape
            valid_labels = valid_labels.reshape(c, )

            clf.fit(train_dataset, train_labels.ravel())

            # hyper parameter optimization
            optimized_model = GridSearchCV(clf, param_grid=params, cv=4)

            start = time()
            optimized_model.fit(valid_dataset, valid_labels.ravel())
            print("Hyper parameter optimisation took %.2f seconds" % (time() - start))
            print(optimized_model.cv_results_)
            best_params = optimized_model.best_params_
            print(best_params)
            # fit with hyper parameters
            train_predictions = optimized_model.predict(train_dataset)
            train_acc = ds.accuracy(train_predictions, train_labels)

            test_predictions = optimized_model.predict(test_dataset)
            test_acc = ds.accuracy(test_predictions, test_labels)

            val_predictions = optimized_model.predict(valid_dataset)
            val_acc = ds.accuracy(val_predictions, valid_labels)

            micro = f1_score(test_labels, test_predictions, average='micro')
            macro = f1_score(test_labels, test_predictions, average='macro')
            weighted = f1_score(test_labels, test_predictions, average='weighted')

            precision_recall_fscore = precision_recall_fscore_support(test_labels, test_predictions, average='weighted')

            print("Train: ", train_acc)
            print("Validation: ", val_acc)
            print("Test: ", test_acc)

            print(precision_recall_fscore)

            if test_acc > max_test:
                max_test = test_acc
                max_params = best_params
                best_precision_recall = precision_recall_fscore
                best_acc = [micro, macro, weighted, train_acc, val_acc, test_acc, best_precision_recall]
            print(micro, macro, weighted)
        #
    print(max_params)
    print(best_acc)


def model(dataset, clf, params):
    train_dataset, test_dataset, valid_dataset = ds.get_data(dataset, 0.1, 0.1,0.1)
    train_labels, train_dataset = ds.get_labels_and_features(train_dataset)
    test_labels, test_dataset = ds.get_labels_and_features(test_dataset)

    valid_labels, valid_dataset = ds.get_labels_and_features(valid_dataset)
    c, r = valid_labels.shape
    valid_labels = valid_labels.reshape(c, )

    clf.fit(train_dataset, train_labels.ravel())

    # run randomized search
    # hyper parameter optimization
    optimized_model = GridSearchCV(clf, param_grid=params, cv = 5)

    start = time()
    optimized_model.fit(valid_dataset, valid_labels.ravel())
    print("Hyper parameter optimisation took %.2f seconds" % (time() - start))
    print(optimized_model.cv_results_)
    best_params = optimized_model.best_params_
    print(best_params)

    # fit with hyper parameters
    train_predictions = optimized_model.predict(train_dataset)
    train_acc = ds.accuracy(train_predictions, train_labels)

    test_predictions = optimized_model.predict(test_dataset)
    test_acc = ds.accuracy(test_predictions, test_labels)

    val_predictions = optimized_model.predict(valid_dataset)
    val_acc = ds.accuracy(val_predictions, valid_labels)

    micro = f1_score(test_labels, test_predictions, average='micro')
    macro = f1_score(test_labels, test_predictions, average='macro')
    weighted = f1_score(test_labels, test_predictions, average='weighted')

    print("Train: ", train_acc)
    print("Validation: ", val_acc)
    print("Test: ", test_acc)

    print(micro, macro, weighted)
#

#