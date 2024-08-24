from data_processing import prepare_data, load_data
import csv
from glob import glob
import pandas as pd

file_paths = glob('data/daily_sales_data_*.csv')

# Combine all the CSV files so they can be read all at once


# Create a writing stream for the CSV file
with open('data/clean_data.csv', mode='w', newline='') as clean_data:
    writer = csv.writer(clean_data, delimiter=',')

    # Write a header row into the new CSV file
    writer.writerow(['Product', 'Price', 'Quantity',
                    'Sales', 'Date', 'Region'])

    # Iterate through each file in file_paths
    for file in file_paths:
        # Create a reader object for each file
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            # Skip the first row(header) of each CSV file
            next(csv_reader)

            # Iterate over each row in the reader object and filter the data
            for row in csv_reader:
                product = row[0]
                price = float(row[1].strip('$'))
                quantity = float(row[2])
                sales = price * quantity
                date = row[3]
                region = row[4]

                # Write each row into the CSV file
                writer.writerow(
                    [product, price, quantity, sales, date, region])
