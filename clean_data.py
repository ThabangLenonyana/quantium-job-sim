import csv
from glob import glob

file_paths = glob('data/daily_sales_data_*.csv')

with open('data/clean_data.csv', mode='w', newline='') as clean_data:
    writer = csv.writer(clean_data, delimiter=',')

    writer.writerow(['Sales', 'Date', 'Region'])

    for file in file_paths:
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            next(csv_reader)

            for row in csv_reader:
                if row[0] == 'pink morsel':
                    price = float(row[1].strip('$'))
                    quantity = float(row[2])

                    sales = price * quantity
                    date = row[3]
                    region = row[4]

                    writer.writerow([sales, date, region])
