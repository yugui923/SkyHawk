import numpy as np
import pandas as pd

"""
TODO
convert columns to time range
"""


def clean_df_revenue(df_revenue: pd.DataFrame) -> pd.DataFrame:
    """
    Remove special char
    Fill zeros in empty cells
    Change data type to float
    """

    df_revenue.replace("[$,– ]", "", regex=True, inplace=True)
    df_revenue.replace('', np.nan, inplace=True)
    df_revenue.dropna(axis='index', how='all', inplace=True)
    df_revenue.fillna(0, inplace=True)
    # TODO drop all 0 rows
    df_revenue = df_revenue.astype(float)

    return df_revenue
