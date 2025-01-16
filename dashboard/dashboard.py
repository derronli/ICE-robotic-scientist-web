from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from .experiment_card import card
from .bluetooth_card import bluetooth_card

app = Dash(external_stylesheets=[dbc.themes.COSMO, dbc.icons.FONT_AWESOME])

def container(children):
    return html.Div(
        children,
        style={"max-width": "62rem", "margin": "auto", "padding": "4rem 0"}
    )

# ===============================================================================================================

df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

fig = px.scatter(df, x="gdp per capita", y="life expectancy",
                 size="population", color="continent", hover_name="country",
                 log_x=True, size_max=30)

ongoing_experiment_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Ongoing experiment"),

                dcc.Graph(
                    id='life-exp-vs-gdp',
                    figure=fig
                ),

                dbc.Progress(label="76%", value=76, color="primary", className="rounded")
            ]
        ),
    ],
    style={"width": "80rem", "box-shadow": "0 0 10px rgba(157,143,143,0.45)"},
    className="rounded"
)

dashboard_layout = [
    # html.H1(children='Select a device to connect with', style={'textAlign':'center'}, className="mt-3"),

    # html.Div(
    #     dbc.Row([
    #         dbc.Button("Pair new device", id="open", n_clicks=0),
    #         modal,
    #     ], style={"max-width": "18rem", "margin": "auto", "margin-top": "3rem"})
    # )
    container(
        html.Div(
            [
                dbc.Row(children=[
                    card,
                    bluetooth_card,
                ],
                className="gap-5 justify-content-between pb-5"
                ),
                dbc.Row(
                    ongoing_experiment_card
                )
            ]
        )
    )
]

if __name__ == '__main__':
    app.run(debug=True)
