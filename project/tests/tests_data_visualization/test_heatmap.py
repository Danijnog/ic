import unittest

import pandas as pd

from src.data_visualization import heatmap


class TestHeatmap(unittest.TestCase):

    def test_generate_transitions_for_heatmap(self):
        """
        Test if the function returns correctly a list of lists that contains the transitions
        between clusters for each day that will be used for heatmap.
        """
        df = pd.DataFrame(
            {
                "ID": [1, 1, 2, 2, 3, 3, 3, 3, 3, 3],
                "cluster": [0, 1, 2, 1, 0, 2, 1, 2, 1, 2],
                "date": ["2022-09-25", "2022-09-26", "2022-09-27"] * 3 + ["2022-09-28"]
            }
        )
        unique_dates = df["date"].sort_values().unique()
        num_clusters = df["cluster"].nunique()

        heatmap_list = heatmap.get_transitions_list_for_heatmap(df)
        self.assertEqual(len(heatmap_list), num_clusters * num_clusters)
        self.assertEqual(len(heatmap_list[0]), len(unique_dates[1:]))


    def test_plot_heatmap(self):
        """
        Test if the function generates a heatmap correctly.
        """
        df = pd.DataFrame(
            {
                "ID": [1, 1, 2, 2, 3, 3, 3, 3, 3, 3],
                "cluster": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                "date": ["2022-09-25", "2022-09-26", "2022-09-27"] * 3 + ["2022-09-28"]
            }
        )
        unique_dates = df["date"].sort_values().unique()
        
        heatmap_list = heatmap.get_transitions_list_for_heatmap(df)
        self.assertIsNotNone(heatmap_list)

        heatmap_fig = heatmap.plot_heatmap(heatmap_list, df)
        heatmap_fig_coord_x = heatmap_fig.data[0]["x"]
        heatmap_fig_coord_y = heatmap_fig.data[0]["y"]

        # Check if the len of the x axis is equal to the number of unique dates minus the first date
        self.assertEqual(len(heatmap_fig_coord_x), len(unique_dates[1:]))

        # Check if the len of the y axis is equal to the number of transitions
        self.assertEqual(len(heatmap_fig_coord_y), len(heatmap_list))


    def test_empty_dataframe(self):
        """
        Test if the function handles an empty dataframe correctly.
        """
        df = pd.DataFrame(columns=["ID", "cluster", "date"])
        heatmap_list = heatmap.get_transitions_list_for_heatmap(df)
        self.assertEqual(heatmap_list, [])


    def test_single_date(self):
        """
        Test if the function handles a dataframe with a single date correctly.
        """
        df = pd.DataFrame(
            {
                "ID": [1, 2, 3],
                "cluster": [0, 1, 2],
                "date": ["2022-09-25"] * 3
            }
        )
        heatmap_list = heatmap.get_transitions_list_for_heatmap(df)
        num_clusters = df["cluster"].nunique()
        
        # The heatmap list should be a list of empty lists because there is only one date
        self.assertEqual(heatmap_list, [[] for _ in range(num_clusters ** 2)])