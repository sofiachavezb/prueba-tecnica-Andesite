from typing import Dict
from data import *
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc

def graph_daily_cycles_dist()->go.Figure:
    """
    Graph of the distribution of daily cycles across all the time
    """
    daily_cycles = aggregate_daily_cycles()
    hist = px.histogram(daily_cycles, 
                        x='daily_cycles', 
                        title='Distribución de ciclos diarios')
    hist.update_layout(
        xaxis_title='Cantidad de ciclos diarios',
        yaxis_title='Frecuencia absoluta',
        )
    return hist

def graph_daily_cycles_vs_time_dist()->go.Figure:
    """
    Graph of the distribution of daily cycles respect to time
    """
    daily_cycles = aggregate_daily_cycles()
    monthly_cycles = aggregate_monthly_cycles()
    monthly_cycles = monthly_cycles.set_index('month')
    daily_cycles['month'] = daily_cycles['date'].dt.to_period('M').astype(str)
    daily_cycles = daily_cycles.join(monthly_cycles, on='month')
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=daily_cycles['date'], 
            y=daily_cycles['daily_cycles'], 
            mode='lines', 
            name='Ciclos diarios')
    )
    fig.add_trace(
        go.Scatter(x=daily_cycles['date'], 
        y=daily_cycles['mean'], 
        mode='lines', 
        name='Promedio mensual')
    )
    fig.update_layout(
        title='Cantidad de ciclos diarios a lo largo del tiempo', 
        xaxis_title='Fecha', 
        yaxis_title='Cantidad de ciclos',
        )
    fig.update_yaxes(range=[0, daily_cycles['daily_cycles'].max()*1.1])
    
    return fig

daily_distribution_introduction_texts = ["""
Consideraremos como un ciclo a cada iteración de carga y transporte de un material.""",
"""Primero analizaremos la cantidad de ciclos diarios para identificar si problemas en los datos
disponibles en el tiempo"""]
daily_distribution_introduction = [html.P(text) for text in daily_distribution_introduction_texts]

daily_distribution_analysis_texts = ["""
La cantidad de ciclos diarios presenta variaciones, hay días con pocas iteraciones que podrían 
indicar problemas en la cadena de producción o en la recolección de datos. Sin embargo, no se 
detecta algún patrón en particular, se repiten más en algunos periodos como julio a junio de 2023, 
pero no se concatenan varios días con bajos ciclos.""",
"""Si bien existen variables exógenas que pueden afectar la cantidad de ciclos diarios, como
capacitaciones, mantenimientos o la recolección de datos, en este análisis consideraremos sólo
los datos disponibles.""",
"""Se observa un aumento en la cantidad de ciclos el 2024 frente al año anterior, no se observa un
efecto estacional claro en la cantidad de ciclos diarios, hay una leve oscilación pero requiere
una ventana de tiempo mayor para un resultado más concluyente.""",]
daily_distribution_analysis = [html.P(text) for text in daily_distribution_analysis_texts]

def daily_cycles_layout() -> html.Div:
    """
    Daily cycles section layout
    """
    section = html.Div(
        id='daily-cycles-section',
        children=[
            html.H1('Cantidad de ciclos diarios en todo el periodo', style={'textAlign':'center'}),
            *daily_distribution_introduction,
            dcc.Graph(id='all-daily-cycles-dist', figure=graph_daily_cycles_dist()),
            dcc.Graph(id='daily-cycles-dist', figure=graph_daily_cycles_vs_time_dist()),
            *daily_distribution_analysis,
            ],
        )
    return section