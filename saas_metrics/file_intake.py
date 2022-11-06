import pandas as pd


def read_sample_1():
    """
    *POC*
    This function is not generalized to handle generic files
    Only specifically handles Sample 1
    """

    df = pd.read_csv('sample_data/Sample 1 raw data.csv', skiprows=2)

    df.rename(columns={'Customer ID': 'id', 'Industry': 'industry'}, inplace=True)
    df.loc[:, 'id'] = df.loc[:, 'id'].replace("[$,]", "", regex=True).astype(int)
    df_revenue = df.filter(items=['2017', '2018', '2019', '2020'], axis='columns')

    return df_revenue
