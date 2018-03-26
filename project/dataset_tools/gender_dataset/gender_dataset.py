import dataset_tools.dataset_utils as du
# FOLDER = '/var/storage/sandra/mdc_analysis/mdc_data/lausanne/nkYear/edgelists_year/*'
FOLDER = '/var/storage/miteyan/Dissertation/project/cluster/src/clustering/week_clusters'
CLASSES = '/var/storage/miteyan/Dissertation/project/data/genderclasses'

du.create_dataset(FOLDER, 0.7, 0.2, 0.1)