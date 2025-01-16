from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc



new_devices = [
    "John's iPhone",
    "Bob's iPhone",
    "Sarah's Airpods"
]

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

bluetooth_card = dbc.Card(
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

@callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
