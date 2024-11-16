from dash import html, dcc
import pandas as pd
import plotly.graph_objects as go

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

def layout()->html.Div:
    """
    Layout for the other variables analysis section
    """
    return html.Div(
        children=[
            html.H1("Análisis la distancia recorrida con carga"),
            html.Div(
                children=[
                    html.H3("Análisis del periodo completo"),
                    html.P("En vista de lo anterior analizaremos tanto el periodo completo como el reciente"),
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


                    


    