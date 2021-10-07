from dash.dependencies import Input,Output
import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

dash_app = dash.Dash()
app = dash_app.server

tickers = ['AAPL', 'GOOG']

options = [{'label': i, 'value': i} for i in tickers]


dash_app.layout = html.Div([
    html.Label('Ticker'),
    dcc.Dropdown(
        id="ticker",
        options=options,
        value='AAPL',
        clearable=False,
    ),
    dcc.Graph(id="chart"),
])

@dash_app.callback(
    Output("chart", "figure"), 
    [Input("ticker", "value")])
def display_time_series(ticker):
    # data = db.get_rows_by_isin(ticker)
    # df = pd.DataFrame.from_dict(data)
    df = pd.DataFrame({ 
            "date": [],
            "indicative_value": []}) if df.empty else df
    graph = px.line(
        df, 
        x='date', 
        y='indicative_value', 
        title= "Time Series Data Indicative Value of Aggregated Holding")
    layout = go.Layout()
    return go.Figure(graph, layout)

if __name__ == '__main__':
    dash_app.run_server(debug=True)