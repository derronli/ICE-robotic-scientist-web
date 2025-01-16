from dash import html
import dash_bootstrap_components as dbc

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