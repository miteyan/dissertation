import numpy

import dataset_tools.dataset_functions as ds

file = "/var/storage/miteyan/Dissertation/project/data/synthetic_graphs/d"


array = ds.get_array(file)
numpy.random.shuffle(array)
print(array)
a = ds.abs_scale_array(array)


numpy.savetxt("/var/storage/miteyan/Dissertation/project/data/synthetic_graphs/foo.csv", a, delimiter=",", fmt="%.5e")
