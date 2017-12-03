import csv


file = "/var/storage/Datasets/mdc/nokia_dataset/mdcdb/mdcdb_1003/demographics.csv"
print("uid\tgender\tage\t12\t18\t30\t40\t50\t65\t65+\tworking\tphone bill")
with open(file, 'rt', encoding="UTF8") as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    male = 0
    female = 0

    age1 = 0
    age2 = 0
    age3 = 0
    age4 = 0
    age5 = 0
    age6 = 0
    age7 = 0
    age8 = 0
    count = 0

    class1 = ""
    class2 = ""

    for row in reader:
        count += 1
        r = ', '.join(row)
        print(r)
        rs = r.split("\t")
        # print(rs)
        if rs[1] == '1':
            male += 1
            # print('Male: ', rs[0])
            class1 += rs[0]+ " "
        if rs[1] == '2':
            female += 1
            class2 += rs[0]+ " "

        if rs[2] == '1':
            age1 += 1
        if rs[2] == '2':
            age2 += 1
        if rs[2] == '3':
            age3 += 1
        if rs[2] == '4':
            age4 += 1
        if rs[2] == '5':
            age5 += 1
        if rs[2] == '6':
            age6 += 1
        if rs[2] == '7':
            age7 += 1
        if rs[2] == '8':
            age8 += 1
    #         not specified

    ages = age7+age6+age5+age4+age3+age2+age1
    genders = male+female
    print("uid\tmale f\t12\t18\t30\t40\t50\t65\t65+\tages")

    print(('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(count, male, female , age1, age2, age3, age4, age5, age6, age7, age8, ages)))

    print(class1)
    print(class2)