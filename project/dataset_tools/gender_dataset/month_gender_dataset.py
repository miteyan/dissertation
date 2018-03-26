import dataset_tools.dataset_utils as du

# FOLDER = '/var/storage/sandra/mdc_analysis/mdc_data/lausanne/nkYear/edgelists_year/*'
MONTH_EDGELISTS = '/var/storage/miteyan/Dissertation/project/graph_creation_lib/edgelists_month/*'
MONTH_WRITE_FOLDER = './month_datasets'
CLASSES = '/var/storage/miteyan/Dissertation/project/data/genderclasses'
FILE_NAMES = [MONTH_WRITE_FOLDER + "/train.csv", MONTH_WRITE_FOLDER + "/test.csv", MONTH_WRITE_FOLDER + "/valid.csv"]


du.create_dataset(MONTH_EDGELISTS, 0.7, 0.2, 0.1)