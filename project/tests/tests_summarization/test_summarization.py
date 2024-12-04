import unittest
from unittest.mock import Mock, patch
import pandas as pd

from src.summarization import summarization

class TestSummariesFunctions(unittest.TestCase):

    def setUp(self):
        # Mocks comuns
        # Simulando a chamada a API e a resposta da API
        self.mock_api_client = Mock()
        self.mock_response = Mock()
        self.mock_response.choices = [Mock(message = Mock(content = "Resumo gerado"))]
        self.mock_api_client.chat.completions.create.return_value = self.mock_response
    
    def test_generate_summary(self):
        input_text = "Texto de teste para resumo."
        model = "test-model"

        summary = summarization.generate_summary(input_text, model, self.mock_api_client)
        self.assertEqual(summary, "Resumo gerado")
        self.mock_api_client.chat.completions.create.assert_called_once()

    @patch("os.listdir")
    @patch("pandas.read_csv")
    def test_group_summary(self, mock_read_csv, mock_listdir):
        group_id = 123
        text_encoding = "test-encoding"
        text_model = "test-model"
        max_tokens = 50
        min_number_of_messages = 25
        
        # Mocks para arquivos CSV
        mock_list = ["test1.csv", "test2.csv"]
        mock_listdir.return_value = mock_list
        
        # Configurar DataFrame para simular os CSVs com mensagens
        mock_df = pd.DataFrame({
            "message": ["Mensagem 1", "Mensagem 2", "Mensagem 3"]
        })
        mock_read_csv.return_value = mock_df
        
        # Chama a função e verifica se o retorno contém o resumo esperado
        group_summaries = summarization.group_summary(group_id, text_encoding, text_model, max_tokens, min_number_of_messages, self.mock_api_client)
        self.assertEqual(group_summaries, []) # Como a quantidade de mensagens < 25, a lista retornada de sumário gerado será vazia

    @patch("os.listdir")
    @patch("pandas.read_csv")
    def test_get_summaries_for_groups(self, mock_read_csv, mock_listdir):
        groups = pd.DataFrame({
            "channel_id": [123, 456]
        })
        text_encoding = "test-encoding"
        text_model = "test-model"
        max_tokens = 100
        min_number_of_messages = 25

        # Mock para arquivos csv
        mock_list = ["test1.csv", "test2.csv", "test3.csv"]
        mock_listdir.return_value = mock_list

        # Configurar DataFrame para simular os CSVs com mensagens
        mock_df = pd.DataFrame({
            "message": ["Mensagem 1", "Mensagem 2", "Mensagem 3"]
        })
        mock_read_csv.return_value = mock_df

        groups_summaries = summarization.get_summaries_for_groups(groups, text_encoding, text_model, max_tokens, min_number_of_messages, self.mock_api_client)
        self.assertEqual(groups_summaries,      
                         [{'ID': 123, 'Sumário': []},
                          {'ID': 456, 'Sumário': []}])  