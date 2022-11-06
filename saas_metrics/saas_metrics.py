import numpy as np
import pandas as pd


class SaaSMetrics:
    def __init__(self, df_revenue: pd.DataFrame):
        # store revenue DataFrame
        self.df_revenue = df_revenue

        # TODO understand what need to be initialized
        # initialize 5 internal DataFrames
        self.df_churned = pd.DataFrame()
        self.df_contraction = pd.DataFrame()
        self.df_resurrected = pd.DataFrame()
        self.df_expansion = pd.DataFrame()
        self.df_new = pd.DataFrame()

    def calculate_five_saas_delta(self):
        """
        Calculate the 5 SaaS deltas and return a tuple of 5 DataFrames:
            results[0]: churned
            results[1]: contraction
            results[2]: resurrected
            results[3]: expansion
            results[4]: new
        """

        # calculate analysis helpers
        df_analysis_helper = pd.DataFrame(index=self.df_revenue.index)
        df_analysis_helper['first_time_as_customer'] = self.df_revenue.ne(0).idxmax(axis='columns')
        df_analysis_helper['n_first_time_as_customer'] = self.df_revenue.columns.get_indexer(
            df_analysis_helper['first_time_as_customer'])

        n_time_periods = len(self.df_revenue.columns)

        # calculate churned revenue
        self.df_churned = pd.DataFrame(index=self.df_revenue.index)
        for i in range(n_time_periods - 1):
            i = i + 1  # align i with current period (second period)
            condition = (
                    (self.df_revenue.iloc[:, i - 1] > 0) &
                    (self.df_revenue.iloc[:, i] == 0)
            )
            new_column = pd.DataFrame(np.where(
                condition,
                -self.df_revenue.iloc[:, i - 1],
                0
            ))
            self.df_churned = pd.concat([self.df_churned, new_column], axis='columns')
        self.df_churned.set_axis(self.df_revenue.columns[1:].to_list(), axis='columns', inplace=True)

        # calculate contraction revenue
        self.df_contraction = pd.DataFrame(index=self.df_revenue.index)
        for i in range(n_time_periods - 1):
            i = i + 1  # align i with current period (second period)
            condition = (
                    (self.df_revenue.iloc[:, i - 1] > 0) &
                    (self.df_revenue.iloc[:, i] > 0) &
                    (self.df_revenue.iloc[:, i] < self.df_revenue.iloc[:, i - 1])
            )
            new_column = pd.DataFrame(np.where(
                condition,
                self.df_revenue.iloc[:, i] - self.df_revenue.iloc[:, i - 1],
                0
            ))
            self.df_contraction = pd.concat([self.df_contraction, new_column], axis='columns')
        self.df_contraction.set_axis(self.df_revenue.columns[1:].to_list(), axis='columns', inplace=True)

        # calculate resurrected revenue
        # TODO debug 2 resurrected in 2018
        self.df_resurrected = pd.DataFrame(index=self.df_revenue.index)
        for i in range(n_time_periods - 1):
            i = i + 1  # align i with current period (second period)
            condition = (
                    (self.df_revenue.iloc[:, i - 1] == 0) &
                    (self.df_revenue.iloc[:, i] > 0) &
                    (i > df_analysis_helper.loc[:, 'n_first_time_as_customer'])
            )
            new_column = pd.DataFrame(np.where(
                condition,
                self.df_revenue.iloc[:, i],
                0
            ))
            self.df_resurrected = pd.concat([self.df_resurrected, new_column], axis='columns')
        self.df_resurrected.set_axis(self.df_revenue.columns[1:].to_list(), axis='columns', inplace=True)

        # calculate expansion revenue
        self.df_expansion = pd.DataFrame(index=self.df_revenue.index)
        for i in range(n_time_periods - 1):
            i = i + 1  # align i with current period (second period)
            condition = (
                    (self.df_revenue.iloc[:, i - 1] > 0) &
                    (self.df_revenue.iloc[:, i] > self.df_revenue.iloc[:, i - 1])
            )
            new_column = pd.DataFrame(np.where(
                condition,
                self.df_revenue.iloc[:, i] - self.df_revenue.iloc[:, i - 1],
                0
            ))
            self.df_expansion = pd.concat([self.df_expansion, new_column], axis='columns')
        self.df_expansion.set_axis(self.df_revenue.columns[1:].to_list(), axis='columns', inplace=True)

        # calculate new revenue
        self.df_new = pd.DataFrame(index=self.df_revenue.index)
        for i in range(n_time_periods - 1):
            i = i + 1  # align i with current period (second period)
            condition = (
                    (self.df_revenue.iloc[:, i - 1] == 0) &
                    (self.df_revenue.iloc[:, i] > 0) &
                    (i == df_analysis_helper.loc[:, 'n_first_time_as_customer'])
            )
            new_column = pd.DataFrame(np.where(
                condition,
                self.df_revenue.iloc[:, i],
                0
            ))
            self.df_new = pd.concat([self.df_new, new_column], axis='columns')
        self.df_new.set_axis(self.df_revenue.columns[1:].to_list(), axis='columns', inplace=True)

        return 0

    def arr_delta_summary(self):
        """
        Generate $ of ARR summary table from SaaS delta DataFrames
        """
        column_names = [
            'total_churned',
            'total_contraction',
            'total_resurrected',
            'total_expansion',
            'total_new'
        ]

        df_arr_summary = pd.DataFrame(index=self.df_revenue.columns.tolist())
        for i, df in enumerate([self.df_churned,
                                self.df_contraction,
                                self.df_resurrected,
                                self.df_expansion,
                                self.df_new
                                ]):
            saas_delta_sum = pd.DataFrame(df.sum(axis=0), columns=[column_names[i]])
            df_arr_summary = df_arr_summary.merge(saas_delta_sum, left_index=True, right_index=True, how='left')

        # TODO sum all changes and checksum against delta ARR

        ending_arr = pd.DataFrame(self.df_revenue.sum(axis=0), columns=['ending_arr'])
        df_arr_summary = df_arr_summary.merge(ending_arr, left_index=True, right_index=True, how='left')

        return df_arr_summary

    def customer_delta_summary(self):
        """
        Generate # of customer summary table from SaaS delta DataFrames
        """
        column_names = [
            'total_churned',
            'total_resurrected',
            'total_new'
        ]

        df_customer_summary = pd.DataFrame(index=self.df_revenue.columns.tolist())
        for i, df in enumerate([self.df_churned,
                                self.df_resurrected,
                                self.df_new
                                ]):
            saas_delta_sum = pd.DataFrame(df.astype(bool).sum(axis=0), columns=[column_names[i]])
            df_customer_summary = df_customer_summary.merge(saas_delta_sum, left_index=True, right_index=True,
                                                            how='left')

        # reverse signs for churned customers
        df_customer_summary.loc[:, 'total_churned'] = -df_customer_summary.loc[:, 'total_churned']

        # TODO sum all changes and checksum against delta customers

        ending_active_customers = pd.DataFrame(self.df_revenue.astype(bool).sum(axis=0),
                                               columns=['ending_active_customers'])
        df_customer_summary = df_customer_summary.merge(ending_active_customers, left_index=True, right_index=True,
                                                        how='left')
        return df_customer_summary
