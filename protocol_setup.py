from dash import Dash, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import dash_extensions.javascript as js

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

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

app.layout = html.Div()


# Custom CSS
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        <script src="https://unpkg.com/konva@9.3.0/konva.min.js"></script>
        {%favicon%}
        {%css%}
        <style>
            body {
                margin: 0;
                padding: 0;
                display: flex;
            }

            #left-menu, #right-menu {
                background: #f0f0f0;
                height: 100vh; /* Full viewport height */
                width: 200px;
                position: sticky; /* Make the menus sticky */
                top: 0; /* Stick to the top of the viewport */
                transition: width 0.3s;
                z-index: 10; /* Ensure menus stay above other content */
            }

            #container {
                flex: 1;
            }

            .collapse-button {
                position: absolute;
                top: 10px;
                right: 10px;
                z-index: 1;
            }

            .collapsed {
                width: 50px;
            }

            .menu-buttons {
                display: flex;
                flex-direction: column; 
                align-items: center; 
                height: 100%; 
                padding-top: 3rem
            }

            #import-button, #export-button {
                width: 100px;
                padding: 10px;
                margin: 10px 0; 
                font-size: 14px;
                cursor: pointer;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f0f0f0;
                transition: background-color 0.3s;
            }

            #import-button:hover, #export-button:hover {
                background-color: #ddd; 
            }
        </style>
    </head>
    <body>
        {%app_entry%}

        <div id="left-menu">
        <button class="collapse-button" onclick="toggleLeftMenu()">←</button>
        </div>
        <div id="container"></div>
        <div id="right-menu">
            <button class="collapse-button" onclick="toggleRightMenu()">→</button>
            <div class="menu-buttons" id="menu-buttons">
                <button id="import-button">Import</button>
                <button id="export-button">Export</button>
            </div>
        </div>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""
if __name__ == "__main__":
    app.run_server(debug=True)
