import csv
import helper.write_file as writer

file = "/var/storage/Datasets/mdc/nokia_dataset/mdcdb/mdcdb_1003/demographics.csv"
write_file = './age_classes/age_classes'
print("uid\tgender\tage\t12\t18\t30\t40\t50\t65\t65+\tworking\tphone bill")
with open(file, 'rt', encoding="UTF8") as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    class1 = ""
    class2 = ""

    count = 0
    for row in reader:
        count += 1
        r = ', '.join(row)
        print(r)
        rs = r.split("\t")
        # print(rs)
        if rs[2] == '1' or rs[2] == '2' or rs[2] == '3':
            class1 += rs[0]+ " "
        if rs[2] == '4' or rs[2] == '5' or rs[2] == '6'or rs[2] == '7':
            class2 += rs[0]+ " "

    print(count)
    print(class1)
    print(class2)
    class1 += '\n'

    with open(file=write_file, mode='w') as f:
        f.write(class1)
        f.write(class2)
    f.close()