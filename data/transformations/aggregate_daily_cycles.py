import pandas as pd
def aggregate_daily_cycles()->pd.DataFrame:
    """
    Aggregates the total number of cycles per day

    Returns:
    pd.DataFrame: A DataFrame containing:
    - date, datetime: day
    - daily_cycles, int: The total number of cycles for that day
    """
    df_path = 'files/timeseries_haul_loading_data.csv'

    df = pd.read_csv(df_path)

    daily_cycles = df.groupby('date').size().reset_index(name='daily_cycles')
    daily_cycles['date'] = pd.to_datetime(daily_cycles['date'])

    return daily_cycles