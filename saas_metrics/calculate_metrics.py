import numpy as np
import pandas as pd


def calculate_five_saas_delta(df_revenue):
    """
    returns a tuple of 5 dataframes:
        results[0]: churned
        results[1]: contracted
        results[2]: resurrected
        results[3]: expansion
        results[4]: new
    """

    n_time_periods = len(df_revenue.columns)

    # change data type to float and fill zeros
    for i in range(n_time_periods):
        df_revenue.iloc[:, i] = df_revenue.iloc[:, i].replace("[$,– ]", "", regex=True)
        df_revenue.replace('', np.nan, inplace=True)
        df_revenue.fillna(0, inplace=True)
        df_revenue.iloc[:, i] = df_revenue.iloc[:, i].astype(float)

    # calculate analysis helpers
    df_analysis_helper = pd.DataFrame(index=df_revenue.index)
    df_analysis_helper['first_time'] = df_revenue.ne(0).idxmax(axis='columns')
    df_analysis_helper['n_first_time'] = df_analysis_helper['first_time'].apply(
        lambda x: df_revenue.columns.to_list().index(x)
    )

    # calculate churned revenue
    df_churned = pd.DataFrame(index=df_revenue.index)
    for i in range(n_time_periods - 1):
        i = i + 1  # align i with current period (second period)
        condition = (
                (df_revenue.iloc[:, i - 1] > 0) &
                (df_revenue.iloc[:, i] == 0)
        )
        new_column = pd.DataFrame(np.where(
            condition,
            -df_revenue.iloc[:, i - 1],
            0
        ))
        df_churned = pd.concat([df_churned, new_column], axis='columns')
    df_churned.set_axis(df_revenue.columns[1:].to_list(), axis='columns', inplace=True)

    # calculate contraction revenue
    df_contraction = pd.DataFrame(index=df_revenue.index)
    for i in range(n_time_periods - 1):
        i = i + 1  # align i with current period (second period)
        condition = (
                (df_revenue.iloc[:, i - 1] > 0) &
                (df_revenue.iloc[:, i] > 0) &
                (df_revenue.iloc[:, i] < df_revenue.iloc[:, i - 1])
        )
        new_column = pd.DataFrame(np.where(
            condition,
            df_revenue.iloc[:, i] - df_revenue.iloc[:, i - 1],
            0
        ))
        df_contraction = pd.concat([df_contraction, new_column], axis='columns')
    df_contraction.set_axis(df_revenue.columns[1:].to_list(), axis='columns', inplace=True)

    # calculate resurrected revenue
    df_resurrected = pd.DataFrame(index=df_revenue.index)
    for i in range(n_time_periods - 1):
        i = i + 1  # align i with current period (second period)
        condition = (
                (df_revenue.iloc[:, i - 1] == 0) &
                (df_revenue.iloc[:, i] > 0) &
                (i > df_analysis_helper.loc[:, 'n_first_time'])
        )
        new_column = pd.DataFrame(np.where(
            condition,
            df_revenue.iloc[:, i],
            0
        ))
        df_resurrected = pd.concat([df_resurrected, new_column], axis='columns')
    df_resurrected.set_axis(df_revenue.columns[1:].to_list(), axis='columns', inplace=True)

    # calculate expansion revenue
    df_expansion = pd.DataFrame(index=df_revenue.index)
    for i in range(n_time_periods - 1):
        i = i + 1  # align i with current period (second period)
        condition = (
                (df_revenue.iloc[:, i - 1] > 0) &
                (df_revenue.iloc[:, i] > df_revenue.iloc[:, i - 1])
        )
        new_column = pd.DataFrame(np.where(
            condition,
            df_revenue.iloc[:, i] - df_revenue.iloc[:, i - 1],
            0
        ))
        df_expansion = pd.concat([df_expansion, new_column], axis='columns')
    df_expansion.set_axis(df_revenue.columns[1:].to_list(), axis='columns', inplace=True)

    # calculate new revenue
    df_new = pd.DataFrame(index=df_revenue.index)
    for i in range(n_time_periods - 1):
        i = i + 1  # align i with current period (second period)
        condition = (
                (df_revenue.iloc[:, i - 1] == 0) &
                (df_revenue.iloc[:, i] > 0) &
                (i == df_analysis_helper.loc[:, 'n_first_time'])
        )
        new_column = pd.DataFrame(np.where(
            condition,
            df_revenue.iloc[:, i],
            0
        ))
        df_new = pd.concat([df_new, new_column], axis='columns')
    df_new.set_axis(df_revenue.columns[1:].to_list(), axis='columns', inplace=True)

    return df_churned, df_contraction, df_resurrected, df_expansion, df_new
