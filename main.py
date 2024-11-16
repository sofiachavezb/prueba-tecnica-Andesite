import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO

# Importar las secciones
from dashboard.daily_cycles_section import daily_cycles_layout as daily_layout
from dashboard.monthly_cycles_section import layout as monthly_layout
from dashboard.monthly_cycles_section import register_callbacks as register_monthly_callbacks
from dashboard.daily_cycles_vs_tons import layout as daily_vs_tons_layout
from dashboard.trucks_daily_cycles_section import layout as trucks_daily_cycles_layout
from dashboard.trucks_daily_tons_section  import layout as trucks_daily_tons_layout
from dashboard.loaders_tons_section import layout as loaders_layout
from dashboard.trucks_loaders_tons_section import layout as truck_loader_tons_layout
from dashboard.shovels_per_load_section import layout as shovels_per_load_layout
from dashboard.truck_cycle_section import layout as truck_cycle_analysis_layout
from dashboard.loader_cycle_section import layout as loader_cycle_analysis_layout
from dashboard.empty_distance_section import layout as empty_distance_analysis_layout
from dashboard.loaded_distance_section import layout as loaded_distance_analysis_layout

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])
theme_switch = ThemeSwitchAIO(
    aio_id="theme", themes=[dbc.themes.COSMO, dbc.themes.CYBORG]
)
sidebar = html.Div(
    children=[
        html.H2("Secciones", className="display-6"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Inicio", href="/", id="link-home", active="exact"),
                dbc.NavLink("Ciclos diarios", href="/daily-cycles", id="link-daily-cycles", active="exact"),
                dbc.NavLink("Ciclos mensuales", href="/monthly-cycles", id="link-monthly-cycles", active="exact"),
                dbc.NavLink("Ciclos vs toneladas", href="/cycles-vs-tons", id="link-cycles-vs-tons", active="exact"),
                dbc.NavLink("Ciclos diarios de camiones", href="/trucks-daily-cycles", id="link-daily-truck-activity", active="exact"),
                dbc.NavLink("Toneladas diarias de camiones", href="/trucks-daily-tons", id="link-daily-truck-tons", active="exact"),
                dbc.NavLink("Toneladas por cargador", href="/loaders-tons", id="link-loaders", active="exact"),
                dbc.NavLink("Toneladas por camión y cargador", href="/truck-loader-tons", id="link-truck-loader-tons", active="exact"),
                dbc.NavLink("Análisis palas por carga", href="/shovels-per-load", id="link-shovels-per-load", active="exact"),
                dbc.NavLink("Análisis de ciclo de camión", href="/truck-cycle-analysis", id="link-truck-cycle-analysis", active="exact"),
                dbc.NavLink("Análisis de ciclo de cargador", href="/loader-cycle-analysis", id="link-loader-cycle-analysis", active="exact"),
                dbc.NavLink("Análisis de distancia sin carga", href="/empty-distance-analysis", id="link-empty-distance-analysis", active="exact"),
                dbc.NavLink("Análisis de distancia con carga", href="/loaded-distance-analysis", id="link-loaded-distance-analysis", active="exact"), 
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

app.layout = html.Div(
    children=[
        theme_switch,
        dcc.Location(id='url', refresh=False),
        sidebar,
        html.Div(
            id='page-content',
            style={'margin-left': '20%', 'padding': '2rem'}
        ),
    ]
)


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/daily-cycles':
        return daily_layout()
    elif pathname == '/monthly-cycles':
        return monthly_layout()
    elif pathname == '/cycles-vs-tons':
        return daily_vs_tons_layout()
    elif pathname == '/trucks-daily-cycles':
        return trucks_daily_cycles_layout()
    elif pathname == '/trucks-daily-tons':
        return trucks_daily_tons_layout()
    elif pathname == '/loaders-tons':
        return loaders_layout()
    elif pathname == '/truck-loader-tons':
        return truck_loader_tons_layout()
    elif pathname == '/shovels-per-load':
        return shovels_per_load_layout()
    elif pathname == '/truck-cycle-analysis':
        return truck_cycle_analysis_layout()
    elif pathname == '/loader-cycle-analysis':
        return loader_cycle_analysis_layout()
    elif pathname == '/empty-distance-analysis':
        return empty_distance_analysis_layout()
    elif pathname == '/loaded-distance-analysis':
        return loaded_distance_analysis_layout()
    else:
        return html.Div(children=[
            html.H1('Bienvenido'),
            html.P('Seleccione las secciones para visualizar los análisis')
        ])

register_monthly_callbacks(app)
if __name__ == '__main__':
    app.run_server(debug=False)
