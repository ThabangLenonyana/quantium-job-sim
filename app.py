import pandas as pd
from prophet import Prophet
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

# Read CSV file data into a pandas DataFrame
df = (pd.read_csv('data/clean_data.csv')
      # Convert date values into Datetime Objects
      .assign(Date=lambda data: pd.to_datetime(data['Date'], format='%Y-%m-%d'))
      .sort_values(by='Date')
      )

# Define unique attributes for filtering
regions = df['Region'].sort_values().unique()
products = df['Product'].sort_values().unique()

# Link CSS style sheet
css_style_sheet = [
    {
        'href': ('https://fonts.googleapis.com/css2?'
                 'family=Lato:wght@400;700&display=swap'),
        'rel': 'stylesheet'
    }
]

# Initialize an instance of the Dash Application
app = Dash(__name__, external_stylesheets=css_style_sheet)
app.title = 'Soul Food: Dashboard'

# Define the layout of the Dash App
app.layout = html.Div(
    children=[
        ######### HEADER #########
        html.Div(
            children=[
                html.P(children='🥑', className='header-emoji'),
                html.H1(children='Soul Food Analytic Dashboard',
                        className='header-title'),
                html.P(children=(
                    """Analyze if sales were higher before or after the Pink Morsel
                    price increase on the 15th of January, 2021"""),
                    className='header-description')
            ],
            className='header'
        ),
        ######### BODY ########
        html.Div(
            children=[
                # ---MENU---
                html.Div(
                    children=[
                        html.Div(children='Region', className='menu-title'),
                        dcc.Dropdown(
                            id='region-filter',
                            options=[{'label': 'All Regions', 'value': 'All'}] +
                            [{'label': region, 'value': region}
                             for region in regions],
                            value='All',
                            clearable=False,
                            className='dropdown'
                        )
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children='Product',
                                 className='menu-title'),
                        dcc.Dropdown(
                            id='product-filter',
                            options=[{'label': 'All Products', 'value': 'All'}] +
                            [{'label': product, 'value': product}
                                for product in products],
                            value='All',
                            clearable=False,
                            className='dropdown'
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children='Date Range',
                                 className='menu-title'),
                        dcc.DatePickerRange(
                            id='date-range',
                            min_date_allowed=df['Date'].min().date(),
                            max_date_allowed=df['Date'].max().date(),
                            start_date=df['Date'].min().date(),
                            end_date=df['Date'].max().date()
                        )
                    ]
                ),
            ],
            className='menu',
        ),

        html.Div(
            children=[
                # ---Line Graph---
                html.Div(
                    children=dcc.Graph(
                        id='price-chart',
                        config={'displayModeBar': False},
                        style={'height': '600px'}
                    ),
                    className='card'
                ),
                html.Div(children=[
                    # ---Pie Chart---
                    html.Div(
                        children=dcc.Graph(
                            id='donut-chart',
                            config={'displayModeBar': False}
                        ),
                        className='card column'
                    ),
                    # ---Heat Map---
                    html.Div(
                        children=dcc.Graph(
                            id='sales-heatmap',
                            config={'displayModeBar': False}
                        ),
                        className='card column'
                    )
                ], className='row'
                ),
                html.Div(
                    children=[
                        html.H2('Sales Forcasting',
                                className='header-title-inverse'),
                        html.P(
                            ' A time-series forecasting chart that uses historical sales data to predict future sales.',
                            className='header-description-inverse'),

                        html.Div(
                            children=[
                                html.Div(children='Region',
                                         className='menu-title'),
                                dcc.Dropdown(
                                    id='forecast-region-filter',
                                    options=[{'label': 'All Regions', 'value': 'All'}] + [{'label': region, 'value': region}
                                                                                          for region in regions],
                                    value='All',
                                    clearable=False,
                                    className='dropdown'
                                ),
                                html.Div(children='Product',
                                         className='menu-title'),
                                dcc.Dropdown(
                                    id='forecast-product-filter',
                                    options=[{'label': 'All Products', 'value': 'All'}] + [{'label': product, 'value': product}
                                                                                           for product in products],
                                    value='All',
                                    clearable=False,
                                    className='dropdown'
                                )
                            ],
                            className='menu'
                        ),
                        html.Div(
                            children=dcc.Graph(
                                id='forecast-chart',
                                config={'displayModeBar': False},
                                style={'height': '600px'}
                            ),
                            className='card'
                        )
                    ]
                )
            ],
            className='wrapper'

        )
    ],

)

# Callback Functions


