import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from connection import db_connection


class TestDataBaseFunctions(unittest.TestCase):
    @patch("connection.db_connection.create_engine")  # Decorator to avoid a real database connection
    def test_success_connection(self, mock_create_engine):
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        conn = db_connection.connection()
        self.assertIsNotNone(conn)
        self.assertEqual(conn, mock_engine)
        mock_create_engine.assert_called_once()

    @patch("connection.db_connection.pd.read_sql")
    def test_get_groups(self, mock_read_sql):
        mock_df = pd.DataFrame(
            {
                "channel_id": [19283841, -123941, 1], 
                "quantidade_mensagens": [30928, 2, 0]
            }
        )
        mock_read_sql.return_value = mock_df

        initial_date = "2023-09-25"
        end_date = "2023-01-16"
        result_df = db_connection.get_groups(initial_date, end_date)

        self.assertEqual(len(result_df), 3)
        self.assertTrue((result_df["channel_id"][0] == [19283841]))
        mock_read_sql.assert_called_once()
