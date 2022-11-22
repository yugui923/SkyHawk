# import dependencies
import pandas as pd

from saas_metrics import file_intake, data_cleansing, saas_metrics, visualize

# import and clean up raw flat file
df_revenue = file_intake.read_sample_1()
df_revenue = data_cleansing.clean_df_revenue(df_revenue)

# initial analysis instance
analysis = saas_metrics.SaaSMetrics(df_revenue)

# calculate summaries of $ARR and #customers
revenue_summary = analysis.revenue_delta_summary()
customer_summary = analysis.customer_delta_summary()

# TODO visualize
visualize.heatmap(revenue_summary.iloc[:, :6])
visualize.heatmap(customer_summary.iloc[:, :6])

# TODO Export chart to Excel
excel_writer = pd.ExcelWriter('output_sample_1.xlsx', engine='xlsxwriter')
revenue_summary.to_excel(excel_writer, sheet_name='Revenue Summary')
customer_summary.to_excel(excel_writer, sheet_name='Customer Summary')

excel_writer.save()

input('end of main')