@ app.callback(
    Output('price-chart', 'figure'),
    Output('donut-chart', 'figure'),
    Output('sales-heatmap', 'figure'),
    Output('forecast-chart', 'figure'),
    Input('region-filter', 'value'),
    Input('product-filter', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
    Input('forecast-region-filter', 'value'),
    Input('forecast-product-filter', 'value')


)
# Function to filter and update charts
def update_charts(region, product, start_date, end_date, forecast_region, forecast_product):

    if region == 'All' and product == 'All':
        filtered_data = df[(df['Date'] >= start_date)
                           & (df['Date'] <= end_date)]
    elif region == 'All':
        filtered_data = df[(df['Product'] == product) & (
            df['Date'] >= start_date) & (df['Date'] <= end_date)]
    elif product == 'All':
        filtered_data = df[(df['Region'] == region) & (
            df['Date'] >= start_date) & (df['Date'] <= end_date)]
    else:
        filtered_data = df[(df['Region'] == region) & (df['Product'] == product) & (
            df['Date'] >= start_date) & (df['Date'] <= end_date)]

    filtered_data = filtered_data.set_index('Date')

    resampled_data = filtered_data.resample('M').sum()
    resampled_data['Sales_MA'] = resampled_data['Sales'].rolling(
        window=3).mean()

    # Define the sales trend chart graph using filtered data
    price_chart_figure = {
        'data': [
            {'x': resampled_data.index,
             'y': resampled_data['Sales'],
             'name': 'Monthly Sales',
             'type': 'line',
             'hovertemplate': ('$%{y:.2f}<extra></extra>')
             },
            {'x': resampled_data.index,
             'y': resampled_data['Sales_MA'],
             'type': 'line',
             'name': '3-Month Moving Average',
             'hovertemplate': ('$%{y:.2f}<extra></extra>')
             }
        ],

        'layout': {'title': {'text': 'Sales Trend Over Time (Monthly Aggregated)',
                             'x': 0.05,
                             'xanchor': 'left'},

                   'xaxis': {'title': 'Date', 'fixedrange': True},
                   'yaxis': {'title': 'Sales (USD)', 'tickprefix': '$', 'fixedrange': True},
                   'colorway': ["#17b897", "#f76c6c"]
                   }

    }

    # filter Dataframe by grouping the data according to product
    product_sales = df.groupby(
        'Product', as_index=False).agg({'Sales': 'sum'})

    # Define a pie chart according to the filtered data
    donut_chart_figure = px.pie(
        product_sales,
        values='Sales',
        names='Product',
        hole=0.5,
        title='Sales Contribution by Product'
    )

    # Filter dataframe by grouging data acording to date and region
    heatmap_data = filtered_data.groupby(
        ['Date', 'Region']).sum().reset_index()

    # Define a heatmap graph
    heatmap_figure = px.density_heatmap(
        heatmap_data,
        x='Date',
        y='Region',
        z='Sales',
        color_continuous_scale='viridis',
        title='Sales Heatmap by Date and Region'
    )

    if forecast_region == 'All' and forecast_product == 'All':
        forecast_data = df.copy()
    elif forecast_region == 'All':
        forecast_data = df[(df['Product'] == forecast_product)]
    elif forecast_product == 'All':
        forecast_data = df[df['Region'] == forecast_region]
    else:
        forecast_data = df[(df['Region'] == forecast_region) &
                           (df['Product'] == forecast_product)]

    # Aggregate data by month
    monthly_data = forecast_data.resample('M', on='Date').sum().reset_index()
    monthly_data = monthly_data[['Date', 'Sales']]
    monthly_data.columns = ['ds', 'y']

    model = Prophet()
    model.fit(monthly_data)

    future = model.make_future_dataframe(periods=12, freq='M')
    forecast = model.predict(future)

    forecast_chart_figure = px.line(forecast, x='ds', y='yhat', labels={
                                    'ds': 'Date', 'yhat': 'Forecasted Sales (USD)'})
    actual_sales_line = px.line(monthly_data, x='ds', y='y')

    for trace in actual_sales_line.data:
        trace['line']['color'] = '#f76c6c'  # Set color for actual sales line
        forecast_chart_figure.add_trace(trace)

    '''forecast_chart_figure.add_traces(px.line(
        monthly_data, x='ds', y='y').data)  # Overlay actual sales data'''

    # Update layout for consistent style
    forecast_chart_figure.update_layout(
        title='Sales Forecasting',
        xaxis_title='Date',
        yaxis_title='Sales (USD)',
        colorway=["#17b897", "#f76c6c"],
        template='plotly_white')

    return price_chart_figure, donut_chart_figure, heatmap_figure, forecast_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)
