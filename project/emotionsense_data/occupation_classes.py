import csv


file = "/var/storage/sandra/location2017/emotionsense/data/surveys/staticSurveys_textLabel.txt"
print("uid\tgender\tage\t12\t18\t30\t40\t50\t65\t65+\tworking\tphone bill")
with open(file, 'rt', encoding="UTF8") as csvfile:
    reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    working = 0
    notworking = 0

    working = ""
    notworking = ""

    for row in reader:
        print(row[1], row[4])
        if row[4] == '"In full time employment"':
            working += row[1][1:-1]+ " "
        elif row[4] != "NA":
            notworking += row[1][1:-1]+ " "
    print(working)
    print(notworking)