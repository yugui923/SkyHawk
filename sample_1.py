# import dependencies
import pandas as pd

from saas_metrics import file_intake, calculate_metrics

# import and clean up raw flat file
df = file_intake.read_sample_1()
df.rename(columns={'Customer ID': 'id', 'Industry': 'industry'}, inplace=True)
df.loc[:, 'id'] = df.loc[:, 'id'].replace("[$,]", "", regex=True).astype(int)
df_revenue = df.filter(items=['2017', '2018', '2019', '2020'], axis='columns')

# calculate saas deltas for each user across time periods
results = calculate_metrics.calculate_five_saas_delta(df_revenue)

# generate $ of ARR summary table from saas delta dataframes
summary_col_names = [
    'total_churned',
    'total_contraction',
    'total_resurrected',
    'total_expansion',
    'total_new'
]

lst_dates = df_revenue.columns.tolist()
df_arr_summary = pd.DataFrame(index=lst_dates)
for i in range(len(results)):
    saas_delta_sum = pd.DataFrame(results[i].sum(axis=0), columns=[summary_col_names[i]])
    df_arr_summary = df_arr_summary.merge(saas_delta_sum, left_index=True, right_index=True, how='left')

ending_arr = pd.DataFrame(df_revenue.sum(axis=0), columns=['ending_arr'])
df_arr_summary = df_arr_summary.merge(ending_arr, left_index=True, right_index=True, how='left')

# generate # of customer summary table from saas delta dataframes
df_customer_summary = pd.DataFrame(index=lst_dates)  # TODO
for i in [0, 2, 4]:
    print(i)
    saas_delta_sum = pd.DataFrame(results[i].astype(bool).sum(axis=0), columns=[summary_col_names[i]])
    df_customer_summary = df_customer_summary.merge(saas_delta_sum, left_index=True, right_index=True, how='left')

# reverse sign for churned customers
df_customer_summary.loc[:, 'total_churned'] = -df_customer_summary.loc[:, 'total_churned']

ending_active_customers = pd.DataFrame(df_revenue.astype(bool).sum(axis=0), columns=['ending_active_customers'])
df_customer_summary = df_customer_summary.merge(ending_active_customers, left_index=True, right_index=True, how='left')

input('end of main')
