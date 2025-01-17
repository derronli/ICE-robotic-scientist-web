from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dashboard.dashboard import dashboard_layout


# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

# app = Dash(external_stylesheets=[dbc.themes.COSMO])

# app.layout = [
#     html.H1(children='Title of Dash App', style={'textAlign':'center'}),
#     dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
#     dcc.Graph(id='graph-content'),
#     dbc.DropdownMenu(label="Menu", children=[
#         dbc.DropdownMenuItem("Hello"),
#         dbc.DropdownMenuItem("World")
#     ])
# ]

# @callback(
#     Output('graph-content', 'figure'),
#     Input('dropdown-selection', 'value')
# )
# def update_graph(value):
#     dff = df[df.country==value]
#     return px.line(dff, x='year', y='pop')

app = Dash(external_stylesheets=[dbc.themes.COSMO, dbc.icons.FONT_AWESOME])

app.layout = [
    html.Div(
        dashboard_layout
    )
]

if __name__ == '__main__':
    app.run(debug=True)
