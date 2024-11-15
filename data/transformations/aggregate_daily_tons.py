import pandas as pd
def aggregate_daily_tons()->pd.DataFrame:
    """
    Aggregates the total tons for each day in the dataset.

    Returns:
    pd.DataFrame: A DataFrame containing:
    - date, datetime: day
    - daily_tons, float: total tons for that day
    """
    df_path = 'files/timeseries_haul_loading_data.csv'

    df = pd.read_csv(df_path)

    daily_tons = df.groupby('date')['ton'].sum().reset_index(name='daily_tons')
    daily_tons['date'] = pd.to_datetime(daily_tons['date'])

    return daily_tons