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

loader_total_cycle_analysis_texts = ["""
Caso análogo al de la cantidad de palas, distribuciones constantes entre los camiones y cargadores,
con PH06 y PH55 levemente menos eficientes que los otros dos cargadores.""","""
Se vuelve a presentar una distribución con masa concentrada en la región central, aunque en esa
región sea considerablemente uniforme. Es interesante analizar es constante y prolongada,
pero no porque las distribuciones entre los distintos cargadores neutralice los picos, sino porque 
todos los cargadores presentan distribuciones similares, casi uniformes en la región central, 
levemente desplazadas. Cabe analizar por qué tanto en conjunto, como a nivel individual, los ciclos
de carga son tan probable que duren 200 segundos como 400."""]
loader_total_cycle_analysis = [html.P(text) for text in loader_total_cycle_analysis_texts]

def layout()->html.Div:
    """
    Layout for the other variables analysis section
    """
    return html.Div(
        children=[
            html.H1("Análisis del tiempo de ciclo de los cargadores"),
            html.Div(
                children=[
                    html.H2("Distribución de la duración de los ciclos de cargadores"),
                    dcc.Graph(
                        figure=plot_variable_dist_for_period('loader_total_cycle', 0, 800, 4000)
                    ),
                    dcc.Graph(
                        figure=plot_dist('loader_total_cycle', 'mean')
                    ),
                    dcc.Graph(
                        figure=plot_variable_dist_by_loader('loader_total_cycle', overlay=True, xmin=0, xmax=800)
                    ),
                    *loader_total_cycle_analysis,
                    ]
            )
            ]
    )


                    


    