import unittest
from unittest.mock import patch

import pandas as pd

from src.data_visualization import distribution

MIN_NUMBER_OF_MESSAGES = 100


class TestDistributionFunctions(unittest.TestCase):
    @patch("pandas.read_csv")  # First decorator is applied last
    @patch("os.listdir")  # The last decorator is applied first
    def test_get_dfs_for_distribution(self, mock_listdir, mock_read_csv):
        mock_listdir.return_value = ["messages_2023-01-08.csv"]

        mock_df = pd.DataFrame(
            {
                "message_id": [11234, 3, 1235],
                "message": ["olá", "uma mensagem aqui", "testando"],
                "message_utc": [
                    "2023-01-02 06:07:31",
                    "2023-01-02 09:49:40",
                    "2023-01-02 16:53:39",
                ],
                "from_id": [147705440, 3, 3],
                "date": ["2023-01-06", "2023-01-07", "2023-01-07"],
                "time": ["05:56:42", "11:08:18", "16:53:51"],
            }
        )
        mock_read_csv.return_value = mock_df

        groups = pd.DataFrame(
            {"channel_id": [125284814, 984214814], "quantidade_mensagens": [3, 3]}
        )
        df_cdf_messages_active_users, df_cdf_days = distribution.get_dfs_for_distribution_function(
            groups, MIN_NUMBER_OF_MESSAGES
        )

        self.assertEqual(len(df_cdf_messages_active_users), 2)
        self.assertTrue(df_cdf_messages_active_users["num_messages"][0] == 3)
        self.assertTrue(df_cdf_messages_active_users["active_users"][0] == 2)

        # Check if methods 'os.listdir' and 'pd.read_csv' was called at least once at the function
        mock_listdir.assert_called()
        mock_read_csv.assert_called()

        self.assertEqual(len(df_cdf_days), 2)
        self.assertTrue(df_cdf_days["num_days_groups_with_messages"][0] == 0)

    def test_cumulative_distribution_function(self):
        df_cdf_messages_active_users = pd.DataFrame(
            {
                "ID": [1, 2, 3, 4, 5, 6, 7, 8],
                "num_messages": [1, 1, 2, 2, 8, 90, 5, 67],
                "date": [
                    "2023-01-06",
                    "2023-01-09",
                    "2023-01-07",
                    "2023-01-09",
                    "2023-01-09",
                    "2023-01-09",
                    "2023-01-03",
                    "2023-01-02",
                ],
                "active_users": [12, 12, 12, 5, 5, 4, 32, 28],
            }
        )

        df_cdf_days = pd.DataFrame({"ID": [1, 2, 3], "num_days_groups_with_messages": [10, 2, 2]})

        messages_fig, active_users_fig, days_distribution_fig = (
            distribution.cumulative_distribution_function(
                df_cdf_messages_active_users, df_cdf_days, MIN_NUMBER_OF_MESSAGES
            )
        )
        self.assertEqual(len(df_cdf_messages_active_users), 8)

        # Figure 1 is related to the CDF of messages
        fig_1_coord_x_values = messages_fig.data[0]["x"]  # Messages amount
        fig_1_cumulative_distribution = messages_fig.data[0]["y"]  # Cumulative distribution of messages
        self.assertEqual(list(fig_1_coord_x_values), [1, 1, 2, 2, 5, 8, 67, 90])

        df = pd.DataFrame(
            {
                "num_messages": fig_1_coord_x_values, 
                "cdf": fig_1_cumulative_distribution
            }
        )

        self.assertEqual(df["num_messages"][3], 2)
        self.assertEqual(df["cdf"][3], 0.5)

        self.assertEqual(fig_1_cumulative_distribution[0], 0.125)
        self.assertEqual(fig_1_cumulative_distribution[7], 1)

        # Second figure is related to the CDF of active users
        fig_2_coord_x_values = active_users_fig.data[0]["x"]  # Active users amount
        fig_2_cumulative_distribution = active_users_fig.data[0]["y"]  # Cumulative distribution of active users
        self.assertEqual(list(fig_2_coord_x_values), [4, 5, 5, 12, 12, 12, 28, 32])

        dff = pd.DataFrame(
            {
                "active_users": fig_2_coord_x_values, 
                "cdf": fig_2_cumulative_distribution
            }
        )

        self.assertEqual(dff["active_users"][3], 12)
        self.assertEqual(dff["cdf"][3], 0.5)

        self.assertEqual(fig_2_cumulative_distribution[0], 0.125)
        self.assertEqual(fig_2_cumulative_distribution[7], 1)

        # Third figure is related to the CDF of amount of days with messages considering the
        # threshold of 'min_number_of_messages'.
        fig_3_coord_x_values = days_distribution_fig.data[0]["x"]  # Days with messages amount, considering the threshold
        fig_3_cumulative_distribution = days_distribution_fig.data[0]["y"]  # Cumulative distribution of days with messages
        self.assertEqual(list(fig_3_coord_x_values), [2, 2, 10])

        dfff = pd.DataFrame(
            {
                "num_days_groups_with_messages": fig_3_coord_x_values,
                "cdf": fig_3_cumulative_distribution,
            }
        )

        self.assertEqual(dfff["num_days_groups_with_messages"][2], 10)
        self.assertEqual(dfff["cdf"][2], 1)
