# Soul Food Analytic Dashboard

This project is a data analytics dashboard for visualizing and analyzing sales data for Soul Food, built with Dash, Plotly, and Prophet. It offers insights into sales trends, product distribution, regional performance, and includes a time series prediction model.

## Project Structure
 - **app.py**: The main application file containing the Dash app layout, callbacks, and data processing logic.
 - **data/clean_data.csv**: The dataset used in the project.
 - **assets/**: Contains custom CSS for styling the dashboard.
 - **requirements.txt/**: Contains all the necessary dependancies to run the application 
 - **models/**: Directory containing the Prophet model and scripts related to time series prediction.
 - **README.md**: This documentation file.

## Features

- **Data Visualization Dashboard**: The dashboard allows users to visualize sales data with interactive charts.
  - **Sales Trend Graph**: Displays aggregated monthly sales with a 3-month moving average.
  - **Sales Distribution Pie Chart**: Always shows the distribution of sales across all products.
  - **Sales Heatmap**: Displays the density of sales across regions over time.
  
- **Time Series Prediction**: A Prophet model is implemented to predict future sales based on historical data.

## Prophet Model

The Prophet model is used for time series forecasting. It is located in the models/ directory. The model is trained on historical sales data and forecasts future sales trends. The forecasted data is displayed alongside historical data in the dashboard.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ThabangLenonyana/quantium-job-sim.git
    cd quantium-job-sim
    ```

2. Set up the virtual environment and install dependencies:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    python app.py
    ```

## Usage

- **Filtering Options**: The dashboard provides filtering options for regions and products. Users can select individual regions or products, or aggregate all regions/products.
- **Predictions**: The time series prediction graph provides insights into future sales trends.

## License

This project is licensed under the MIT License.
