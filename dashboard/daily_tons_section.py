from typing import Dict
from data import *
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc


def graph_all_daily_tons_dist():
    daily_tons = aggregate_daily_tons()
    hist = px.histogram(daily_tons, 
                        x='daily_tons', 
                        title='Distribución de toneladas diarias')
    hist.update_layout(
        xaxis_title='Toneladas diarias',
        yaxis_title='Frecuencia absoluta',
        )
    return hist


def graph_daily_tons_dist():
    daily_tons = aggregate_daily_tons()
    monthly_tons = aggregate_monthly_tons()
    monthly_tons = monthly_tons.set_index('month')
    daily_tons['month'] = daily_tons['date'].dt.to_period('M').astype(str)
    daily_tons = daily_tons.join(monthly_tons, on='month')
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=daily_tons['date'], 
            y=daily_tons['daily_tons'], 
            mode='lines', 
            name='Toneladas diarias'
        )
    )
    fig.add_trace(
        go.Scatter(x=daily_tons['date'], 
        y=daily_tons['mean'], 
        mode='lines', 
        name='Promedio mensual')
    )
    fig.update_layout(
        title='Toneladas diarias',
        xaxis_title='Fecha', 
        yaxis_title='Cantidad de registros',
        )
    fig.update_yaxes(range=[0, daily_tons['daily_tons'].max()*1.1])
    
    return fig


def layout() -> html.Div:
    return html.Div(
            id='daily-tons-section',
            children=[
                html.H1('Toneladas diarias', style={'textAlign':'center'}),
                dcc.Graph(id='all-daily-tons-dist', figure=graph_all_daily_tons_dist()),
                dcc.Graph(id='daily-tons-dist', figure=graph_daily_tons_dist())
                ],
            )