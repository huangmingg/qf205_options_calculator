from dash.dependencies import Input, Output, State
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from datetime import date, timedelta
from api import get_tickers, get_closing_price
from calculate import calculate_price
from typing import Tuple
# import plotly.graph_objs as go
# import plotly.express as px


dash_app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash_app.server

TICKERS, _ = get_tickers()

ticker_dropdown = dbc.FormGroup(
    [
        dbc.Label("Ticker", html_for="ticker-dropdown", width=2),
        dbc.Col(
            dcc.Dropdown(
                id="ticker-dropdown",
                options=[{"label": i, "value": i} for i in TICKERS],
                value=TICKERS[0] if len(TICKERS) else '',
            ),
            width=10,
        ),
    ],
    row=True,
)


calculation_radio = dbc.FormGroup(
    [
        dbc.Label("Calculation Method", html_for="calculation-radios", width=2),
        dbc.Col(
            dbc.RadioItems(
                id="calculation-radios",
                options=[
                    { "label": "Explicit Method", "value": 'explicit' },
                    { "label": "Implicit Method", "value": 'implicit' },
                    { "label": "Crank Method", "value": 'crank' },
                ],
                value='explicit',
                inline=True
            ),
            width=10,
        ),
    ],
    row=True,
)


pricing_row_input = dbc.FormGroup(
    [
        dbc.Label("Closing Price", html_for="closing-price-input", width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="closing-price-input", value=0, min=0
            ),
            width=4,
        ),
        dbc.Label("Strike Price", html_for="strike-price-input", width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="strike-price-input", value=0, min=0
            ),
            width=4,
        ),
    ],
    row=True,
)


vol_int_row_input = dbc.FormGroup(
    [
        dbc.Label("Volatility (%)", html_for="volatility-input", width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="volatility-input", value=5, min=0
            ),
            width=4,
        ),
        dbc.Label("Interest Rate (%)", html_for="interest-input", width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="interest-input", value=5, min=0
            ),
            width=4,
        ),
    ],
    row=True,
)


maturity_div_row_input = dbc.FormGroup(
    [
        dbc.Label("Maturity (Days)", html_for="maturity-input", width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="maturity-input", value=14, min=0
            ),
            width=4,
        ),
        dbc.Label("Dividend Yield (%)", html_for="dividend-input", width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="dividend-input", value=5, min=0
            ),
            width=4,
        ),        
    ],
    row=True,
)

space_time_step_row_input = dbc.FormGroup(
    [
        dbc.Label("M (Space Step)", html_for="space-step-input", width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="space-step-input", value=1, min=0
            ),
            width=4,
        ),
        dbc.Label("N (Time Step)", html_for="time-step-input", width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="time-step-input", value=1, min=0
            ),
            width=4,
        ),        
    ],
    row=True,
)


submit_button = dbc.Button("Calculate", color="primary", block=True, id="submit-button", n_clicks=0)
input_form = dbc.Form(
    [
        ticker_dropdown,
        pricing_row_input,
        vol_int_row_input,
        maturity_div_row_input,
        space_time_step_row_input,
        calculation_radio,
        submit_button
    ]
)


call_put_output = dbc.FormGroup(
    [
        dbc.Label("Call Price", html_for="call-price-output", width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="call-price-output", disabled=True, value=0
            ),
            width=4,
        ),
        dbc.Label("Put Price", html_for="put-price-output", width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="put-price-output", disabled=True, value=0
            ),
            width=4,
        ),        
    ],
    row=True,
)

output_form = dbc.Form(
    [
        call_put_output
    ]
)

dash_app.layout = html.Div(
    [
        html.H1("Options Pricing Calculator", className="display-5"),
        html.Hr(),
        input_form,
        html.Hr(), 
        output_form,
        html.Div(id='alert-div', children=[
            html.Div(id='update-price-alert', children=[]),
            html.Div(id='calculation-alert', children=[]),
        ])
    ],
    className='p-4',
    )


@dash_app.callback(
    Output(component_id='closing-price-input', component_property='value'),
    Output(component_id='strike-price-input', component_property='value'),
    Output(component_id='update-price-alert', component_property='children'),
    Input(component_id='ticker-dropdown', component_property='value'),
)
def update_price(ticker: str):
    p, err = get_closing_price(ticker)
    if err:
        error = dbc.Alert(
            err,
            is_open=True,
            duration=4000,
            color="danger"
        )
        return 0, 0, error

    else:
        return p, round((p*1.05),2), dash.no_update


@dash_app.callback(
    Output(component_id='call-price-output', component_property='value'),
    Output(component_id='put-price-output', component_property='value'),
    Output(component_id='calculation-alert', component_property='children'),
    Input('submit-button', 'n_clicks'),
    State('closing-price-input', 'value'),
    State('strike-price-input', 'value'),
    State('volatility-input', 'value'),
    State('interest-input', 'value'),
    State('maturity-input', 'value'),
    State('dividend-input', 'value'),
    State('space-step-input', 'value'),
    State('time-step-input', 'value'),
    State('calculation-radios', 'value'),
)
def calculate(
    n: int, 
    cp: float, 
    sp: float, 
    v: float, 
    int_rate: float, 
    mat: float, 
    div: float, 
    ss: float, 
    ts: float, 
    calculation_type: str
):
    if not n:
        return 0, 0, dash.no_update
    res, err = calculate_price(cp, sp, int_rate, div, mat, v, ss, ts, calculation_type)
    if err:
        error = dbc.Alert(
            err,
            is_open=True,
            duration=4000,
            color="danger"
        )
        return 0, 0, error
    else:
        call, put = res
        return call, put, dash.no_update
     


if __name__ == '__main__':
    dash_app.run_server(debug=True)