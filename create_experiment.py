from dash import Dash, html
import dash_bootstrap_components as dbc

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

# Layout
app.layout = html.Div([
    # Header
    dbc.Navbar(
        dbc.Container([
            dbc.NavbarBrand("Untitled Diagram", className="ms-2"),
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("File")),
                dbc.NavItem(dbc.NavLink("Edit")),
                dbc.NavItem(dbc.NavLink("View")),
            ], navbar=True),
        ]),
        color="dark",
        dark=True,
    ),

    # WE WANT A SUBMIT BUTTON --> PUBLISHING TO EXTERNAL REPO / etc.

    # Main container
    html.Div([
        # Sidebar
        html.Div(
            id="sidebar",
            children=[
                html.Div("Shapes", className="sidebar-title"),
                html.Div(
                    id="shapes",
                    children=[
                        html.Div("Square", className="shape square", draggable="true", id="square"),
                        html.Div("Circle", className="shape circle", draggable="true", id="circle"),
                    ],
                ),
            ],
            className="sidebar",
        ),

        # Grid
        html.Div(
            id="grid",
            className="grid",
            children=[],
        ),
    ], className="main-container"),
], className="app-container")

# Custom CSS
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .app-container {
                display: flex;
                flex-direction: column;
                height: 100vh;
            }
            .main-container {
                display: flex;
                flex: 1;
                overflow: hidden;
            }
            .sidebar {
                width: 200px;
                background-color: #f8f9fa;
                border-right: 1px solid #ddd;
                padding: 10px;
                box-sizing: border-box;
            }
            .sidebar-title {
                font-weight: bold;
                margin-bottom: 10px;
            }
            .shape {
                border: 1px solid #000;
                padding: 10px;
                margin-bottom: 10px;
                text-align: center;
                cursor: grab;
            }
            .square {
                background-color: #ffcccc;
            }
            .circle {
                background-color: #ccffcc;
                border-radius: 50%;
            }
            .grid {
                flex: 1;
                position: relative;
                background-color: #f4f4f4;
                background-size: 20px 20px;
                background-image: linear-gradient(to right, #ddd 1px, transparent 1px), 
                                  linear-gradient(to bottom, #ddd 1px, transparent 1px);
                overflow: auto;
            }
            .draggable {
                position: absolute;
                cursor: move;
                z-index: 10;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
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
