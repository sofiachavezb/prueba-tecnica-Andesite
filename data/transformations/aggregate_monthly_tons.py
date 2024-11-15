import pandas as pd
import numpy as np
from .aggregate_daily_tons import aggregate_daily_tons

def aggregate_monthly_tons()->pd.DataFrame:
    """
    Aggregates the total number of tons per month 

    Returns:
    pd.DataFrame: A DataFrame with:
    - 'month', str : The month 
    - 'sum', int : The total number of tons in that month
    - 'mean', float : The average number of daily tons in that month
    - 'median', float : The median number of daily tons in that month
    - 'std', float : The standard deviation of the daily tons in that month
    - 'min', int : The minimum number of daily tons in that month
    - 'max', int : The maximum number of daily tons in that month
    - 'Q1', float : The first quartile of the daily tons in that month
    - 'Q3', float : The third quartile of the daily tons in that month
    """

    daily_tons = aggregate_daily_tons()

    daily_tons['date'] = pd.to_datetime(daily_tons['date'])
    daily_tons['month'] = daily_tons['date'].dt.to_period('M')

    q1 = lambda x: np.percentile(x, 25)
    q3 = lambda x: np.percentile(x, 75)

    

    monthly_tons = daily_tons.groupby('month').agg(
        sum=('daily_tons', 'sum'),
        mean=('daily_tons', 'mean'),
        median=('daily_tons', 'median'),
        std=('daily_tons', 'std'),
        min=('daily_tons', 'min'),
        max=('daily_tons', 'max'),
        Q1=('daily_tons', q1),
        Q3=('daily_tons', q3)
    )

    monthly_tons = monthly_tons.reset_index()
    monthly_tons['month'] = monthly_tons['month'].astype(str)

    return monthly_tons

