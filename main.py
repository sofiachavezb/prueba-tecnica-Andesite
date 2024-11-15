import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Importar las secciones
from dashboard.daily_records_section import layout as daily_layout
from dashboard.monthly_records_section import layout as monthly_layout
from dashboard.monthly_records_section import register_callbacks as register_monthly_callbacks
from dashboard.daily_tons_section import layout as daily_tons_layout

# Crear la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Sidebar
sidebar = html.Div(
    [
        html.H2("Secciones", className="display-6"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Registros diarios", href="/daily-records", id="link-daily-records", active="exact"),
                dbc.NavLink("Registros mensuales", href="/monthly-records", id="link-monthly-records", active="exact"),
                dbc.NavLink("Toneladas diarias", href="/daily-tons", id="link-daily-tons", active="exact"),
            ],
            vertical=True,
            pills=True
        ),
    ],
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "20%",
        "padding": "2rem",
        "background-color": "#f8f9fa",
    },
)

# Layout principal
app.layout = html.Div(
    children=[
        dcc.Location(id='url', refresh=False),
        sidebar,  
        html.Div(
            id='page-content',
            style={'margin-left': '20%', 'padding': '2rem'}
        ),
    ]
)

# Callback para actualizar el contenido basado en la URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/daily-records':
        return daily_layout()
    elif pathname == '/monthly-records':
        return monthly_layout()
    elif pathname == '/daily-tons':
        return daily_tons_layout()
    else:
        return html.H1("Bienvenido al dashboard")

# Registrar los callbacks de las secciones
register_monthly_callbacks(app)
if __name__ == '__main__':
    app.run_server(debug=True)
