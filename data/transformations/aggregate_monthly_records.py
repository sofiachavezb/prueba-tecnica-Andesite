import pandas as pd
import numpy as np
from .aggregate_daily_records import aggregate_daily_records
def aggregate_monthly_records()->pd.DataFrame:
    """
    Aggregates the total number of records per month 

    Returns:
    pd.DataFrame: A DataFrame with:
    - 'month', str : The month 
    - 'sum', int : The total number of records in that month
    - 'mean', float : The average number of daily records in that month
    - 'median', float : The median number of daily records in that month
    - 'std', float : The standard deviation of the daily records in that month
    - 'min', int : The minimum number of daily records in that month
    - 'max', int : The maximum number of daily records in that month
    - 'Q1', float : The first quartile of the daily records in that month
    - 'Q3', float : The third quartile of the daily records in that month
    """

    daily_records = aggregate_daily_records()

    daily_records['date'] = pd.to_datetime(daily_records['date'])
    daily_records['month'] = daily_records['date'].dt.to_period('M')

    q1 = lambda x: np.percentile(x, 25)
    q3 = lambda x: np.percentile(x, 75)

    monthly_records = daily_records.groupby('month').agg(
        sum=('daily_records', 'sum'),
        mean=('daily_records', 'mean'),
        median=('daily_records', 'median'),
        std=('daily_records', 'std'),
        min=('daily_records', 'min'),
        max=('daily_records', 'max'),
        Q1=('daily_records', q1),
        Q3=('daily_records', q3)
    )

    monthly_records = monthly_records.reset_index()
    monthly_records['month'] = monthly_records['month'].astype(str)

    return monthly_records

