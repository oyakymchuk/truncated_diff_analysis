import csv
for j in range(3,9):
    reader = csv.reader(open(f'kalyna_{j}.csv', 'r'))
    i=0
# print(len(reader))
    for row in reader:
        i+=1
    print(i)