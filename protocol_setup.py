from dash import Dash, html
import dash_bootstrap_components as dbc
import os

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO], assets_ignore='equipment_setup.js')

# Layout
# app.layout = html.Div([
#     # Header
#     dbc.Navbar(
#         dbc.Container([
#             dbc.NavbarBrand("Untitled Diagram", className="ms-2"),
#             dbc.Nav([
#                 dbc.NavItem(dbc.NavLink("File")),
#                 dbc.NavItem(dbc.NavLink("Edit")),
#                 dbc.NavItem(dbc.NavLink("View")),
#             ], navbar=True),
#         ]),
#         color="dark",
#         dark=True,
#     ),

#     # WE WANT A SUBMIT BUTTON --> PUBLISHING TO EXTERNAL REPO / etc.

#     # Main container
#     html.Div([
#         # Sidebar
#         html.Div(
#             id="sidebar",
#             children=[
#                 html.Div("Shapes", className="sidebar-title"),
#                 html.Div(
#                     id="shapes",
#                     children=[
#                         html.Div("Square", className="shape square", draggable="true", id="square"),
#                         html.Div("Circle", className="shape circle", draggable="true", id="circle"),
#                     ],
#                 ),
#             ],
#             className="sidebar",
#         ),

#         # Grid
#         html.Div(
#             id="grid",
#             className="grid",
#             children=[],
#         ),
#     ], className="main-container"),
# ], className="app-container")

# navbar = html.Div([
#     # Header
#     dbc.Navbar(
#         dbc.Container([
#             dbc.NavbarBrand("Untitled Diagram", className="ms-2"),
#             dbc.Nav([
#                 dbc.NavItem(dbc.NavLink("File")),
#                 dbc.NavItem(dbc.NavLink("Edit")),
#                 dbc.NavItem(dbc.NavLink("View")),
#             ], navbar=True),
#         ]),
#         color="dark",
#         dark=True,
#     )
# ])

app.layout = html.Div()

path_to_html = os.path.join("templates", "protocol_setup.html")
with open(path_to_html, "r", encoding="utf-8") as f:
    app.index_string = f.read()


if __name__ == "__main__":
    app.run_server(debug=True)
