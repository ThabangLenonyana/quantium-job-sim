import plotly.express as px


def create_price_chart(resampled_data):
    return {'data': [
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


def create_donut_chart(df):
    product_sales = df.groupby(
        'Product', as_index=False).agg({'Sales': 'sum'})
    return px.pie(
        product_sales,
        values='Sales',
        names='Product',
        hole=0.5,
        title='Sales Contribution by Product'
    )


def create_heatmap(filtered_data):
    heatmap_data = filtered_data.groupby(
        ['Date', 'Region']).sum().reset_index()
    return px.density_heatmap(
        heatmap_data,
        x='Date',
        y='Region',
        z='Sales',
        color_continuous_scale='viridis',
        title='Sales Heatmap by Date and Region'
    )


def create_forecast_chart(forecast, monthly_data):
    forecast_chart_figure = px.line(forecast, x='ds', y='yhat', labels={
                                    'ds': 'Date', 'yhat': 'Forecasted Sales (USD)'})
    actual_sales_line = px.line(monthly_data, x='ds', y='y')

    for trace in actual_sales_line.data:
        trace['line']['color'] = '#f76c6c'
        forecast_chart_figure.add_trace(trace)

    # Update layout for consistent style
    forecast_chart_figure.update_layout(
        title='Sales Forecasting',
        xaxis_title='Date',
        yaxis_title='Sales (USD)',
        colorway=["#17b897", "#f76c6c"],
        template='plotly_white')

    return forecast_chart_figure
