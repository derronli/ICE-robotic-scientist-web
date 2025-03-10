from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import os

# Initialize the app
def equipment_setup_page(app):
    # Load the HTML content from the file
    path_to_html = os.path.join("templates", "equipment_setup.html")
    with open(path_to_html, "r", encoding="utf-8") as f:
        app.index_string = f.read()

    # Return an empty layout (or any placeholder content)
    return html.Div()

