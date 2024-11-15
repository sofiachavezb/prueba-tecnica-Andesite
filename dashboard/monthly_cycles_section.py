from typing import Dict
from data import *
from plotly.subplots import make_subplots
from dash import html, dcc
from dash.dependencies import Output, Input

import plotly.express as px

import plotly.graph_objects as go
from plotly.subplots import make_subplots

def graph_detailed_monthly_dist() -> go.Figure:
    daily_cycles = aggregate_daily_cycles()
    daily_cycles['month'] = daily_cycles['date'].dt.to_period('M').astype(str)
    
    # Definir los límites del eje Y
    y_min = daily_cycles['daily_cycles'].min()
    y_max = daily_cycles['daily_cycles'].max()
    distances = y_max - y_min
    y_min -= 0.2 * distances
    y_max += 0.2 * distances
    
    n_months = len(daily_cycles['month'].unique())
    cols = 6
    rows = (n_months // cols) + (n_months % cols > 0)
    
    fig = make_subplots(rows=rows, 
                        cols=cols, 
                        subplot_titles=daily_cycles['month'].unique(),
                        horizontal_spacing=0.05,
                        vertical_spacing=0.05)

    for idx, month in enumerate(daily_cycles['month'].unique()):
        cycles = daily_cycles[daily_cycles['month'] == month]['daily_cycles']
        
        violin = go.Violin(y=cycles, name=month, box_visible=True, meanline_visible=True)
        
        row = (idx // cols) + 1
        col = (idx % cols) + 1
        fig.add_trace(violin, row=row, col=col)
        fig.update_yaxes(range=[y_min, y_max], row=row, col=col)

    fig.update_layout(
        title="Distribución de ciclos diarios por mes",
        yaxis=dict(title="Cantidad de ciclos diarios", 
        range=[y_min, y_max]),
        height=500 * rows,
    )

    return fig

def graph_comparative_monthly_dist() -> go.Figure:
    
    daily_cycles = aggregate_daily_cycles()
    daily_cycles['month'] = daily_cycles['date'].dt.to_period('M').astype(str)

    graph = px.violin(
                daily_cycles, 
                x='month', 
                y='daily_cycles', 
                box=True,
                orientation='v',
                title="Distribución de ciclos diarios por mes",
                labels={'month': 'Mes', 'cycles': 'Cantidad de ciclos diarios'},
                width=1000,
                height=500)
    
    graph.update_layout(
        yaxis=dict(title="Cantidad de ciclos diarios"),
        xaxis=dict(title="Mes"),
        violinmode='overlay'
    )
     
    return go.Figure(graph)

def graph_monthly_statistics() -> go.Figure:
    monthly_cycles = aggregate_monthly_cycles()
    monthly_cycles['month'] = monthly_cycles['month'].astype(str)
    
    names = {
        'mean': 'Promedio mensual',
        'median': 'Mediana mensual',
        'min': 'Mínimo mensual',
        'max': 'Máximo mensual',
        'Q1': 'Cuartil 1',
        'Q3': 'Cuartil 3'
    }

    fig = go.Figure()
    for column in names.keys():
        fig.add_trace(
            go.Scatter(
                x=monthly_cycles['month'],
                y=monthly_cycles[column],
                mode='lines',
                name=names[column],
            )
        )
    fig.update_layout(
        title='Estadísticas mensuales',
        xaxis_title='Mes',
        yaxis_title='Cantidad de ciclos',
        height=500
    )

    return fig


monthly_distribution_analysis_texts = [
"""
Para los distintos meses se observan distintas distribuciones de ciclos diarios.
Meses como julio de 2023 presentan una cola larga hacia los pocos ciclos, mientras que mayo de 
2024 es el caso contrario, con una cola menor para ciclos bajos que altos, aunque esta es menos
extensa que la cola inferior de julio de 2023.
""",
"""
Se observa que en general los meses presentan una distribución con una región central más densa,
con skews que varían según valores extremos y con una cantidad de ciclos que aumentan entre 2023
y 2024. La leve oscilación mencionada anteriormente se hace más visibe en estos gráficos.
"""
]

monthly_distribution_analysis = [html.P(text) for text in monthly_distribution_analysis_texts]

def layout() -> html.Div:
    section = html.Div(
        id='monthly-cycles-section',
        children=[
            html.H1('Distribuciones de cantidad de ciclos diarios por mes'),
            dcc.RadioItems(
                id='view-toggle',
                options=[
                    {'label': 'Vista general', 'value': 'general'},
                    {'label': 'Vista detallada', 'value': 'detailed'},
                    {'label': 'Estadísticas mensuales', 'value': 'statistics'}
                ],
                value='general',
                labelStyle={'display': 'inline-block', 'margin-right': '10px'}
            ),
            dcc.Graph(id='daily-cycles-month-dists'),
            *monthly_distribution_analysis
        ],
    )

    return section


def register_callbacks(app):
    @app.callback(
        Output('daily-cycles-month-dists', 'figure'),
        Input('view-toggle', 'value')
    )
    def update_monthly_view(view):
        if view == 'general':
            return graph_comparative_monthly_dist()
        elif view == 'detailed':
            return graph_detailed_monthly_dist()
        elif view == 'statistics':
            return graph_monthly_statistics()
        else:
            return graph_comparative_monthly_dist()