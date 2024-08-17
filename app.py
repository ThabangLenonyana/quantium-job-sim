import pandas as pd
from dash import Dash, Input, Output, dcc, html

# Read CSV file data into a pandas DataFrame
df = (pd.read_csv('data/clean_data.csv')
      # Convert date values into Datetime Objects
      .assign(Date=lambda data: pd.to_datetime(data['Date'], format='%Y-%m-%d'))
      .sort_values(by='Date')
      )

regions = df['Region'].sort_values().unique()

css_style_sheet = [
    {
        'href': ('https://fonts.googleapis.com/css2?'
                 'family=Lato:wght@400;700&display=swap'),
        'rel': 'stylesheet'
    }
]

app = Dash(__name__, external_stylesheets=css_style_sheet)
app.title = 'Soul Food: Dashboard'

app.layout = html.Div(
    children=[
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

        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children='Region', className='menu-title'),
                        dcc.Dropdown(
                            id='region-filter',
                            options=[{'label': region, 'value': region}
                                     for region in regions],
                            value='North',
                            clearable=False,
                            className='dropdown'
                        )
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
                )
            ],
            className='menu',
        ),

        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id='price-chart',
                        config={'displayModeBar': False},
                    ),
                    className='card'
                ),
            ],
            className='wrapper'
        )
    ]
)


@app.callback(
    Output('price-chart', 'figure'),
    Input('region-filter', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_charts(region, start_date, end_date):
    filtered_data = df.query(
        "Region == @region and Date >= @start_date and Date <= @end_date"
    )

    price_chart_figure = {
        'data': [
            {'x': filtered_data['Date'],
             'y': filtered_data['Sales'],
             'type': 'line',
             'hovertemplate': ('$%{y:.2f}<extra></extra>')
             }],

        'layout': {'title': {'text': 'Sales Trend Over Time',
                             'x': 0.05,
                             'xanchor': 'left'},

                   'xaxis': {'fixedrange': True},
                   'yaxis': {'tickprefix': '$', 'fixedrange': True},
                   'colorway': ["#17b897"]
                   }

    }

    return price_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)
