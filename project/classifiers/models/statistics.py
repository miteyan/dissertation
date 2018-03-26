from dataset_tools.dataset_functions import get_array

dataset = ["/var/storage/miteyan/Dissertation/project/data/age_datasets/dataset.csv", "/var/storage/miteyan/Dissertation/project/data/genderdata/weekly_dataset.csv","/var/storage/miteyan/Dissertation/project/data/emotion_sense_dataset.csv", ]

all_vectors = get_array(dataset[2])
for j in range(len(all_vectors)):
    print(all_vectors[j][1])
