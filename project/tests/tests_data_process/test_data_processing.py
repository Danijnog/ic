import csv
import unittest
from unittest.mock import Mock, call, patch

import pandas as pd

from connection import db_connection
from src.data_process import data_processing


class TestDataProcessFunctions(unittest.TestCase):
    @patch("connection.db_connection.create_engine")
    @patch("pandas.read_sql")  # Mock the pd.read_sql function to simulate
    def test_retrieved_db(self, mock_read_sql, mock_create_engine):
        """
        Test if the function 'retrieved_db' returns the expected DataFrame with the data from the database.
        """
        mock_df = pd.DataFrame(
            {
                "message_id": [1, 2, 3],
                "message": ["Mensagem de teste", "olá", None],
                "message_utc": [
                    "2023-01-06 10:00:00",
                    "2023-01-07 11:00:00",
                    "2023-01-10 12:00:00",
                ],
                "from_id": [9283, 123, 2849],
            }
        )
        mock_read_sql.return_value = mock_df

        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine

        conn = db_connection.connection()

        initial_date = "2023-01-01"
        end_date = "2023-01-15"

        group_id = 192841
        result_df = data_processing.retrieved_db(
            group_id, conn, initial_date, end_date
        )  # Since the 'pd.read_sql' function was mocked, this line returns the mock_df instead of accessing the database

        self.assertEqual(len(result_df), 2)
        self.assertEqual(result_df["message_id"][0], 1)
        self.assertNotIn(None, result_df["message"].values)
        self.assertIn("Mensagem de teste", result_df["message"].values)
        mock_read_sql.assert_called_once()

    @patch("src.data_process.data_processing.os.path.exists")
    @patch("src.data_process.data_processing.pd.DataFrame.to_csv")
    def test_separate_messages_in_days(self, mock_to_csv, mock_path_exists):
        """
        Test if the function 'separate_messages_in_days' separates the messages in days correctly.
        """
        mock_df = pd.DataFrame(
            {
                "message_id": [1, 2, 3],
                "message": ["Mensagem de teste", "olá", "Teste"],
                "message_utc": [
                    "2023-01-06 10:00:00",
                    "2023-01-06 11:00:00",
                    "2023-01-07 12:00:00",
                ],
                "from_id": [9283, 123, 2849],
            }
        )
        mock_path_exists.return_value = False

        group_id = 192841
        data_processing.separate_messages_in_days(mock_df, group_id)

        expected_calls = [
            call(
                f"data/msgPerGroup/ID_{group_id}/messages_2023-01-06.csv",
                header="True",
                index=False,
                quoting=csv.QUOTE_ALL,
            ),
            call(
                f"data/msgPerGroup/ID_{group_id}/messages_2023-01-07.csv",
                header="True",
                index=False,
                quoting=csv.QUOTE_ALL,
            ),
        ]

        mock_to_csv.assert_has_calls(expected_calls, any_order=False)

    @patch("src.data_process.data_processing.os.makedirs")
    @patch("src.data_process.data_processing.retrieved_db")
    def test_get_separated_messages(self, mock_retrieved_db, mock_makedirs):
        """
        Tests if the function 'get_separated_messages' separates messages correctly
        and creates the necessary directories for each group.
        """
        mock_retrieved_db.return_value = pd.DataFrame(
            {
                "message_id": [1, 2, 3],
                "message": ["Mensagem de teste", "olá", "Teste"],
                "message_utc": [
                    "2023-01-06 10:00:00",
                    "2023-01-06 11:00:00",
                    "2023-01-07 12:00:00",
                ],
                "from_id": [9283, 123, 2849],
            }
        )
        groups = pd.DataFrame({"channel_id": ["-12345", "-67890"], "quantidade_mensagens": [3, 3]})

        groups_ids = groups["channel_id"].values
        expected_calls = [
            call(f"data/msgPerGroup/ID_{groups_ids[0]}", exist_ok=True),
            call(f"data/msgPerGroup/ID_{groups_ids[1]}", exist_ok=True),
        ]

        data_processing.get_separated_messages(groups)
        mock_makedirs.assert_has_calls(expected_calls, any_order=False)
    
    def clean_messages(self):
        pass

    def clear_messages(self):
        pass

    
