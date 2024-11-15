import pandas as pd
def load_dataset()->pd.DataFrame:
    df_path = 'files/timeseries_haul_loading_data.csv'
    df = pd.read_csv(df_path)
    df['date'] = pd.to_datetime(df['date'])
    return df