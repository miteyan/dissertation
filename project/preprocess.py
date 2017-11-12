import time

from joblib import Parallel, delayed

from networkmodels import LausanneNetworks, fullLausanneNetworks

# code to preprocess the datasets and save them in hdf5 format
if __name__ == '__main__':
    # optionsList = [#{'datafolder':'data/Seattle', 'dataset':'Seattle', 'datetime':True, 'toLocalTime':False, 'frequency':'week'},
    # {'datafolder':'data/Geolife_Trajectories_1.3', 'dataset':'Beijing', 'datetime':True, 'toLocalTime':True, 'frequency':'week'},
    # {'datafolder':'data/android_app_data', 'dataset':'android_app', 'datetime':True, 'toLocalTime':False, 'frequency':'week'},\
    # {'datafolder':'data/ios_app_data', 'dataset':'ios_app', 'datetime':True, 'toLocalTime':False, 'frequency':'week'},
    # {'datafolder':'../mdc_data', 'dataset':'lausanne', 'datetime':True, 'toLocalTime':True, 'frequency':'week'},
    # {'datafolder':'../mdc_data', 'dataset':'full_lausanne', 'datetime':True, 'toLocalTime':True, 'frequency':'week'}
    # ]

    # optionsList = [#{'datafolder':'data/Seattle', 'dataset':'Seattle', 'datetime':True, 'toLocalTime':False, 'frequency':'day'},
    # {'datafolder':'data/Geolife_Trajectories_1.3', 'dataset':'Beijing', 'datetime':True, 'toLocalTime':True, 'frequency':'day'},
    # {'datafolder':'data/android_app_data', 'dataset':'android_app', 'datetime':True, 'toLocalTime':False, 'frequency':'day'},\
    # {'datafolder':'data/ios_app_data', 'dataset':'ios_app', 'datetime':True, 'toLocalTime':False, 'frequency':'day'},
    # {'datafolder':'../mdc_data', 'dataset':'lausanne', 'datetime':True, 'toLocalTime':True, 'frequency':'day'},
    # {'datafolder':'../mdc_data', 'dataset':'full_lausanne', 'datetime':True, 'toLocalTime':True, 'frequency':'day'}
    # ]

    optionsList = [
		# {'datafolder':'data/Seattle', 'dataset':'Seattle', 'datetime':True, 'toLocalTime':False, 'frequency':'year'},
        # {'datafolder':'data/Geolife_Trajectories_1.3', 'dataset':'Beijing', 'datetime':True, 'toLocalTime':True, 'frequency':'year'},
        # {'datafolder':'data/android_app_data', 'dataset':'android_app', 'datetime':True, 'toLocalTime':False, 'frequency':'year'},\
        # {'datafolder':'data/ios_app_data', 'dataset':'ios_app', 'datetime':True, 'toLocalTime':False, 'frequency':'year'},
        {'datafolder': '../mdc_data', 'dataset': 'lausanne', 'datetime': True, 'toLocalTime': True,
         'frequency': 'year'},
        # {'datafolder':'../mdc_data', 'dataset':'full_lausanne', 'datetime':True, 'toLocalTime':True, 'frequency':'year'}
    ]

    start = time.time()


    def preprocess_data(options):
        if options['dataset'] == 'Seattle':
            model = SeattleNetworks(options)
        elif options['dataset'] == 'Beijing':
            model = BeijingNetworks(options)
        elif options['dataset'] == 'ios_app':
            model = IosNetworks(options)
        elif options['dataset'] == 'android_app':
            model = AndroidNetworks(options)
        elif options['dataset'] == 'lausanne':
            model = LausanneNetworks(options)
        elif options['dataset'] == 'full_lausanne':
            model = fullLausanneNetworks(options)
        # else:
        #	model = LoctracNetworks(options)
        print('start preprocess')
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
