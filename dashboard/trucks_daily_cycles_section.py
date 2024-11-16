from typing import List
import pandas as pd
from data import aggregate_daily_active_trucks, aggregate_trucks_daily_tons, CAEX61_comparison
import plotly.graph_objs as go
from dash import html, dcc
from dash.dependencies import Output, Input

def graph_daily_trucks_vs_time()->go.Figure:
    """
    Graphs the number of daily active trucks over time
    """
    daily_truck_cycles = aggregate_daily_active_trucks()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=daily_truck_cycles['date'],
            y=daily_truck_cycles['daily_active_trucks'],
            mode='lines',
            name='Ciclos diarios'
        )
    )
    fig.update_layout(
        title='Camiones activos diarios',
        xaxis_title='Fecha',
        yaxis_title='Camiones activos'
    )

    return fig

def get_trucks_daily_cycles_statistics(only_active_trucks:bool)->pd.DataFrame:
    """
    Returns the daily cycles statistics across all the trucks.

    Args:
    only_active_trucks: If True, only the active trucks are considered. Else, trucks without
    cycles will add data with 0 cycles.

    Returns:
    pd.DataFrame: DataFrame with the daily cycles statistics
    """
    
    daily_trucks_activity = aggregate_trucks_daily_tons(only_active_trucks=only_active_trucks)
    daily_trucks_activity = daily_trucks_activity.groupby(['date'])['total_daily_cycles']
    daily_trucks_activity = daily_trucks_activity.agg([
        'mean',
        'median',
        'min',
        'max',
        lambda x: x.quantile(0.25),
        lambda x: x.quantile(0.75)
    ])
    daily_trucks_activity.columns = ['mean', 'median', 'min', 'max', 'Q1', 'Q3']
    daily_trucks_activity = daily_trucks_activity.reset_index()
    daily_trucks_activity['date'] = pd.to_datetime(daily_trucks_activity['date'])

    return daily_trucks_activity

active_trucks_daily_activity = get_trucks_daily_cycles_statistics(only_active_trucks=True)
all_trucks_daily_activity = get_trucks_daily_cycles_statistics(only_active_trucks=False)

def graph_trucks_daily_cycles_satistics()->go.Figure:
    """
    Graphs the selected statistics of the daily cycles of the trucks

    Args:
    selected_stats: List of statistics to be plotted: mean, median, min, max, Q1, Q3

    Returns:
    go.Figure: Plotly figure with the selected statistics
    """

    fig = go.Figure()
    for stat,name,show in [('mean', 'Promedio', False),
                           ('median', 'Mediana', True),
                           ('min', 'Mínimo', True),
                           ('max', 'Máximo', False),
                           ('Q1', 'Q1', True),
                           ('Q3', 'Q3', True)]:
        if stat == 'date':
            continue
        fig.add_trace(
            go.Scatter(
                x=active_trucks_daily_activity['date'],
                y=active_trucks_daily_activity[stat],
                mode='lines',
                name=name,
                visible=True if show else 'legendonly'
            )
        )

    fig.update_layout(
        title='Estadísticas de ciclos diarios de camiones',
        xaxis_title='Fecha',
        yaxis_title='Cantidad de ciclos diarios'
    )

    return fig

def graph_total_cycles_per_truck()->go.Figure:
    """
    Graphs the total cycles per truck
    """
    daily_trucks_activity = aggregate_trucks_daily_tons(only_active_trucks=False)
    daily_trucks_activity = daily_trucks_activity.drop(columns=['date'])
    daily_trucks_activity = daily_trucks_activity.groupby(['truck']).agg('sum')
    daily_trucks_activity = daily_trucks_activity.reset_index()
    daily_trucks_activity = daily_trucks_activity.sort_values(by='total_daily_cycles')

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=daily_trucks_activity['truck'],
            y=daily_trucks_activity['total_daily_cycles'],
            name='Ciclos totales'
        )
    )
    fig.update_layout(
        title='Ciclos totales por camión',
        xaxis_title='Camión',
        yaxis_title='Ciclos totales'
    )

    return fig

analysis_1_texts = ["""
Es relevante notar que el día que tuvo por lejos la menor cantidad de camiones activos, el 26 de
junio de 2023, la cantidad de ciclos diarios fue menor a su promedio mensual pero no está entre
los días con menor cantidad de ciclos. Ordenados de menor cantidad de ciclos a mayor, este 
día ocupa la posición 176
""",
"""
A su vez, el segundo día con menor cantidad de camiones activos, el 24 de agosto de 2023, aparece
en la posición 191 de menor cantidad de ciclos diarios, por lo que la cantidad de camiones
activos no parece ser un factor determinante en la cantidad de ciclos diarios.
"""]
analysis_1 = [html.P(text) for text in analysis_1_texts]

