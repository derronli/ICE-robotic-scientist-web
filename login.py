from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(external_stylesheets=[dbc.themes.COSMO])

app.layout = [
    html.H1(children='ICE Lab Robotic Scientist', style={'textAlign':'center'}, className="mt-3"),
    html.Div(
        dbc.Row([
            dbc.Input(id="email", placeholder="Email", type="text", className="mb-2"),
            dbc.Input(id="password", placeholder="Password", type="password", className="mb-2"),
            dbc.Button("Login", id="login-button", color="primary"),
        ], style={"max-width": "18rem", "margin": "auto", "margin-top": "3rem"})
    )
]

@callback(
    Input('login-button', 'n_clicks'),
    State('email', 'value'),
    State('password', 'value')
)
def submit_login(n_clicks, email, password):
    print(n_clicks, email, password)
    return 0




if __name__ == '__main__':
    app.run(debug=True)
