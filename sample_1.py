# import dependencies
import pandas as pd

from saas_metrics import file_intake, data_cleansing, saas_metrics, visualize


# import and clean up raw flat file
df_revenue = file_intake.read_sample_1()
df_revenue = data_cleansing.clean_df_revenue(df_revenue)

# calculate saas deltas for each user across time periods
analysis = saas_metrics.SaaSMetrics(df_revenue)
analysis.calculate_five_saas_delta()

# generate $ of ARR summary table from saas delta dataframes
arr_summary = analysis.arr_delta_summary()

# generate # of customer summary table from saas delta dataframes
customer_summary = analysis.customer_delta_summary()

# TODO visualize
visualize.heatmap(arr_summary)
visualize.heatmap(customer_summary)


input('end of main')
