import csv
reader = csv.reader(open('kalyna_1.csv', 'r'))
i=0
for row in reader:
    print(row)
    i+=1
    if i == 10000:
        break