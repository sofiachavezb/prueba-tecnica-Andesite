from data import *
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc
from plotly.subplots import make_subplots

def graph_all_daily_tons_dist():
    daily_tons = aggregate_daily_tons()
    hist = px.histogram(daily_tons, 
                        x='daily_tons', 
                        title='Distribución de toneladas diarias totales en todo el periodo')
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
            name='Toneladas diarias totales a lo largo del tiempo'
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
        yaxis_title='Cantidad de ciclos',
        )
    fig.update_yaxes(range=[0, daily_tons['daily_tons'].max()*1.1])
    
    return fig

def graph_daily_tons_vs_cycles_scatter():
    daily_tons = aggregate_daily_tons()
    daily_cycles = aggregate_daily_cycles()
    daily_tons['daily_cycles'] = daily_cycles['daily_cycles']
    fig = px.scatter(daily_tons, y='daily_tons', x='daily_cycles', title='Toneladas totales diarias vs ciclos diarios')
    fig.update_layout(
        yaxis_title='Toneladas diarias',
        xaxis_title='Cantidad de ciclos diarios',
        )
    return fig

def graph_daily_tons_vs_cycles_double_axis_dist():
    daily_tons = aggregate_daily_tons()
    daily_cycles = aggregate_daily_cycles().set_index('date')
    daily_tons = daily_tons.join(daily_cycles, on='date')
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=daily_tons['date'], 
            y=daily_tons['daily_tons'], 
            mode='lines', 
            name='Toneladas diarias'
        ),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=daily_tons['date'], 
        y=daily_tons['daily_cycles'], 
        mode='lines', 
        name='Ciclos diarios'),
        secondary_y=True
    )

    fig.update_layout(
        title='Toneladas totales y ciclos diarios a lo largo del tiempo',
        xaxis_title='Fecha', 
        yaxis_title='Toneladas diarias',
        )
    return fig

def graph_daily_tons_vs_cycles_dists():
    daily_tons = aggregate_daily_tons()
    daily_cycles = aggregate_daily_cycles().set_index('date')
    daily_tons = daily_tons.join(daily_cycles, on='date')
    min_cycles = daily_tons['daily_cycles'].min()
    max_cycles = daily_tons['daily_cycles'].max()
    min_tons = daily_tons['daily_tons'].min()
    max_tons = daily_tons['daily_tons'].max()
    cycles = daily_tons['daily_cycles']
    cycles = cycles.apply(lambda x: (x-min_cycles)/(max_cycles-min_cycles))
    tons = daily_tons['daily_tons']
    tons = tons.apply(lambda x: (x-min_tons)/(max_tons-min_tons))

    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=cycles,
            name='Ciclos diarios',
            histnorm='probability',
        )
    )
    fig.add_trace(
        go.Histogram(
            x=tons,
            name='Toneladas diarias',
            histnorm='probability',
        )
    )

    fig.update_layout(
        title='Distribuciones (normalizadas) de toneladas totales y ciclos diarios en todo el periodo',
        xaxis_title='Valor normalizado',
        yaxis_title='Densidad',
        )
    return fig


introduction_texts = ["""
Como la variable más relevante son las toneladas producidas, debemos analizar si están bien
representadas en datos, para ello comparamos la distribución de las toneladas diarias con la
distribución de los ciclos diarios.
""",
"""
Es esperable que haya una fuerte correlación entre la cantidad de tonealdas producidas y la 
cantidad de ciclos diarios, ya que una mayor extracción de material debería implicar un aumento
en la cantidad de ciclos. Si bien tanto el camión como el cargador pueden aumentar la canditdad de
material cargado y movido, existen límites para esto y es esperable que en un proceso eficiente
se minimicen los viajes innecesarios, distancias vacías y tiempos muertos.
"""]
introduction = [html.P(text) for text in introduction_texts]


analysis_1_text = """
Se presenta una clara relación lineal entre la cantidad de tonealdas producidas y la cantidad de
ciclos diarios. La dispersión de los datos es baja, lo que da muestra de un proceso consistente
"""
analysis_1 = html.P(analysis_1_text)
analysis_2_text = """
Las distribuciones de tonelaje movido y cantidad de Ciclos son prácticamente idénticas en forma,
tanto en su variación a lo largo del tiempo como en su distribución general."""
analysis_2 = html.P(analysis_2_text)
def layout() -> html.Div:
    return html.Div(
            id='daily-tons-section',
            children=[
                html.H1('Toneladas diarias', style={'textAlign':'center'}),
                * introduction,
                dcc.Graph(id='all-daily-tons-dist', figure=graph_all_daily_tons_dist()),
                dcc.Graph(id='daily-tons-dist', figure=graph_daily_tons_dist()),
                dcc.Graph(id='daily-tons-vs-cycles', figure=graph_daily_tons_vs_cycles_scatter()),
                analysis_1,
                dcc.Graph(id='daily-tons-vs-cycles-double-axis-dist', figure=graph_daily_tons_vs_cycles_double_axis_dist()),
                dcc.Graph(id='daily-tons-vs-cycles-dists', figure=graph_daily_tons_vs_cycles_dists()),
                analysis_2,
                ],
            )