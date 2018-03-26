import csv

file = "/var/storage/sandra/location2017/emotionsense/data/surveys/staticSurveys_textLabel.txt"
with open(file, 'rt', encoding="UTF8") as csvfile:
    reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    working = 0

    fullworking = ""
    fw = 0
    stillatschool = ""
    ss = 0
    unemployed = ""
    u = 0
    retired = ""
    atuniversity = ""
    parent = ""
    unemployed = ""
    parttime = ""
    selfemployed = ""
    r = 0
    au = 0
    p = 0
    u = 0
    pt = 0
    s = 0

    for row in reader:
        if row[4] == '"In full time employment"':
            fullworking += str(row[1][1:-1]) + " "
            fw += 1
        elif row[4] == '"Still at school"':
            stillatschool += row[1][1:-1]+ " "
            ss += 1
        elif row[4] == '"Homemaker/full-time parent"':
            parent += row[1][1:-1]+ " "
            p += 1
        elif row[4] == '"Self employed"':
            selfemployed += row[1][1:-1]+ " "
            s+=1
        elif row[4] == '"Unemployed"':
            unemployed += row[1][1:-1]+ " "
            u+= 1
        elif row[4] == '"At university"':
            atuniversity += row[1][1:-1]+ " "
            au+=1
        elif row[4] == '"Part time employment"':
            parttime += row[1][1:-1]+ " "
            pt+=1
        elif row[4] == '"Retired"':
            retired += row[1][1:-1]+ " "
            r+=1
        else:
            print(row[4])

    print(working)
    print(stillatschool)
    print(unemployed)
    print(parent)
    print(selfemployed)
    print(unemployed)
    print(retired)
    print(atuniversity)
    print(parttime)
    print([fw, ss, p, s, u, au, pt, r])
