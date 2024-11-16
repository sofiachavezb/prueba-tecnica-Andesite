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

empty_distance_analysis_texts = [
"""
Se observa una distribución multimodal con distintos picos que, a su vez, tienen frecuencias muy
distintas, pero cada uno se distingue fácilmente en la curva. Considerando que es muy importante
minimizar esta variable, esta distribución indica con claridad las principales distancias que los
camiones recorren vacíos y que seguramente están asociadas a procesos planificados, como carga, 
descarga o mantenimiento que son parte del ciclo de trabajo de los camiones.""",
"""
Además se observa que cada cargador está asociado a un pico de la distribución: PH06 a 5.3 KM,
PH48 a 7 KM, PH55 a 4KM y PH58 a 7.1 KM (aproximadamente). Tiene sentido que para cargar un camión
se deba recorrer una distancia vacía, esta información permite plantear posibles optimizaciones de 
rutas para dichos puntos.""",
"""
En general, los distintos camiones recorren distancias vacías casi idénticas en mediana. A fin de
evitar la sensibilidad del promedio a los outliers, en este caso consideramos esta métrica para 
cada par de (cargador, camión) y se observa que es muy constante entre los distintos camiones.
Sin embargo, notamos que CAEX61, el camión que previamente identificamos como nuevo, pero irregular,
se diferencia del resto en la mediana de la distancia vacía que recorre. Es necesario verificar 
si las rutas se han actualizado recientemente o si esta diferencia es atribuible al camión en 
particular. Una alternativa para ello es analizar la distribución de la distancia vacía del periodo
reciente.""",
"""
Junto con lo anterior, podemos profundizar en el análisis considerando no solo la mediana de los
camiones de cada cargador, sino la distribución de todas las rutas que pasaron por cada cargador.
""",
]
distance_empty_analysis = [html.P(text) for text in empty_distance_analysis_texts]
distance_dist_analysis_texts = ["""
Confirmamos que la asociación de cada cargador con un pico de la distribución de la distancia vacía
utilizando sólo la mediana es insuficiente, notamos que los picos de la distribución de la distancia
vacía de los camiones están asociados a distancias muy frecuentes recorridas desde los cargadores.
Todos puntos de mayor concentración se explican por rutas frecuentes, a la vez que las 
distribuciones de cada cargador sugieren una cantidad de rutas frecuentes específicas, existe un
grado de control sobre las distancias vacías recorridas, pero que puede ser mejorado. PH06 presenta
distancias típicas reconocibles, en cambio, PH48 tiene mucha menos concentración en torno a puntos
específicos, es más multimodal y en torno a cada moda no hay una concentración tan alta de rutas."""
]
distance_dist_analysis = [html.P(text) for text in distance_dist_analysis_texts]

recent_empty_distance_analysis_texts = ["""
Se observa que CAEX61 tiene un comportamiento casi indistinguible de los otros camiones, lo que
confirma que las distancias que habitualmente los camiones recorren vacíos han sufrido un cambio
reciente debido a un cambio en la planificación, este cambio no se explica por motivos aleatorios.
""","""
Queda analizar entonces si la distribución reciente de las distancias vacías indica rutas frecuentes
a optimizar o si es un comportamiento aleatorio."""]
recent_empty_distance_analysis = [html.P(text) for text in recent_empty_distance_analysis_texts]                                    

empty_distance_conclusion_texts = ["""
Es destacable que las distancias recorridas sin carga por sobre los 7 KM ahora son mucho menos
frecuentes y que los principales picos de la distribución están asociados a cargadores, lo que
sugiere un mayor control de esta variable. Sin embargo, las rutas de PH48 y PH58 sobre 6 KM siguen
alargando la cola de la distribución, sería recomendable revisar para qué se siguen utilizando 2 o
3 rutas de esa longitud. En contraste, PH06 presenta rutas de esa longitud, pero que se diferencian
más entre sí, a la vez que tiene una concentración muy alta en su ruta principal."""]
empty_distance_conclusion = [html.P(text) for text in empty_distance_conclusion_texts]
def layout()->html.Div:
    """
    Layout for the other variables analysis section
    """
    return html.Div(
        children=[
            html.H1("Análisis de la distancia recorrida sin carga"),
            html.Div(
                children=[
                    html.H3("Análisis de todo el periodo de tiempo"),
                    dcc.Graph(
                        figure=plot_variable_dist_for_period('distance_empty', None, None, 1000)),
                    dcc.Graph(
                        figure=plot_dist('distance_empty', 'median')
                    ),
                    *distance_empty_analysis,
                    dcc.Graph(
                        figure=plot_variable_dist_by_loader('distance_empty', overlay=True)
                    ),
                    *distance_dist_analysis,

                    html.H3("Análisis del periodo reciente"),
                    dcc.Graph(
                        figure=plot_variable_since_CAEX61('distance_empty', 'median')
                    ),
                    *recent_empty_distance_analysis,
                    dcc.Graph(
                        figure=plot_variable_dist_since_CAEX61('distance_empty')
                    ),
                    dcc.Graph(
                        figure=plot_variable_dist_by_loader_since_CAEX61('distance_empty')
                    ),
                    *empty_distance_conclusion,

                    html.H2("Distribución de la distancia recorrida con carga"),
                    html.P("En vista de lo anterior analizaremos tanto el periodo completo como el reciente"),
                    html.H3("Análisis del periodo completo"),
                    dcc.Graph(
                        figure=plot_variable_dist_for_period('distance_full', None, None, 1000)
                    ),
                    dcc.Graph(
                        figure=plot_dist('distance_full', 'median')
                    ),
                    dcc.Graph(
                        figure=plot_variable_dist_by_loader('distance_full', overlay=True)
                    ),
                    ]
            )
            ]
    )


                    


    