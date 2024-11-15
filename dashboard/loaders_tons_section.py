import pandas as pd
import plotly.graph_objs as go
from dash import html, dcc, dash_table

def zero_tons_rows_table()->dash_table.DataTable:
    df = pd.read_csv('files/timeseries_haul_loading_data.csv')
    zero_tons_rows = df[df['ton'] == 0]
    return dash_table.DataTable(
        id='zero-tons-rows',
        columns=[{'name': i, 'id': i} for i in zero_tons_rows.columns],
        data=zero_tons_rows.to_dict('records')
    )

def plot_tons_dists()->go.Figure:
    df = pd.read_csv('files/timeseries_haul_loading_data.csv')
    df = df[df['ton'] != 0]

    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=df['ton'],
            nbinsx=100
        )
    )
    fig.update_layout(
        title='Distribución de toneladas de todos los cargadores',
        xaxis_title='Toneladas',
        yaxis_title='Frecuencia'
    )

    return fig

def plot_loaders_ton_dist()->go.Figure:

    df = pd.read_csv('files/timeseries_haul_loading_data.csv')
    df = df[df['ton'] != 0]
    df = df.groupby('loader')

    fig = go.Figure()
    for loader in df.groups:

        loader_data = df.get_group(loader)
        fig.add_trace(
            go.Histogram(
                x=loader_data['ton'],
                nbinsx=100,
                name=loader
            )
        )

    fig.update_layout(
        title='Distribución de toneladas transportadas por cargador',
        xaxis_title='Toneladas',
        yaxis_title='Frecuencia'
    )

    return fig

def plot_ton_statistics_by_charger_vs_time() -> html.Div:
    # Leer y procesar datos
    df = pd.read_csv('files/timeseries_haul_loading_data.csv')
    df = df[['date', 'loader', 'ton']]
    df = df[df['ton'] != 0]
    df['date'] = pd.to_datetime(df['date'])

    # Agregaciones
    df = df.groupby(['date', 'loader']).agg(
        sum=('ton', 'sum'),
        min=('ton', 'min'),
        max=('ton', 'max'),
        mean=('ton', 'mean'),
        median=('ton', 'median'),
        Q1=('ton', lambda x: x.quantile(0.25)),
        Q3=('ton', lambda x: x.quantile(0.75))
    ).reset_index()

    df = df.sort_values('date')

    figs = []
    fig = go.Figure()
    for loader in df['loader'].unique():
        loader_data = df[df['loader'] == loader]
        fig.add_trace(
            go.Scatter(
                x=loader_data['date'],
                y=loader_data['mean'],
                name=loader,
                mode='lines',
                legendgroup=loader
            )
        )

        fig.add_trace(
            go.Scatter(
                x=loader_data['date'],
                y=loader_data['mean'],
                name=loader,
                mode='lines',
                legendgroup=loader
            )
        )

        fig.update_layout(
            title='Promedio y mediana de toneladas diarias',
            xaxis_title='Fecha',
            yaxis_title='Toneladas')
    
    figs.append(fig)

    statistics = [
        ('sum', 'Toneladas diarias totales'),
        ('min', 'Toneladas diarias mínimas'),
        ('max', 'Toneladas diarias máximas'),
        ('Q1', 'Q1 de toneladas diarias'),
        ('Q3', 'Q3 de toneladas diarias')
    ]

    for stat, title in statistics:
        fig = go.Figure()
        for loader in df['loader'].unique():
            loader_data = df[df['loader'] == loader]

            fig.add_trace(
                go.Scatter(
                    x=loader_data['date'],
                    y=loader_data[stat],
                    name=loader,
                    mode='lines',
                    legendgroup=loader,
                )
            )
            fig.update_layout(
                title=title,
                xaxis_title='Fecha',
                yaxis_title='Toneladas'
            )

        figs.append(fig)

    return html.Div(children=[dcc.Graph(figure=fig) for fig in figs])


loaders_dists_texts = ["""
Las distrubiciones de las toneladas cargadas por cada tipo de unidad son normales prácticamente
perfectas. Veamos la curva que describen al estandarizar los datos."""
]
loaders_dists_analysis = [html.P(text) for text in loaders_dists_texts]
def plot_loaders_tons_normalized_dists()->go.Figure:
    df = pd.read_csv('files/timeseries_haul_loading_data.csv')
    df = df[df['ton'] != 0]
    mean = df['ton'].mean()
    std = df['ton'].std()
    df['ton'] = df['ton'].apply(lambda x: (x - mean) / std)
    df = df.groupby('loader')
    fig = go.Figure()
    for loader in df.groups:
        loader_data = df.get_group(loader)
        fig.add_trace(
            go.Histogram(
                x=loader_data['ton'],
                nbinsx=100,
                name=loader,
                histnorm='probability'
            )
        )
    fig.update_layout(
        title=f'Distribución estandarizada de toneladas transportadas por cargadores',
        xaxis_title='Toneladas',
        yaxis_title='Frecuencia abosluta'
    )

    return fig

analysis_1_texts = ["""
Dadas las distribuciones que hemos visto hasta el momento, es relevante considerar escalar los
datos con scalers adecuados para distribuciones cuasi-normales, tales como StandardScaler que
recién hemos aplicado."""]

analysis_1 = [html.P(text) for text in analysis_1_texts]

introduction_2_texts = ["""
Habiendo analizado las distribuciones de las toneladas transportadas por los cargadores durante
todo el periodo de tiempo, es relevante considerar si su distribución varía en el tiempo."""]
introduction_2 = [html.P(text) for text in introduction_2_texts]

analysis_2_text = """
El comportamiento general de las variables es estático con variaciones a priori atribuibles a la
aleatoriedad de los datos. Concluimos entonces que las toneladas cargadas por cada unidad no
presenta variaciones significativas en el tiempo y que acumuladas en el tiempo se comportan como
una distribución normal."""
analysis_2 = html.P(analysis_2_text)
    
def layout()-> html.Div:
    return html.Div(
        id='loaders',
        children=[
            html.H2('Cargadores'),
            html.Hr(),
            html.P('Se detectaron los siguientes registros con 0 toneladas transportadas:'),
            zero_tons_rows_table(),
            dcc.Graph(
                id='loaders-tons-dists',
                figure=plot_tons_dists()
            ),
            dcc.Graph(
                id='loaders-tons-dists-by-loader',
                figure=plot_loaders_ton_dist()
            ),
            *loaders_dists_analysis,
            dcc.Graph(
                id='loaders-tons-dists-normalized',
                figure=plot_loaders_tons_normalized_dists()
            ),
            *analysis_1,
            html.Hr(),
            *introduction_2,
            plot_ton_statistics_by_charger_vs_time(),
            analysis_2
        ])