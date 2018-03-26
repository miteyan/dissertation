import dataset_tools.dataset_utils as du

# MONTH_EDGELISTS = '/var/storage/miteyan/Dissertation/project/graph_creation_lib/edgelists_month/*'
WEEK_EDGE_LISTS_DBSCAB = '/var/storage/miteyan/Dissertation/project/cluster/src/clustering/week_clusters/*'
WRITE_FOLDER = '/var/storage/miteyan/Dissertation/project/data/age_datasets/'
CLASSES = '/var/storage/miteyan/Dissertation/project/data/age_classes/age_classes'
FILE_NAME = WRITE_FOLDER + "/week_clustered_dataset.csv"

du.create_datasets(FILE_NAME, CLASSES, WEEK_EDGE_LISTS_DBSCAB)