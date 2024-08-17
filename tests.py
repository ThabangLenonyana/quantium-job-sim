import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from dash.testing.application_runners import import_app


@pytest.fixture
def dash_duo(dash_duo):
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    service = Service(ChromeDriverManager().install())
    dash_duo.driver = webdriver.Chrome(service=service, options=options)
    return dash_duo


def test_header_is_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)

    header = dash_duo.find_element('.header-title')
    assert header is not None
    assert header.text == 'Soul Food Analytic Dashboard'


def test_visualisation(dash_duo, dash_app):
    dash_duo.start_sever(dash_app)

    visual = dash_duo.find_element('#price-chart')
    assert visual is not None


def test_menu(dash_duo, dash_app):
    dash_duo.start_sever(dash_app)

    menu = dash_duo.find_element('.menu')
    assert menu is not None
