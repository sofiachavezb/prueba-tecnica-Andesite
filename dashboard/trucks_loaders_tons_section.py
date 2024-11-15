import pandas as pd
import plotly.graph_objs as go
from dash import html, dcc, dash_table
import plotly.express as px

def plot_truck_vs_loader_tons():
    df = pd.read_csv('files/timeseries_haul_loading_data.csv')
    df = df[df['ton'] != 0]
    df = df.groupby(['truck', 'loader']).agg('sum').reset_index()
    fig = px.scatter(df, x='truck', y='loader', size='ton', color='ton')
    fig.update_layout(
        title='Toneladas transportadas por camión y cargador',
        xaxis_title='Camión',
        yaxis_title='Cargador'
    )
    return fig

def layout()-> html.Div:
    return html.Div(
        id='truck-loader-tons',
        children=[
            html.H1('Toneladas transportadas por camión y cargador'),
            dcc.Graph(
                id='truck-loader-tons-plot',
                figure=plot_truck_vs_loader_tons()
            )
        ])