from dash import html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

static_df = pd.read_csv('files/timeseries_haul_loading_data.csv')

def plot_variable_dist_for_period(  variable:str, 
                                    x_min:float=None, 
                                    x_max:float=None,
                                    bins:int=None,
                                    df:pd.DataFrame = None)->go.Figure:
    if df is None:
        df = static_df
    df = df[df[variable] != 0]

    fig = go.Figure()
    if bins:
        trace = go.Histogram(x=df[variable], nbinsx=bins)
    else:
        trace = go.Histogram(x=df[variable])
    fig.add_trace(trace)

    layout_args = {
        'title': f'Distribución de {variable}',
        'xaxis_title': variable,
        'yaxis_title': 'Frecuencia'
    }
    if x_min is not None and x_max is not None:
        layout_args['xaxis'] = dict(range=[x_min, x_max])
    fig.update_layout(**layout_args)

    return fig

def plot_variable_dist_since_CAEX61(variable:str, df:pd.DataFrame=None)->go.Figure:
    if df is None:
        df = static_df
    df = df[df[variable] != 0]
    CAEX61_first_date = df[df['truck'] == 'CAEX61']['date'].min()
    df = df[df['date'] >= CAEX61_first_date]

    return plot_variable_dist_for_period(variable, df=df)


def plot_dist(target_variable: str, agg_func: str, df:pd.DataFrame=None)->go.Figure:
    if df is None:
        df = static_df
    df = df[['loader', 'truck', target_variable]]
    fig = go.Figure()
    if agg_func == 'Q1':
        agg_func_call = lambda x: x.quantile(0.25)
    elif agg_func == 'Q3':
        agg_func_call = lambda x: x.quantile(0.75)
    else:
        agg_func_call = agg_func
    for loader in df['loader'].unique():
        loader_data = df[df['loader'] == loader].drop(columns='loader')
        loader_data = loader_data.groupby('truck').agg(agg_func_call).reset_index()
        fig.add_trace(
            go.Bar(
                x=loader_data['truck'],
                y=loader_data[target_variable],
                name=loader
            )
        )
        
    fig.update_layout(
        xaxis_title='Camión',
        yaxis_title='truck '+agg_func,
        title=f'Distribución de {target_variable} por camión y cargador'
    )

    return fig

def plot_variable_dist_by_loader(   variable:str, 
                                    df:pd.DataFrame=None, 
                                    overlay:bool=False,
                                    xmin:float=None,
                                    xmax:float=None)->go.Figure:
    if df is None:
        df = static_df
    df = df[['loader', variable]]
    fig = go.Figure()
    for loader in df['loader'].unique():
        loader_data = df[df['loader'] == loader].drop(columns='loader')
        fig.add_trace(
            go.Histogram(
                x=loader_data[variable],
                name=loader,
                histnorm='probability density',
                opacity=0.6 if overlay else 1
                )
        )

    fig.update_layout(
        title=f'Distribución de {variable} por cargador',
        xaxis_title=variable,
        yaxis_title='Densidad de probabilidad',
        barmode='overlay' if overlay else 'group',
        xaxis=dict(range=[xmin, xmax]) if xmin is not None and xmax is not None else None
    )
    
    return fig

def plot_variable_dist_by_loader_since_CAEX61(variable:str, df:pd.DataFrame=None)->go.Figure:
    if df is None:
        df = static_df
    df = df[df[variable] != 0]
    CAEX61_first_date = df[df['truck'] == 'CAEX61']['date'].min()
    df = df[df['date'] >= CAEX61_first_date]

    return plot_variable_dist_by_loader(variable, df)

def plot_variable_since_CAEX61(variable:str, agg_func:str)->go.Figure:
    df = static_df
    df['date'] = pd.to_datetime(df['date'])
    df = df[df[variable] != 0]
    CAEX61_first_date = df[df['truck'] == 'CAEX61']['date'].min()
    df = df[df['date'] >= CAEX61_first_date]

    return plot_dist(variable, agg_func, df)

truck_cycle_analysis_texts = ["""
Se observa que los cargadores que en la sección anterior eran constantemente mejores, aunque por 
una muy leve diferencia, en este caso empeoran bastante su rendimiento, con una diferencia 
proporcionalmente mayor a su ventaja anterior.""","""
Además, la distribución de todo el periodo, camiones y cargadores no concentra su masa en su región
central, en cambio, se asemeja más a una distribución bimodal, con dos picos en 1650 y 3150. Es
fácilmente identificable que los cargadores se dividen en dos grupos, uno conformado por PH06 y 
PH55 que tienen picos claros y con ciclos de camiones más cortos, y otro conformado por PH48 y PH58
que tienen distribuciones más planas, incluso bimodales, con tiempos de ciclo más largos."""]
truck_cycle_analysis = [html.P(text) for text in truck_cycle_analysis_texts]
def layout()->html.Div:
    """
    Layout for the other variables analysis section
    """
    return html.Div(
        children=[
            html.H1("Análisis de la duración de los ciclos de camiones"),
            html.Div(
                children=[
                    
                    html.H2("Distribución de la duración de los ciclos de camiones"),
                    dcc.Graph(
                        figure=plot_variable_dist_for_period('truck_total_cycle', 0, 5000,400)),
                    dcc.Graph(
                        figure=plot_dist('truck_total_cycle', 'mean')
                    ),
                    dcc.Graph(
                        figure=plot_variable_dist_by_loader('truck_total_cycle', xmin=0, xmax=5000, overlay=True)
                    ),
                    *truck_cycle_analysis,

                ]
            )
        ]
    )
