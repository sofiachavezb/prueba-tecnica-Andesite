import pandas as pd
from data import aggregate_trucks_daily_tons
import plotly.graph_objs as go
from dash import html, dcc, dash_table
import plotly.express as px

def zero_tons_rows_table()->dash_table.DataTable:
    df = pd.read_csv('files/timeseries_haul_loading_data.csv')
    zero_tons_rows = df[df['ton'] == 0]
    return dash_table.DataTable(
        id='zero-tons-rows',
        columns=[{'name': i, 'id': i} for i in zero_tons_rows.columns],
        data=zero_tons_rows.to_dict('records')
    )

def graph_tons_distribution()->go.Figure:
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
        title='Distribución de toneladas transportadas en todo el periodo',
        xaxis_title='Toneladas',
        yaxis_title='Frecuencia'
    )

    return fig


graph_intro_text = """
El siguiente gráfico muestra las estadísticas de las toneladas transportadas por los camiones (
toneladas: Q1, Q2, Q3, promedio, suma ) para cada día, promediadas entre todos los camiones."""
graph_intro = html.P(graph_intro_text)


def graph_daily_trucks_tons_statistics():
    daily_trucks_activity = aggregate_trucks_daily_tons(only_active_trucks=True)
    daily_trucks_activity = daily_trucks_activity.drop(columns=['truck'])
    daily_trucks_activity = daily_trucks_activity.groupby(['date']).agg('mean')
    daily_trucks_activity = daily_trucks_activity.reset_index()
    daily_trucks_activity['date'] = pd.to_datetime(daily_trucks_activity['date'])

    fig = go.Figure()
    for col, name, show in [('total_daily_cycles', 'Ciclos diarios', False), 
                            ('total_daily_tons', 'Total de toneladas diarias', False),
                            ('mean_daily_tons', 'Promedio de toneladas diarias', False),
                            ('median_daily_tons', 'Mediana - Q2 de toneladas diarias', True),
                            ('Q1_daily_tons', 'Q1 de toneladas diarias', True),
                            ('Q3_daily_tons', 'Q3 de toneladas diarias', True)]:
        fig.add_trace(
            go.Scatter(
                x=daily_trucks_activity['date'],
                y=daily_trucks_activity[col],
                mode='lines',
                name=name,
                visible=True if show else 'legendonly'
            )
        )
    fig.update_layout(
        title='Estadísticas de toneladas diarias por camión (promediadas)',
        xaxis_title='Fecha',
        yaxis_title='Toneladas diarias'
    )

    return fig


def graph_daily_trucks_tons_heatmap():
    df = pd.read_csv('files/timeseries_haul_loading_data.csv')
    df = df[df['ton'] != 0]
    df = df.sort_values(by='date')

    fig = px.density_heatmap(
        df,
        x='date',           
        y='ton',            
        labels={'date': 'Fecha', 'ton': 'Toneladas'},
        color_continuous_scale= 'inferno',
    )

    fig.update_layout(
        title='Distribución de toneladas en el tiempo',
        xaxis_title='Fecha',
        yaxis_title='Toneladas',
        coloraxis_colorbar_title='Densidad'
    )

    return fig

def graph_monthly_total_tons_violins():

    df = pd.read_csv('files/timeseries_haul_loading_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M').astype(str)
    df = df[df['ton'] != 0][['month', 'ton']]
    
    fig = go.Figure()
    fig.add_trace(
        go.Violin(
            x=df['month'],
            y=df['ton'],
            box_visible=True,
            meanline_visible=True,
        )
    )
    fig.update_layout(
        title='Distribución de toneladas transportadas por mes',
        xaxis_title='Mes',
        yaxis_title='Toneladas',
    )

    return fig

month_violin_explanation_text = """
La distribución de toneladas transportadas en cada ciclo no presenta variaciones significativas
entre los meses, en general se asemejan a distribuciones normales."""
month_violin_explanation = html.P(month_violin_explanation_text)

trucks_statistics_means_text = """
En línea con lo anterior, los promedios de los cuartiles de las toneladas transportadas por cada 
camión varían en conjunto entre los meses, es decir, las cantidades en general se mueven, pero 
la distribución es, a grandes rasgos, la misma."""

trucks_statistics_means = html.P(trucks_statistics_means_text)

heatmap_text = """
El heatmap muestra la distribución de las toneladas transportadas en el mes, esta vez sin
agrupación por camión, por eso se observan mayores variaciones entre los meses En general, se
mantiene una concentración de toneladas en un punto medio, pero notamos que las dispersiones varían
más en el tiempo, bandas como 20 de Agosto de 2023 presentan una mayor std, una menor concentración,
mientras que en 26 de Noviembre de 2023 a 9 de Diciembre de 2023 se observa clara concentración."""


def layout()->html.Div:
    return html.Div(

        id='daily-truck-activity',
        children=[
            html.H1('Toneladas diarias de camiones'),
            html.Hr(),
            html.P('Analizamos las toneladas diarias de camiones. Detectamos dos datos problemáticos:'),
            zero_tons_rows_table(),
            html.P('Descartando esos datos, la distribución de toneladas en todo el periodo es la siguiente:'),
            dcc.Graph(
                id='daily-trucks-tons-distribution',
                figure=graph_tons_distribution()
            ),
            dcc.Graph(
                id='monthly-tons-violins',
                figure=graph_monthly_total_tons_violins()
            ),
            month_violin_explanation,
            graph_intro,
            dcc.Graph(
                id='daily-trucks-tons-statistics',
                figure=graph_daily_trucks_tons_statistics()
            ),
            trucks_statistics_means,
            dcc.Graph(
                id='daily-trucks-tons-heatmap',
                figure=graph_daily_trucks_tons_heatmap()
            ),
        ]
    )
