from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = Dash(external_stylesheets=[dbc.themes.COSMO, dbc.icons.FONT_AWESOME])

new_devices = [
    "John's iPhone",
    "Bob's iPhone",
    "Sarah's Airpods"
]

def container(children):
    return html.Div(
        children,
        style={"max-width": "70rem", "margin": "auto", "padding": "4rem 0"}
    )

modal = html.Div(
    [
        dbc.Modal(
            [
                # dbc.ModalHeader(dbc.ModalTitle("Header")),
                html.H5("Available Devices", className="mt-3 ms-3"),
                dbc.ModalBody([dbc.Button(device, outline=True, color="secondary", className="d-grid gap-2 col-6 mx-auto mb-2") for device in new_devices]),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="modal",
            is_open=False,
        ),
    ]
)

def load_experiments():
    return html.Div(
        children=[experiment for i in range(5)]
    )

experiment = dbc.Row([
    dbc.Col(html.P("November 11, 2024",className="fw-light"), width=4),
    dbc.Col([
        html.Span("Experiment 1", className="fs-5"),
        html.P("Cell Culture", className="fw-light"),
    ],
    className="gap-2",
    width=8
    )
])

card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Past experiments", className="card-title"),
                html.P(
                    "Click on each to view past data",
                    className="card-text",
                ),
                load_experiments(),
            ]
        ),
    ],
    style={"width": "40rem", "box-shadow": "0 0 10px rgba(157,143,143,0.45)", "max-height": "20rem", "overflow-y": "auto"},
    className="rounded card-scroller"
)

connection_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.I(className="fa-solid fa-circle me-2", style={"color": "#3cc23c"}),
                html.Span("No device connected", className="fs-5"),
                html.Div(
                    [
                        dbc.Row([
                            dbc.Button("Pair new device", id="open", n_clicks=0),
                            modal,
                        ], style={"max-width": "18rem", "margin": "auto", "margin-top": "2rem"}),

                        html.Div(
                            [
                                html.P("Previously connected devices", className="fw-light mb-0 mt-2"),
                                html.Div(
                                    [
                                        html.Div("Dennis's Apple Watch", className="device-entry"),
                                        html.Div("Dennis's AirPods #2", className="device-entry"),
                                    ],
                                    style={"background-color": "#f5f5f5"}
                                ),
                            ]
                        )
                    ]
                ),
            ]
        ),
    ],
    style={"width": "20rem", "box-shadow": "0 0 10px rgba(157,143,143,0.45)", "max-height": "20rem"},
    className="rounded"
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

app.layout = [
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
                    connection_card,
                ],
                className="gap-5 justify-content-center pb-5"
                ),
                dbc.Row(
                    ongoing_experiment_card
                )
            ]
        )
    )
]



@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run(debug=True)
