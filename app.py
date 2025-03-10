from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dashboard.dashboard import dashboard_layout
from equipment_setup import equipment_setup_page


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

app = Dash(external_stylesheets=[dbc.themes.COSMO, dbc.icons.FONT_AWESOME], suppress_callback_exceptions=True)
app.default_index_string = app.index_string

NAVBAR_STYLE = {
    "padding": "1rem",
}

navbar = html.Div([
    dbc.Navbar(
        dbc.Container([
            dbc.Nav([
                dbc.NavLink("Dashboard", href="/", active="exact"),
                dbc.NavLink("Equipment Setup", href="/equipment-setup", active="exact"),
                dbc.NavLink("Protocol Builder", href="/protocol-builder", active="exact"),
            ], navbar=True,pills=True, className="flex justify-content-center column-gap-5"),
        ], className="flex justify-content-center"),
        style=NAVBAR_STYLE
    ),
])

content = html.Div(id="page-content", children=[])


app.layout = [
    dcc.Location(id="url"),
    navbar,
    content
]

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        app.index_string = app.default_index_string
        return dashboard_layout
    elif pathname == "/equipment-setup":
        equipment_setup_page(app)
        return html.Div()
    elif pathname == "/page-2":
        return [
                html.H1('High School in Iran',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph',
                         figure=px.bar(df, barmode='group', x='Years',
                         y=['Girls High School', 'Boys High School']))
                ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == '__main__':
    app.run(debug=True)
