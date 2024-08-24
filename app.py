from prophet import Prophet
from dash import Dash, Input, Output, dcc, html
from dataframes import df, regions, products
from dataframes import filter_data, filter_forecast_data
from plotter import create_donut_chart, create_forecast_chart, create_heatmap, create_price_chart


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
                        html.H2('Sales Forecasting',
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

    filtered_data = filter_data(df, region, product, start_date, end_date)
    filtered_data = filtered_data.set_index('Date')
    resampled_data = filtered_data.resample('M').sum()
    resampled_data['Sales_MA'] = resampled_data['Sales'].rolling(
        window=3).mean()

    price_chart_figure = create_price_chart(resampled_data)
    donut_chart_figure = create_donut_chart(df)
    heatmap_figure = create_heatmap(filtered_data)

    forecast_data = filter_forecast_data(df, forecast_region, forecast_product)
    monthly_data = forecast_data.resample('M', on='Date').sum().reset_index()
    monthly_data = monthly_data[['Date', 'Sales']]
    monthly_data.columns = ['ds', 'y']

    # define an instance of the Prophet class
    model = Prophet()
    model.fit(monthly_data)
    future = model.make_future_dataframe(periods=12, freq='M')
    forecast = model.predict(future)

    forecast_chart_figure = create_forecast_chart(forecast, monthly_data)

    return price_chart_figure, donut_chart_figure, heatmap_figure, forecast_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)
