from typing import Dict
from data import *
from plotly.subplots import make_subplots
from dash import html, dcc
from dash.dependencies import Output, Input

import plotly.express as px

import plotly.graph_objects as go
from plotly.subplots import make_subplots

def graph_detailed_monthly_dist() -> go.Figure:
    daily_records = aggregate_daily_records()
    daily_records['month'] = daily_records['date'].dt.to_period('M').astype(str)
    
    # Definir los límites del eje Y
    y_min = daily_records['daily_records'].min()
    y_max = daily_records['daily_records'].max()
    distances = y_max - y_min
    y_min -= 0.2 * distances
    y_max += 0.2 * distances
    
    n_months = len(daily_records['month'].unique())
    cols = 6
    rows = (n_months // cols) + (n_months % cols > 0)
    
    fig = make_subplots(rows=rows, 
                        cols=cols, 
                        subplot_titles=daily_records['month'].unique(),
                        horizontal_spacing=0.05,
                        vertical_spacing=0.05)

    for idx, month in enumerate(daily_records['month'].unique()):
        records = daily_records[daily_records['month'] == month]['daily_records']
        
        violin = go.Violin(y=records, name=month, box_visible=True, meanline_visible=True)
        
        row = (idx // cols) + 1
        col = (idx % cols) + 1
        fig.add_trace(violin, row=row, col=col)
        fig.update_yaxes(range=[y_min, y_max], row=row, col=col)

    fig.update_layout(
        title="Distribución de registros diarios por mes",
        yaxis=dict(title="Cantidad de registros diarios", 
        range=[y_min, y_max]),
        height=500 * rows,
    )

    return fig

def graph_comparative_monthly_dist() -> go.Figure:
    
    daily_records = aggregate_daily_records()
    daily_records['month'] = daily_records['date'].dt.to_period('M').astype(str)

    graph = px.violin(
                daily_records, 
                x='month', 
                y='daily_records', 
                box=True,
                orientation='v',
                title="Distribución de registros diarios por mes",
                labels={'month': 'Mes', 'records': 'Cantidad de registros diarios'},
                width=1000,
                height=500)
    
    graph.update_layout(
        yaxis=dict(title="Cantidad de registros diarios"),
        xaxis=dict(title="Mes"),
        violinmode='overlay'
    )
     
    return go.Figure(graph)

def graph_monthly_statistics() -> go.Figure:
    monthly_records = aggregate_monthly_records()
    monthly_records['month'] = monthly_records['month'].astype(str)
    
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
                x=monthly_records['month'],
                y=monthly_records[column],
                mode='lines',
                name=names[column]
            )
        )
    fig.update_layout(
        title='Estadísticas mensuales',
        xaxis_title='Mes',
        yaxis_title='Cantidad de registros'
    )

    return fig


monthly_distribution_analysis_texts = [
"""
Para los distintos meses se observan distintas distribuciones de registros diarios.
Meses como julio de 2023 presentan una cola larga hacia los pocos registros, mientras mayo de 2024
es el caso contrario, con una cola más larga hacia los registros altos, aunque no tan pronunciada
como en julio de 2023.
""",
"""
Se observa que en general los meses presentan una distribución con una región central más densa,
con skews que varían según valores extremos y con una cantidad de registros que aumentan entre 2023
y 2024.
"""
]

monthly_distribution_analysis = [html.P(text) for text in monthly_distribution_analysis_texts]

def layout() -> html.Div:
    section = html.Div(
        id='monthly-records-section',
        children=[
            html.H1('Cantidad de registros mensuales por mes'),
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
            dcc.Graph(id='daily-records-month-dists'),
            *monthly_distribution_analysis
        ],
    )

    return section


def register_callbacks(app):
    @app.callback(
        Output('daily-records-month-dists', 'figure'),
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