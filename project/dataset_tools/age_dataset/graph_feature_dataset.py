import dataset_tools.dataset_utils as du

# YEAR_EDGE_LISTS = '/var/storage/sandra/mdc_analysis/mdc_data/lausanne/nkYear/edgelists_year/*'
WEEK_EDGE_LISTS_DBSCAB = '/var/storage/miteyan/Dissertation/project/cluster/src/clustering/week_clusters/*'
WRITE_FOLDER = '/var/storage/miteyan/Dissertation/project/data/genderdata/'
# WRITE_FOLDER = '/var/storage/miteyan/Dissertation/project/data/age_datasets/'
# CLASSES = '/var/storage/miteyan/Dissertation/project/data/gender_classes/genderclasses'
CLASSES = '/var/storage/miteyan/Dissertation/project/data/age_classes/age_classes'
WRITE_FILE = WRITE_FOLDER + "/weekly_dataset2.csv"

du.create_datasets(WRITE_FILE, CLASSES, WEEK_EDGE_LISTS_DBSCAB)