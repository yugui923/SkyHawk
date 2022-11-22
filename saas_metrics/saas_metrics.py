"""
v0.1.0
"""

import numpy as np
import pandas as pd

from saas_metrics import data_validator


class SaaSMetrics:
    def __init__(self, df_revenue: pd.DataFrame):
        # store revenue DataFrame
        self.df_revenue_by_customer = df_revenue

        # initialize 5 internal dataframes
        self.df_churned = pd.DataFrame()
        self.df_contraction = pd.DataFrame()
        self.df_resurrected = pd.DataFrame()
        self.df_expansion = pd.DataFrame()
        self.df_new = pd.DataFrame()

        # initialize summary dataframes
        self.df_revenue_summary = None
        self.df_customer_summary = None

    def _check_five_saas_delta_calculation(self):
        """
        check if the 5 SaaS delta dataframes are calculated
        if not, call calculation function
        """
        for df in [self.df_churned,
                   self.df_contraction,
                   self.df_resurrected,
                   self.df_expansion,
                   self.df_new
                   ]:
            # if columns number less than 1, the call calculation function
            if df.shape[1] < 1:
                self.calculate_five_saas_delta()
                break
        return 0

    def calculate_five_saas_delta(self):
        """
        calculate the 5 SaaS deltas and return a tuple of 5 dataframes:
            results[0]: churned
            results[1]: contraction
            results[2]: resurrected
            results[3]: expansion
            results[4]: new
        """
        print("calculating 5 SaaS delta dataframes...")

        # validate revenue dataframe before starting data manipulation
        if data_validator.validate_df_revenue(self.df_revenue_by_customer):
            print('ERROR: revenue dataframe does not pass data validation')

        # calculate analysis helpers
        df_analysis_helper = pd.DataFrame(index=self.df_revenue_by_customer.index)
        df_analysis_helper['first_time_as_customer'] = self.df_revenue_by_customer.ne(0).idxmax(axis='columns')
        df_analysis_helper['n_first_time_as_customer'] = self.df_revenue_by_customer.columns.get_indexer(
            df_analysis_helper['first_time_as_customer'])

        n_time_periods = len(self.df_revenue_by_customer.columns)

        # calculate the revenue delta attributable to churned customers
        self.df_churned = pd.DataFrame(index=self.df_revenue_by_customer.index)
        for i in range(n_time_periods - 1):
            i = i + 1  # align i with current period (second period)
            condition = (
                    (self.df_revenue_by_customer.iloc[:, i - 1] > 0) &
                    (self.df_revenue_by_customer.iloc[:, i] == 0)
            )
            new_column = pd.DataFrame(
                np.where(condition, -self.df_revenue_by_customer.iloc[:, i - 1], 0),
                index=self.df_revenue_by_customer.index)
            self.df_churned = pd.concat([self.df_churned, new_column], axis='columns')
        self.df_churned = self.df_churned.set_axis(self.df_revenue_by_customer.columns[1:].to_list(), axis='columns')

        # calculate the revenue delta attributable to contraction customers
        self.df_contraction = pd.DataFrame(index=self.df_revenue_by_customer.index)
        for i in range(n_time_periods - 1):
            i = i + 1  # align i with current period (second period)
            condition = (
                    (self.df_revenue_by_customer.iloc[:, i - 1] > 0) &
                    (self.df_revenue_by_customer.iloc[:, i] > 0) &
                    (self.df_revenue_by_customer.iloc[:, i] < self.df_revenue_by_customer.iloc[:, i - 1])
            )
            new_column = pd.DataFrame(
                np.where(condition, self.df_revenue_by_customer.iloc[:, i] - self.df_revenue_by_customer.iloc[:, i - 1],
                         0), index=self.df_revenue_by_customer.index)
            self.df_contraction = pd.concat([self.df_contraction, new_column], axis='columns')
        self.df_contraction = self.df_contraction.set_axis(self.df_revenue_by_customer.columns[1:].to_list(),
                                                           axis='columns')

        # calculate the revenue delta attributable to resurrected customers
        self.df_resurrected = pd.DataFrame(index=self.df_revenue_by_customer.index)
        for i in range(n_time_periods - 1):
            i = i + 1  # align i with current period (second period)
            condition = (
                    (self.df_revenue_by_customer.iloc[:, i - 1] == 0) &
                    (self.df_revenue_by_customer.iloc[:, i] > 0) &
                    (i > df_analysis_helper.loc[:, 'n_first_time_as_customer'])
            )
            new_column = pd.DataFrame(
                np.where(condition, self.df_revenue_by_customer.iloc[:, i], 0),
                index=self.df_revenue_by_customer.index)
            self.df_resurrected = pd.concat([self.df_resurrected, new_column], axis='columns')
        self.df_resurrected = self.df_resurrected.set_axis(self.df_revenue_by_customer.columns[1:].to_list(),
                                                           axis='columns')

        # calculate the revenue delta attributable to expansion customers
        self.df_expansion = pd.DataFrame(index=self.df_revenue_by_customer.index)
        for i in range(n_time_periods - 1):
            i = i + 1  # align i with current period (second period)
            condition = (
                    (self.df_revenue_by_customer.iloc[:, i - 1] > 0) &
                    (self.df_revenue_by_customer.iloc[:, i] > self.df_revenue_by_customer.iloc[:, i - 1])
            )
            new_column = pd.DataFrame(
                np.where(condition, self.df_revenue_by_customer.iloc[:, i] - self.df_revenue_by_customer.iloc[:, i - 1],
                         0), index=self.df_revenue_by_customer.index)
            self.df_expansion = pd.concat([self.df_expansion, new_column], axis='columns')
        self.df_expansion = self.df_expansion.set_axis(self.df_revenue_by_customer.columns[1:].to_list(),
                                                       axis='columns')

        # calculate the revenue delta attributable to new customers
        self.df_new = pd.DataFrame(index=self.df_revenue_by_customer.index)
        for i in range(n_time_periods - 1):
            i = i + 1  # align i with current period (second period)
            condition = (
                    (self.df_revenue_by_customer.iloc[:, i - 1] == 0) &
                    (self.df_revenue_by_customer.iloc[:, i] > 0) &
                    (i == df_analysis_helper.loc[:, 'n_first_time_as_customer'])
            )
            new_column = pd.DataFrame(
                np.where(condition, self.df_revenue_by_customer.iloc[:, i], 0),
                index=self.df_revenue_by_customer.index)
            self.df_new = pd.concat([self.df_new, new_column], axis='columns')
        self.df_new = self.df_new.set_axis(self.df_revenue_by_customer.columns[1:].to_list(), axis='columns')

        # checksum comparing total of 5 SaaS delta and the actual revenue delta over periods
        total_saas_delta = (self.df_churned.to_numpy().sum() +
                            self.df_contraction.to_numpy().sum() +
                            self.df_resurrected.to_numpy().sum() +
                            self.df_expansion.to_numpy().sum() +
                            self.df_new.to_numpy().sum())
        revenue_delta = (self.df_revenue_by_customer.iloc[:, -1].to_numpy().sum() -
                         self.df_revenue_by_customer.iloc[:, 0].to_numpy().sum())
        checksum_diff = total_saas_delta - revenue_delta

        print(f"completed: SaaS 5 delta calculation\n   checksum diff = {checksum_diff:.2f}")

        return 0

    def revenue_delta_summary(self):
        """
        generate $ of revenue delta summary table from SaaS delta dataframes
        """
        self._check_five_saas_delta_calculation()
        column_names = [
            'total_churned',
            'total_contraction',
            'total_resurrected',
            'total_expansion',
            'total_new'
        ]

        # sum up churned, contraction, resurrected, expansion, new revenues
        self.df_revenue_summary = pd.DataFrame(index=self.df_revenue_by_customer.columns.tolist())
        for i, df in enumerate([self.df_churned,
                                self.df_contraction,
                                self.df_resurrected,
                                self.df_expansion,
                                self.df_new
                                ]):
            saas_delta = pd.DataFrame(df.sum(axis='index'), columns=[column_names[i]])
            self.df_revenue_summary = self.df_revenue_summary.merge(saas_delta, left_index=True, right_index=True,
                                                                    how='left')

        # calculate ending revenue directly from raw revenue data
        ending_revenue = pd.DataFrame(self.df_revenue_by_customer.sum(axis=0), columns=['ending_revenue'])
        self.df_revenue_summary = self.df_revenue_summary.merge(ending_revenue, left_index=True, right_index=True,
                                                                how='left')

        # checksum comparing total of 5 SaaS delta and the actual revenue delta over periods
        total_saas_delta = self.df_revenue_summary.iloc[:, :5].fillna(0).to_numpy().sum()
        revenue_delta = ending_revenue.diff(axis=0).fillna(0).to_numpy().sum()
        total_checksum_diff = total_saas_delta - revenue_delta

        print(f'completed: revenue delta summary\n   checksum diff = {total_checksum_diff:.2f}')

        return self.df_revenue_summary

    def customer_delta_summary(self):
        """
        generate # of customer delta summary table from SaaS delta dataframes
        """
        self._check_five_saas_delta_calculation()
        column_names = [
            'total_churned',
            'total_resurrected',
            'total_new'
        ]

        # sum up churned, resurrected, new customers
        self.df_customer_summary = pd.DataFrame(index=self.df_revenue_by_customer.columns.tolist())
        for i, df in enumerate([self.df_churned,
                                self.df_resurrected,
                                self.df_new
                                ]):
            saas_delta = pd.DataFrame(df.astype(bool).sum(axis=0), columns=[column_names[i]])
            self.df_customer_summary = self.df_customer_summary.merge(saas_delta, left_index=True, right_index=True,
                                                                      how='left')

        # reverse signs for churned customers
        self.df_customer_summary.loc[:, 'total_churned'] = -self.df_customer_summary.loc[:, 'total_churned']

        # calculate ending active customers from raw revenue data
        ending_active_customers = pd.DataFrame(self.df_revenue_by_customer.astype(bool).sum(axis=0),
                                               columns=['ending_active_customers'])
        self.df_customer_summary = self.df_customer_summary.merge(ending_active_customers, left_index=True,
                                                                  right_index=True,
                                                                  how='left')

        # checksum comparing total of 5 SaaS delta and the actual customer count delta over periods
        total_saas_delta = self.df_customer_summary.iloc[:, :3].fillna(0).to_numpy().sum()
        customer_delta = ending_active_customers.diff(axis=0).fillna(0).to_numpy().sum()
        total_checksum_diff = total_saas_delta - customer_delta

        print(f'completed: customer delta summary\n   checksum diff = {total_checksum_diff:.2f}')

        return self.df_customer_summary
