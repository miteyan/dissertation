from time import time

from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score, roc_curve
from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold

import dataset_tools.dataset_functions as ds


def k_fold_hyper_parameter(file, clf, params):
    dataset = ds.get_all_data(file, 0.00)

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
    y, X = ds.get_labels_and_features(dataset)
    k = 4
    kfold_outer = KFold(n_splits=k)

    max_test = 0
    accuracy = []
    numIters = 0

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
            # print("Hyper parameter optimisation took %.2f seconds" % (time() - start))
            # print(optimized_model.cv_results_)
            # best_params = optimized_model.best_params_
            # print(best_params)
            # fit with hyper parameters
            train_predictions = optimized_model.predict(train_dataset)
            train_acc = ds.accuracy(train_predictions, train_labels)

            val_predictions = optimized_model.predict(valid_dataset)
            val_acc = ds.accuracy(val_predictions, valid_labels)

            test_predictions = optimized_model.predict(test_dataset)
            test_acc = ds.accuracy(test_predictions, test_labels)
            # micro = f1_score(test_labels, test_predictions, average='micro')
            # macro = f1_score(test_labels, test_predictions, average='macro')
            # weighted = f1_score(test_labels, test_predictions, average='weighted')

            best_precision_recall = precision_recall_fscore_support(test_labels, test_predictions, average='weighted')

            # print("Train: ", train_acc)
            # print("Validation: ", val_acc)
            # print("Test: ", test_acc)
            # print(precision_recall_fscore)
            accuracy.append(test_acc)
            numIters += 1

            if test_acc > max_test:
                max_test = test_acc
                t = time() - start
                roc = roc_curve(valid_labels, val_predictions)
                # max_test = test_acc
                max_params = optimized_model.best_params_
                best = [train_acc, val_acc, test_acc, best_precision_recall[0], best_precision_recall[1],
                        best_precision_recall[2]]
                # best_acc = [micro, macro, weighted, train_acc, val_acc, test_acc, best_precision_recall]
                confusion = confusion_matrix(test_labels, test_predictions)
                # print(micro, macro, weighted)
    print('\n')
    print(t)
    print(best[0])
    print(best[1])
    print(best[2])
    print(best[3])
    print(best[4])
    print(best[5])
    print(confusion)
    print(roc)

    s = sum(accuracy)
    mean = s / numIters
    sum2 = sum(x ** 2 for x in accuracy)
    var = (sum2/ numIters) - (mean*mean)
    print(mean)
    print(var)
    print(max_params)
    print("\n")

def k_fold_hyper_parameter_averages(file, clf, params):
    dataset = ds.get_all_data(file, 0.00)
    y, X = ds.get_labels_and_features(dataset)
    k = 4
    kfold_outer = KFold(n_splits=k)
    max_test = 0
    accuracy = []
    train_accs = []
    val_accs = []
    test_accs = []
    precision = []
    recall = []
    f1 = []
    times = []
    numIters = 0
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
            # fit with hyper parameters
            train_predictions = optimized_model.predict(train_dataset)
            train_acc = ds.accuracy(train_predictions, train_labels)
            val_predictions = optimized_model.predict(valid_dataset)
            val_acc = ds.accuracy(val_predictions, valid_labels)
            test_predictions = optimized_model.predict(test_dataset)
            test_acc = ds.accuracy(test_predictions, test_labels)
            best_precision_recall = precision_recall_fscore_support(test_labels, test_predictions,
                                                                    average='weighted')
            accuracy.append(test_acc)
            numIters += 1
            train_accs.append(train_acc)
            test_accs.append(test_acc)
            val_accs.append(val_acc)

            t = time() - start
            times.append(t)

            # max_test = test_acc
            precision.append(best_precision_recall[0])
            recall.append(best_precision_recall[1])
            f1.append(best_precision_recall[2])
            # best_acc = [micro, macro, weighted, train_acc, val_acc, test_acc, best_precision_recall]
            if test_acc > max_test:
                max_test = test_acc
                confusion = confusion_matrix(test_labels, test_predictions)
                roc = roc_curve(valid_labels, val_predictions)
                max_params = optimized_model.best_params_
    print('\n')
    print(mean_var(train_accs))
    print(mean_var(val_accs))
    print(mean_var(test_accs))
    print(mean_var(precision))
    print(mean_var(recall))
    print(mean_var(f1))
    print(mean_var(times))
    print(confusion)
    print(roc)
    print(max_params)

def mean_var(list):
    s = sum(list)
    length = len(list)
    mean = s / length
    sum2 = sum(x ** 2 for x in list)
    var = (sum2 / length) - (mean * mean)
    return mean, var

def model(dataset, clf, params):
    train_dataset, test_dataset, valid_dataset = ds.get_data(dataset, 0.1, 0.1, 0.1)
    train_labels, train_dataset = ds.get_labels_and_features(train_dataset)
    test_labels, test_dataset = ds.get_labels_and_features(test_dataset)

    valid_labels, valid_dataset = ds.get_labels_and_features(valid_dataset)
    c, r = valid_labels.shape
    valid_labels = valid_labels.reshape(c, )

    clf.fit(train_dataset, train_labels.ravel())

    # run randomized search
    # hyper parameter optimization
    optimized_model = GridSearchCV(clf, param_grid=params, cv=5)

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
