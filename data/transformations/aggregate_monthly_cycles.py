import pandas as pd
import numpy as np
from .aggregate_daily_cycles import aggregate_daily_cycles
def aggregate_monthly_cycles()->pd.DataFrame:
    """
    Aggregates the total number of cycles per month 

    Returns:
    pd.DataFrame: A DataFrame with:
    - 'month', str : The month 
    - 'sum', int : The total number of cycles in that month
    - 'mean', float : The average number of daily cycles in that month
    - 'median', float : The median number of daily cycles in that month
    - 'std', float : The standard deviation of the daily cycles in that month
    - 'min', int : The minimum number of daily cycles in that month
    - 'max', int : The maximum number of daily cycles in that month
    - 'Q1', float : The first quartile of the daily cycles in that month
    - 'Q3', float : The third quartile of the daily cycles in that month
    """

    daily_cycles = aggregate_daily_cycles()

    daily_cycles['date'] = pd.to_datetime(daily_cycles['date'])
    daily_cycles['month'] = daily_cycles['date'].dt.to_period('M')

    q1 = lambda x: np.percentile(x, 25)
    q3 = lambda x: np.percentile(x, 75)

    monthly_cycles = daily_cycles.groupby('month').agg(
        sum=('daily_cycles', 'sum'),
        mean=('daily_cycles', 'mean'),
        median=('daily_cycles', 'median'),
        std=('daily_cycles', 'std'),
        min=('daily_cycles', 'min'),
        max=('daily_cycles', 'max'),
        Q1=('daily_cycles', q1),
        Q3=('daily_cycles', q3)
    )

    monthly_cycles = monthly_cycles.reset_index()
    monthly_cycles['month'] = monthly_cycles['month'].astype(str)

    return monthly_cycles

