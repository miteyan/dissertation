import time
from graph_creation.networkmodels import LausanneNetworks, fullLausanneNetworks
from joblib import Parallel, delayed

# code to preprocess the datasets and save them in hdf5 format
if __name__ == '__main__':

    datafolder = "/var/storage/sandra/mdc_analysis/mdc_data/"
    optionsList = [
        {'datafolder': datafolder, 'dataset': 'full_lausanne', 'datetime': True, 'toLocalTime': True, 'frequency': 'month'},
    ]

    start = time.time()

    def preprocess_data(options):
        print('start preprocess')
        model = fullLausanneNetworks(options)
        dataset = model.preprocess(organize='keep_files_as_given')
        print('preprocess finished in : ', time.time() - start)
        if options['toLocalTime']:
            dataset = model.convert_to_local_time(dataset)
        print('start split over time')
        timesplit_data = model.split_over_time(dataset)

        print('start remove short trajectories')
        timesplit_data = model.remove_short_trajectories(timesplit_data)
        print('start remove check boundaries of the trajectory')
        timesplit_data = model.check_range_latlon(timesplit_data)
        # model.hist_dt(timesplit_data)
        # sys.exit()
        print('write preprocessed data')
        model.save_as_csv(timesplit_data)


    Parallel(n_jobs=-1, backend="threading")(
        map(delayed(preprocess_data), optionsList))

    end = time.time()
    print('finished in ', end - start)

    preprocess_data(optionsList[0])
