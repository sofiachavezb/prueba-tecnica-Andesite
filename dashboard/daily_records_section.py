from typing import Dict
from data import *
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc

def graph_all_daily_records_dist():
    daily_records = aggregate_daily_records()
    hist = px.histogram(daily_records, 
                        x='daily_records', 
                        title='Distribución de registros diarios')
    hist.update_layout(
        xaxis_title='Cantidad de registros diarios',
        yaxis_title='Frecuencia absoluta',
        )
    return hist

def graph_daily_records_dist():
    daily_records = aggregate_daily_records()
    monthly_records = aggregate_monthly_records()
    monthly_records = monthly_records.set_index('month')
    daily_records['month'] = daily_records['date'].dt.to_period('M').astype(str)
    daily_records = daily_records.join(monthly_records, on='month')
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=daily_records['date'], 
            y=daily_records['daily_records'], 
            mode='lines', 
            name='Registros diarios')
    )
    fig.add_trace(
        go.Scatter(x=daily_records['date'], 
        y=daily_records['mean'], 
        mode='lines', 
        name='Promedio mensual')
    )
    fig.update_layout(
        title='Cantidad de registros diarios', 
        xaxis_title='Fecha', 
        yaxis_title='Cantidad de registros',
        )
    fig.update_yaxes(range=[0, daily_records['daily_records'].max()*1.1])
    
    return fig

daily_distribution_introduction_text = """
Primero analizaremos la cantidad de registros diarios para identificar si problemas en la cantidad
de datos en el tiempo."""
daily_distribution_introduction = html.P(daily_distribution_introduction_text)

daily_distribution_analysis_texts = ["""
La cantidad de registros diarios presenta variaciones, hay días con pocos registros que podrían 
indicar problemas en la recolección de datos. Sin embargo, no se aprecia que estos días presenten 
algún patrón en particular, se repiten más en algunos periodos como julio a junio de 2023, pero no
se concatenan varios días con bajos registros.""",
"""Cabe mencionar que una disminución en la cantidad de registros no necesariemente implica un 
problema, se podría explicar por otras razones que requieren conocimiento del contexto.""",
"""
Se observa un aumento en la cantidad de registros el 2024 frente al año anterior, no se observa un
efecto estacional claro en la cantidad de registros diarios, hay una leve oscilación pero requiere
una ventana de tiempo mayor para un resultado más concluyente.""",]
daily_distribution_analysis = [html.P(text) for text in daily_distribution_analysis_texts]

def layout() -> html.Div:
    """
    Sección de registros mensuales con gráficos interactivos y análisis.
    """
    section = html.Div(
        id='daily-records-section',
        children=[
            html.H1('Cantidad de registros diarios', style={'textAlign':'center'}),
            daily_distribution_introduction,
            dcc.Graph(id='all-daily-records-dist', figure=graph_all_daily_records_dist()),
            dcc.Graph(id='daily-records-dist', figure=graph_daily_records_dist()),
            *daily_distribution_analysis,
            ],
        )
    return section