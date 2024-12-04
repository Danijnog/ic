import unittest
from unittest.mock import patch
import pandas as pd

from src.data_visualization import embedding_plot

MIN_NUMBER_OF_MESSAGES = 5

class TestRemovePointsFromEmbedding(unittest.TestCase):

    @patch("os.listdir")
    @patch("pandas.read_csv")
    def test_get_df_for_remove_days_groups_that_has_less_25_messages(self, mock_read_csv, mock_listdir):
        """
        Testa se a função 'get_df_for_remove_days_groups_that_has_less_25_messages' retorna corretamente um
        DataFrame que contém os dias-grupo que possuem uma quantidade de mensagens menor que 25 após fazermos
        a limpeza das mensagens em um dia.
        """
        groups = pd.DataFrame({
            "channel_id": ["-1000000000"],
            "quantidade_mensagens": [10]
        })

        mock_df = pd.DataFrame({
            "message_id": list(range(1, 11)),
            "message": ["Interessante"] * 10, # Palavras repetidas em uma mensagem, serão limpas de acordo com a função de limpeza que é chamada dentro da função que está sendo testada
            "message_utc": ["2022-09-25 11:30:50"] * 10,
            "from_id": [1234] * 10,
            "date": ["2022-09-25"] * 10,
            "time": ["11:30:50"] * 10
        })
        mock_read_csv.return_value = mock_df

        mock_list = ["messages_2022-09-25", "messages_2022-09-26", "messages_2022-09-27"]
        mock_listdir.return_value = mock_list

        df = embedding_plot.get_df_for_remove_days_groups_that_has_less_25_messages(groups, MIN_NUMBER_OF_MESSAGES)
        self.assertEqual(len(df), 3) # Os 3 dias do grupo definido, após a limpeza, irão ser retornados no DataFrame, fazendo o DataFrame ficar com tamanho 3
        mock_read_csv.assert_called()
        mock_listdir.assert_called_once()
    
    @patch("os.listdir")
    @patch("pandas.read_csv")
    def test_remove_days_groups_that_has_less_25_messages(self, mock_read_csv, mock_listdir):
        """
        Testa se a função 'remove_days_groups_that_has_less_25_messages' remove corretamente os dias-grupo que
        estão no Embedding porém possuem uma quantidade de mensagens < 25 no dia.
        """
        groups = pd.DataFrame({
            "channel_id": ["-1000000000", "-1002070304"],
            "quantidade_mensagens": [10, 20]
        })

        mock_df = pd.DataFrame({
            "message_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "message": ["Interessante"] * 10, # Palavras repetidas em uma mensagem, serão limpas de acordo com a função de limpeza que é chamada dentro da função que está sendo testada
            "message_utc": ["2022-09-25 11:30:50"] * 10,
            "from_id": [1234] * 10,
            "date": ["2022-09-25"] * 10,
            "time": ["11:30:50"] * 10
        })
        mock_read_csv.return_value = mock_df

        mock_list = ["messages_2022-09-25", "messages_2022-09-26", "messages_2022-09-27"]
        mock_listdir.return_value = mock_list

        df = pd.DataFrame({
            "x": [13.519, 2.519],
            "y": [-12.787, -6.787],
            "label": ["Os participantes da conversa discutem sobre", "Discussão sobre política"],
            "ID": ["-1001034598292", "-1000000000"],
            "date": ["2022-09-26", "2022-09-25"],
            "cluster": [4, 3]
        })

        filtered_df = embedding_plot.remove_days_groups_that_has_less_25_messages(df, groups, MIN_NUMBER_OF_MESSAGES)
        self.assertEqual(len(filtered_df), 1) # A linha com o grupo de ID -1000000000 é removida, então ficamos com tamanho 1 no DataFrame
        mock_read_csv.assert_called()
        mock_listdir.assert_called()

    def test_remove_days_groups(self):
        """
        Testa se a função 'remove_days_groups' filtra corretamente os dias-grupo informados e remove as linhas do DataFrame que os contém. 
        """
        df = pd.DataFrame({
            "x": [-13.05, -2.05, -5.02],
            "y": [10.2, 5, 1.0],
            "label": ["As mensagens refletem forte polarização e intensa discussão política", "Sumário de teste", "Outro sumário de teste"],
            "ID": ["-123", "-100", "-5"],
            "date": ["2023-01-01", "2022-02-10", "2022-12-20"],
            "cluster": [1, 2, 0],

        })

        group_list = ["-123", "-1234", "-5"]
        day_list = ["2023-01-01", "2022-12-20", "2022-12-20"]
        df_with_day_group_removed = embedding_plot.remove_days_groups(df, group_list, day_list)
        self.assertEqual(len(df_with_day_group_removed), 1) # Irá remover o primeiro e o ultimo dia-grupo de df, ficando com o tamanho 1
    
    def test_remove_cluster(self):
        """
        Testa se a função 'remove_cluster' filtra corretamente os clusters informados e remove as linhas do DataFrame que os contém.
        """
        df = pd.DataFrame({
            "x": [-13.05, -2.05, -5.02],
            "y": [10.2, 5, 1.0],
            "label": ["As mensagens refletem forte polarização e intensa discussão política", "Sumário de teste", "Outro sumário de teste"],
            "ID": ["-123", "-100", "-5"],
            "date": ["2023-01-01", "2022-02-10", "2022-12-20"],
            "cluster": [1, 2, 0],

        })

        cluster_list = [5, 3]
        df_with_clusters_removed = embedding_plot.remove_cluster(df, cluster_list)
        self.assertEqual(len(df_with_clusters_removed), len(df), "Nenhum cluster deveria ser removido.")

    def test_remove_groups(self):
        """
        Testa se a função 'remove_groups' filtra corretamente os grupos informados e remove as linhas do DataFrame que os contém.
        """
        df = pd.DataFrame({
            "x": [-13.05, -2.05, -5.02],
            "y": [10.2, 5, 1.0],
            "label": ["As mensagens refletem forte polarização e intensa discussão política", "Sumário de teste", "Outro sumário de teste"],
            "ID": ["-123", "-100", "-5"],
            "date": ["2023-01-01", "2022-02-10", "2022-12-20"],
            "cluster": [1, 2, 0],

        })

        group_list = ["-5"]
        df_with_clusters_removed = embedding_plot.remove_groups(df, group_list)
        self.assertEqual(len(df_with_clusters_removed), 2)