import pandas as pd

# Main DataFrame
# Read CSV file data into a pandas DataFrame
df = (pd.read_csv('data/clean_sales_data.csv')
      .assign(Date=lambda data: pd.to_datetime(data['Date'], format='%Y-%m-%d'))
      .sort_values(by='Date')
      )

# Define unique attributes for filtering
regions = df['Region'].sort_values().unique()
products = df['Product'].sort_values().unique()


def filter_data(df, region, product, start_date, end_date):
    if region == 'All' and product == 'All':
        return df[(df['Date'] >= start_date)
                  & (df['Date'] <= end_date)]
    elif region == 'All':
        return df[(df['Product'] == product)
                  & (df['Date'] >= start_date)
                  & (df['Date'] <= end_date)]
    elif product == 'All':
        return df[(df['Region'] == region)
                  & (df['Date'] >= start_date)
                  & (df['Date'] <= end_date)]
    else:
        return df[(df['Region'] == region)
                  & (df['Product'] == product)
                  & (df['Date'] >= start_date)
                  & (df['Date'] <= end_date)]


def filter_forecast_data(df, forecast_region, forecast_product):
    if forecast_region == 'All' and forecast_product == 'All':
        return df.copy()
    elif forecast_region == 'All':
        return df[(df['Product'] == forecast_product)]
    elif forecast_product == 'All':
        return df[df['Region'] == forecast_region]
    else:
        return df[(df['Region'] == forecast_region)
                  & (df['Product'] == forecast_product)]
