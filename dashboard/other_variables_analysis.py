from dash import html, dcc
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_variable_period_dist(variable:str)->go.Figure:
    df = pd.read_csv('files/timeseries_haul_loading_data.csv')
    df = df[df[variable] != 0]

    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=df[variable],
            nbinsx=100
        )
    )

    fig.update_layout(
        title=f'Distribución de {variable} en todo el periodo',
        xaxis_title=variable,
        yaxis_title='Frecuencia'
    )

    return fig

def plot_3d_scatter(target_variable: str):
    df = pd.read_csv('files/timeseries_haul_loading_data.csv')
    df = df[['loader', 'truck', target_variable]]
    
    
    # Gráfico interactivo 3D
    fig = px.scatter_3d(
        df,
        x='loader',
        y='truck',
        z=target_variable,
        color='loader',
        hover_data=['truck', target_variable],
        title=f'{target_variable} por cargador y camión',
        labels={'loader': 'Cargador', 'truck': 'Camión', target_variable: 'Variable Objetivo'}
    )

    fig.update_traces(marker=dict(size=5))
    fig.update_layout(
        scene=dict(
            xaxis=dict(title="Loader"),
            yaxis=dict(title="Truck"),
            zaxis=dict(title=target_variable),
        ),
        height=800
    )
    return fig

def layout()->html.Div:
    """
    Layout for the other variables analysis section
    """
    variables = ['n_shovel','truck_total_cycle','loader_total_cycle','distance_empty','distance_full']
    return html.Div(
        children=[
            html.H1("Análisis de otras variables"),
            html.Div(
                children=[
                    html.H2("Distribución de cantidad de palas para una carga"),
                    dcc.Graph(
                        figure=plot_3d_scatter('n_shovel')
                    )
                ]
            )
            ]
    )


                    


    