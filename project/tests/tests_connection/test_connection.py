import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from connection import db_connection


class TestDataBaseFunctions(unittest.TestCase):
    @patch("connection.db_connection.create_engine")  # Decorator to avoid a real database connection
    def test_success_connection(self, mock_create_engine):
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        con = db_connection.connection()
        self.assertIsNotNone(con)
        self.assertEqual(con, mock_engine)
        mock_create_engine.assert_called_once()

    @patch("connection.db_connection.pd.read_sql") # Mock the pd.read_sql function to simulate
    def test_retrieved_db(self, mock_read_sql):
        mock_df = pd.DataFrame(
            {
                "message_id": [1, 2, 3],
                "message": ["Mensagem de teste", "olá", None],
                "message_utc": ["2023-01-06", "2023-01-07", "2023-01-10"],
                "from_id": [9283, 123, 2849],
            }
        )
        mock_read_sql.return_value = mock_df

        group_id = 192841
        result_df = db_connection.retrieved_db(
            group_id
        )  # Since the 'pd.read_sql' function was mocked, this line returns the mock_df instead of accessing the database

        self.assertEqual(len(result_df), 2)
        self.assertEqual(result_df["message_id"][0], 1)
        self.assertNotIn(None, result_df["message"].values)
        self.assertIn("Mensagem de teste", result_df["message"].values)
        mock_read_sql.assert_called_once()

    @patch("connection.db_connection.pd.read_sql")
    def test_get_groups(self, mock_read_sql):
        mock_df = pd.DataFrame(
            {
                "channel_id": [19283841, -123941, 1], 
                "quantidade_mensagens": [30928, 2, 0]
            }
        )
        mock_read_sql.return_value = mock_df

        result_df = db_connection.get_groups()

        self.assertEqual(len(result_df), 3)
        self.assertTrue((result_df["channel_id"][0] == [19283841]))
        mock_read_sql.assert_called_once()
