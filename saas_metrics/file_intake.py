import pandas as pd


# import sample 1 raw data
def read_sample_1():
    df = pd.read_csv('sample_data/Sample 1 raw data.csv', skiprows=2)
    return df
