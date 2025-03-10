from dash import Dash, html
import dash_bootstrap_components as dbc
import os

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

app.layout = html.Div()

path_to_html = os.path.join("templates", "equipment_setup.html")
with open(path_to_html, "r", encoding="utf-8") as f:
    app.index_string = f.read()

if __name__ == "__main__":
    app.run_server(debug=True)
