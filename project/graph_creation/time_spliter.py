from datetime import datetime
import os.path
import pandas as pd

# STEP 1, takes the raw dataset data to per user data for each month.

dataset = '/var/storage/sandra/mdc_analysis/mdc_data/nokia_data_full.csv'
# data = '/var/storage/miteyan/Dissertation/project/data/testlocations/loc'
folder = "./full_data/"
for chunk in pd.read_csv(dataset, chunksize=1000):
    data = chunk.values.tolist()

    for i in range(0, len(data)):
        line = data[i]
        user = line[0]
        time = datetime.fromtimestamp(float(line[1])).isocalendar()
        month = time[2]
        print(time)
        print(month)
        year = time[0]
        file_name = folder + str(user)[:-2] + '_' + str(year) + '_' + str(month) + '.csv'

        time = datetime.fromtimestamp(float(line[1]))
        final_line = str(time) + ',' + str(line[3]) + ',' + str(line[2]) + '\n'
        # if not os.path.exists(file_name):
        #     f = open(file_name, "w+")
        #     f.write('datetime,lat,lon\n')
        #     print(file_name)
        #     f.close()
        #
        # with open(file_name, "a+") as myfile:
        #     myfile.write(final_line)