analysis_2_texts = ["""
Analizando el comportamiento de la cantidad de ciclos diarios entre los distintos camiones, si bien
anteriormente observamos un incremento general entre 2023 y 2024, Q3 aumenta más que Q1 y el mínimo
aunque presenta máximos mayores, en general se mantiene en el mismo rango de 1 a 4 ciclos. En este 
gráfico no incluimos camiones que no tuvieron ciclos en un día, por lo cual las curvas muestran que
no hay mejoras significativas en los "peores" camiones (en términos de ciclos diarios) disponibles
a lo largo del tiempo.
"""]
analysis_2 = [html.P(text) for text in analysis_2_texts]

analysis_3_text = """
El camión CAEX61 es el con menos ciclos realizados en todo el periodo. Analizaremos si se debe a
que es un camión nuevo en la flota"""
analysis_3 = html.P(analysis_3_text)

def plot_trucks_longevity()->go.Figure:

    df = pd.read_csv('files/timeseries_haul_loading_data.csv')
    df = df[['date', 'truck']]
    df['date'] = pd.to_datetime(df['date'])
    max_date = df['date'].max()
    df = df.groupby('truck')['date'].agg(['min','size'])
    df = df.sort_values(by='size')
    df['longevity'] = max_date - df['min']
    df['longevity'] = df['longevity'].dt.days

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['longevity'],
            name='Días desde el primer ciclo'
        )
    )
    fig.update_layout(
        title='Longevidad de los camiones',
        xaxis_title='Camión',
        yaxis_title='Días de actividad'
    )

    return fig

analysis_4_text = """
CAEX61 es un camión nuevo en la flota, por lo que es de esperar que tenga menos ciclos qe el resto.
Sin embargo, la cantidad de ciclos diarios es muy baja en comparación con el resto de los camiones,
analizaremos cómo se compara con el resto de los camiones."""
analysis_4 = html.P(analysis_4_text)

def graph_CAEX61_comparison()->go.Figure:
    """
    Graphs the comparison of the CAEX61 truck with the rest of the trucks
    """
    CAEX_61, other_trucks = CAEX61_comparison()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=CAEX_61['date'],
            y=CAEX_61['daily_cycles'],
            mode='lines',
            name='CAEX61'
        )
    )
    for col, name, show in [('Q3', 'Q3 de otros camiones', False), 
                            ('median', ('Mediana - Q2 de otros camiones'), False),
                            ('Q1', 'Q1 de otros camiones', True),
                            ('min', 'Mínimo de otros camiones', True)]:

        fig.add_trace(
            go.Scatter(
                x=other_trucks['date'],
                y=other_trucks[col],
                mode='lines',
                name=name,
                visible=True if show else 'legendonly'
            )
        )

    fig.update_layout(
        title = 'Comparación de ciclos diarios del camión CAEX61 con el resto de los camiones',
        xaxis_title = 'Fecha',
        yaxis_title = 'Ciclos diarios'
    )

    return fig

analysis_5_text = """
Concluimos que CAEX61 es un camión nuevo en la flota, pero que pese a ello no presenta un buen
rendimiento en términos de ciclos diarios, normalmente está en el primer cuartil de la cantidad de
ciclos."""
analysis_5 = html.P(analysis_5_text)


def layout()->html.Div:
    return html.Div(

        id='daily-truck-activity',
        children=[
            html.H1('Ciclos diarios de camiones'),
            dcc.Graph(figure=graph_daily_trucks_vs_time()),
            *analysis_1,
            dcc.Graph(figure=graph_trucks_daily_cycles_satistics()),
            *analysis_2,
            html.Hr(),
            html.H2('Peores camiones en cantidad de ciclos diarios'),
            html.Hr(),
            html.P("Ahora sí consideraremos los camiones que no tuvieron ciclos en un día"),
            dcc.Graph(figure=graph_total_cycles_per_truck()),
            analysis_3,
            dcc.Graph(figure=plot_trucks_longevity()),
            analysis_4,
            dcc.Graph(figure=graph_CAEX61_comparison()),
            analysis_5
        ]
    )
