import pandas as pd

def aggregate_daily_active_trucks()->pd.DataFrame:
    """
    Aggregates the total number of active trucks per day

    Returns:
    pd.DataFrame: A DataFrame containing:
    - date, datetime: day
    - daily_active_trucks, int: The total number of active trucks for that day
    """

    df_path = 'files/timeseries_haul_loading_data.csv'
    df = pd.read_csv(df_path)

    df = df[['date', 'truck']]
    df = df.drop_duplicates()

    daily_truck_cycles = df.groupby('date').size().reset_index(name='daily_active_trucks')
    daily_truck_cycles['date'] = pd.to_datetime(daily_truck_cycles['date'])

    return daily_truck_cycles