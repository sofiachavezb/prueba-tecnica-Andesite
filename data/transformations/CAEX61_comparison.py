from typing import Tuple
import pandas as pd

def CAEX61_comparison()->Tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv('files/timeseries_haul_loading_data.csv')

    trucks_daily_cycles = df[['truck', 'date']].sort_values(by='truck')
    all_trucks = trucks_daily_cycles.groupby(['truck', 'date'], observed=True).size().reset_index(name='daily_cycles')
    
    CAEX_61 = all_trucks[all_trucks['truck'] == 'CAEX61']
    CAEX_61 = CAEX_61[['date', 'daily_cycles']]

    other_trucks = all_trucks[all_trucks['truck'] != 'CAEX61']
    other_trucks = other_trucks[['date', 'daily_cycles']].groupby('date', observed=False)
    other_trucks = other_trucks.agg(
        mean = ('daily_cycles', 'mean'),
        median = ('daily_cycles', 'median'),
        Q1 = ('daily_cycles', lambda x: x.quantile(0.25)),
        Q3 = ('daily_cycles', lambda x: x.quantile(0.75)),
        min = ('daily_cycles', 'min'),
    ).reset_index()

    return CAEX_61, other_trucks