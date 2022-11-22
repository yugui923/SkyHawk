"""
TODO convert columns to time range
"""
import numpy as np
import pandas as pd


def clean_df_revenue(df_revenue: pd.DataFrame) -> pd.DataFrame:
    """
    Remove special char
    Fill zeros in empty cells
    Change data type to float
    """

    df_revenue = df_revenue.replace("[$,– ]", "", regex=True) \
        .replace('', np.nan) \
        .dropna(axis='index', how='all') \
        .fillna(0)
    # TODO drop all 0 rows
    df_revenue = df_revenue.astype(float)

    return df_revenue
