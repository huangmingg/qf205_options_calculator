import dash_bootstrap_components as dbc
import dash_core_components as dcc
from api import get_tickers
from datetime import date, timedelta

# ticker_dropdown = dbc.FormGroup(
#     [
#         dbc.Label("Ticker", html_for="dropdown", width=3),
#         dbc.Col(
#             dcc.Dropdown(
#                 id="dropdown",
#                 options=[{"label": i, "value": i} for i in get_tickers()],
#             ),
#             width=10,
#         ),
#     ],
#     row=True
# )


# date_picker = dbc.FormGroup(
#     [
#         dbc.Label("Select Date", html_for="date-picker"),
#         dcc.DatePickerSingle(
#             id="date-picker",
#             min_date_allowed=date(1995, 8, 5),
#             max_date_allowed=date.today() - timedelta(days=1),
#             initial_visible_month=date(2017, 8, 5),
#             date=date.today() - timedelta(days=1)
#     ),
#     ]
# )


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


submit_button = dbc.Button("Calculate", color="primary", block=True, n_clicks=0)



input_form = dbc.Form(
    [
        ticker_dropdown,
        date_picker,
        calculation_radio
    ]

)
