from dash.dependencies import Input,Output
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
# import pandas as pd
# import plotly.graph_objs as go
# import plotly.express as px
from datetime import date, timedelta
# from components import *
from api import get_tickers


dash_app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash_app.server


ticker_dropdown = dbc.FormGroup(
    [
        dbc.Label("Ticker", html_for="ticker-dropdown", width=2),
        dbc.Col(
            dcc.Dropdown(
                id="ticker-dropdown",
                options=[{"label": i, "value": i} for i in get_tickers()],
                value='AAPL',
            ),
            width=10,
        ),
    ],
    row=True,
)


date_picker = dbc.FormGroup(
    [
        dbc.Label("Pricing Date", html_for="date-picker", width=2),
        dbc.Col(
            dcc.DatePickerSingle(
                id="date-picker",
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date.today() - timedelta(days=1),
                initial_visible_month=date(2017, 8, 5),
                date=date.today() - timedelta(days=1)
            ),
            width=10,
        ),
    ],
    row=True,
)

calculation_radio = dbc.FormGroup(
    [
        dbc.Label("Calculation Method", html_for="calculation-radio", width=2),
        dbc.Col(
            dbc.RadioItems(
                id="calculation-radios",
                options=[
                    {"label": "Explicit Method", "value": 1},
                    {"label": "Implicit Method", "value": 2},
                ],
                value=1,
                inline=True
            ),
            width=10,
        ),
    ],
    row=True,
)


closing_price_input = dbc.FormGroup(
    [
        dbc.Label("Closing Price", html_for="closing-price-input", width=2),
        dbc.Col(
            dbc.Input(
                type="number", id="closing-price-input", placeholder="Enter closing price"
            ),
            width=10,
        ),
    ],
    row=True,
)

volatility_input = dbc.FormGroup(
    [
        dbc.Label("Volatility", html_for="volatility-input", width=2),
        dbc.Col(
            dbc.Input(
                type="number", id="volatility-input"
            ),
            width=10,
        ),
    ],
    row=True,
)

interest_rate_input = dbc.FormGroup(
    [
        dbc.Label("Interest Rate", html_for="interest-input", width=2),
        dbc.Col(
            dbc.Input(
                type="number", id="interest-input"
            ),
            width=10,
        ),
    ],
    row=True,
)

maturity_input = dbc.FormGroup(
    [
        dbc.Label("Maturity", html_for="maturity-input", width=2),
        dbc.Col(
            dbc.Input(
                type="number", id="maturity-input"
            ),
            width=10,
        ),
    ],
    row=True,
)

strike_price_input = dbc.FormGroup(
    [
        dbc.Label("Strike Price", html_for="strike-price-input", width=2),
        dbc.Col(
            dbc.Input(
                type="number", id="strike-price-input"
            ),
            width=10,
        ),
    ],
    row=True,
)

dividend_yield_input = dbc.FormGroup(
    [
        dbc.Label("Dividend Yield", html_for="dividend-input", width=2),
        dbc.Col(
            dbc.Input(
                type="number", id="dividend-input"
            ),
            width=10,
        ),
    ],
    row=True,
)

space_step_input = dbc.FormGroup(
    [
        dbc.Label("M", html_for="space-step-input", width=2),
        dbc.Col(
            dbc.Input(
                type="number", id="space-step-input"
            ),
            width=10,
        ),
    ],
    row=True,
)

time_step_input = dbc.FormGroup(
    [
        dbc.Label("N", html_for="time-step-input", width=2),
        dbc.Col(
            dbc.Input(
                type="number", id="time-step-input"
            ),
            width=10,
        ),
    ],
    row=True,
)


submit_button = dbc.Button("Calculate", color="primary", block=True, n_clicks=0)

input_form = dbc.Form(
    [
        ticker_dropdown,
        date_picker,
        closing_price_input,
        volatility_input,
        interest_rate_input,
        maturity_input,
        strike_price_input,
        space_step_input,
        time_step_input,
        calculation_radio,
        submit_button
    ]

)

dash_app.layout = html.Div(input_form)

@dash_app.callback(
    Output(component_id='closing-price-input', component_property='value'),
    Input(component_id='ticker-dropdown', component_property='value'),
    Input(component_id='date-picker', component_property='date')
)

def update_price(ticker: str, date: date) -> None:
    print(ticker, date)
    pass


if __name__ == '__main__':
    dash_app.run_server(debug=True)