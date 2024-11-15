import pandas as pd

def aggregate_trucks_daily_tons(only_active_trucks:bool)->pd.DataFrame:

    df_path = 'files/timeseries_haul_loading_data.csv'
    df = pd.read_csv(df_path)

    daily_truck_activity = df.groupby(['truck','date'], observed=only_active_trucks).agg(
        total_daily_cycles=('ton', 'count'),
        total_daily_tons=('ton', 'sum'),
        mean_daily_tons=('ton', 'mean'),
        median_daily_tons=('ton', 'median'),
        Q1_daily_tons=('ton', lambda x: x.quantile(0.25)),
        Q3_daily_tons=('ton', lambda x: x.quantile(0.75))
    )

    daily_truck_activity = daily_truck_activity.reset_index()
    daily_truck_activity['date'] = pd.to_datetime(daily_truck_activity['date'])

    return daily_truck_activity