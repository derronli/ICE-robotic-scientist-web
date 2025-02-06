from dash import Dash, html
import dash_bootstrap_components as dbc

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

app.layout = html.Div()

app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}

        <script src="https://unpkg.com/konva@9.3.0/konva.min.js"></script>
    <style>
        body {
            margin: 0;
            padding: 0;
            display: flex;
        }

        #left-menu, #right-menu {
            background: #f0f0f0;
            height: 100vh; /* Full viewport height */
            width: 250px; /* Slightly wider right menu */
            position: sticky; /* Make the menus sticky */
            top: 0; /* Stick to the top of the viewport */
            transition: width 0.3s;
            z-index: 10; /* Ensure menus stay above other content */
        }

        #container {
            flex: 1;
            display: flex;
            justify-content: center; /* Center the matrix horizontally */
            align-items: center; /* Center the matrix vertically */
            flex-wrap: wrap; /* Allow wrapping for the matrix */
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

        .rectangle-info {
            padding: 10px;
            font-size: 16px;
        }
        
        </style>
        {%css%}
    </head>
    <body>
        {%app_entry%}

        <div id="left-menu">
            <button class="collapse-button" onclick="toggleLeftMenu()">←</button>
        </div>
        <div id="container"></div>
        <div id="right-menu">
            <button class="collapse-button" onclick="toggleRightMenu()">→</button>
            <div class="rectangle-info" id="rectangle-info">
                Click on a rectangle to see its color.
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
