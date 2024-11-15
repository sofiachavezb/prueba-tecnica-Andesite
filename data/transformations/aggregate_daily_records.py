import pandas as pd
def aggregate_daily_records()->pd.DataFrame:
    """
    Aggregates the total number of records per day 

    Returns:
    pd.DataFrame: A DataFrame containing:
    - date, datetime: day
    - daily_records, int: The total number of records for that day
    """
    df_path = 'files/timeseries_haul_loading_data.csv'

    df = pd.read_csv(df_path)

    daily_records = df.groupby('date').size().reset_index(name='daily_records')
    daily_records['date'] = pd.to_datetime(daily_records['date'])

    return daily_records