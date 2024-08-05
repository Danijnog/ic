import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

from data import db_connection

class testDataBaseFunctions(unittest.TestCase):

    @patch('data.db_connection.create_engine') # Decorador para evitar uma conexão real com o banco de dados
    def test_success_connection(self, mock_create_engine):
        # Mock the create_engine function to simulate a successful connection
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        con = db_connection.connection()
        self.assertIsNotNone(con)
        self.assertEqual(con, mock_engine)
        mock_create_engine.assert_called_once()
    
    @patch('data.db_connection.pd.read_sql')
    def test_retrieved_db(self, mock_read_sql):
        # Mock the pd.read_sql function to simulate
        mock_df = pd.DataFrame({
            'message_id': [1, 2, 3],
            'message': ['Mensagem de teste', 'olá', None],
            'message_utc': ['2023-01-06', '2023-01-07', '2023-01-10'],
            'from_id': [9283, 123, 2849]
            })
        mock_read_sql.return_value = mock_df

        group_id = 192841
        result_df = db_connection.retrieved_db(group_id) # Como a função 'pd.read_sql' foi mockada, essa linha retorna o mock_df em vez de acessar o banco de dados

        self.assertEqual(len(result_df), 2)
        self.assertNotIn(None, result_df['message'].values)
        self.assertIn('Mensagem de teste', result_df['message'].values)
        mock_read_sql.assert_called_once()
    
    @patch('data.db_connection.pd.read_sql')
    def test_get_groups(self, mock_read_sql):
        mock_df = pd.DataFrame({
            'channel_id': [19283841, -123941, 1],
            'quantidade_mensagens': [30928, 2, 0]
        })
        mock_read_sql.return_value = mock_df

        result_df = db_connection.get_groups()

        self.assertEqual(len(result_df), 3)
        self.assertTrue((result_df['channel_id'][0] == [19283841]))
        mock_read_sql.assert_called_once()

if __name__ == '__main__':
    unittest.main()