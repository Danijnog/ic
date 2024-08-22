import unittest
from unittest.mock import patch
import pandas as pd
import numpy as np

from data_visualization import distribution

MIN_NUMBER_OF_MESSAGES = 100

class TestDistributionFunctions(unittest.TestCase):

    @patch('data_visualization.distribution.pd.read_csv') # Primeiro decorador é aplicado por ultimo
    @patch('data_visualization.distribution.os.listdir') # O último decorador é aplicado primeiro
    def test_get_dfs_for_distribution(self, mock_listdir, mock_read_csv):
        mock_listdir.return_value = ['messages_2023-01-08.csv']

        mock_df = pd.DataFrame({
            'message_id': [11234, 3, 1235],
            'message': ['olá', 'uma mensagem aqui', 'testando'],
            'message_utc': ['2023-01-02 06:07:31', '2023-01-02 09:49:40', '2023-01-02 16:53:39'],
            'from_id': [147705440, 3, 3],
            'date': ['2023-01-06', '2023-01-07', '2023-01-07'],
            'time': ['05:56:42', '11:08:18', '16:53:51']
        })
        mock_read_csv.return_value = mock_df

        groups = pd.DataFrame({
            'channel_id': [125284814, 984214814],
            'quantidade_mensagens': [3, 3]
        })
        df_cdf_messages_active_users, df_cdf_days = distribution.get_dfs_for_distribution_function(groups, MIN_NUMBER_OF_MESSAGES)

        self.assertEqual(len(df_cdf_messages_active_users), 2)
        self.assertTrue(df_cdf_messages_active_users['quantidade_mensagens'][0] == 3)
        self.assertTrue(df_cdf_messages_active_users['active_users'][0] == 2) # Usuários ativos é a quantidade de mensagens de 'from_id' diferente
        mock_listdir.assert_called() # Verificar se o método os.listdir foi chamado pelo menos uma vez na função
        mock_read_csv.assert_called() # Verificar se o método pd.read_csv foi chamado pelo menos uma vez na função

        self.assertEqual(len(df_cdf_days), 2)
        self.assertTrue(df_cdf_days['num_dias_grupo_com_mensagem'][0] == 0)
    
    
    def test_cumulative_distribution_function(self):
        df_cdf_messages_active_users = pd.DataFrame({
            'ID': [1, 2, 3, 4, 5, 6, 7, 8],
            'quantidade_mensagens': [1, 1, 2, 2, 8, 90, 5, 67],
            'date': ['2023-01-06', '2023-01-09', '2023-01-07', '2023-01-09', '2023-01-09', '2023-01-09', '2023-01-03', '2023-01-02',],
            'active_users': [12, 12, 12, 5, 5, 4, 32, 28]
        })

        df_cdf_days = pd.DataFrame({
            'ID': [1, 2, 3],
            'num_dias_grupo_com_mensagem': [10, 2, 2]
        })

        messages_fig, active_users_fig, days_distribution_fig = distribution.cumulative_distribution_function(df_cdf_messages_active_users, df_cdf_days, MIN_NUMBER_OF_MESSAGES)
        self.assertEqual(len(df_cdf_messages_active_users), 8)

        # Figura 1 referente ao CDF de mensagens
        fig_1_coord_x_values = messages_fig.data[0]['x'] # Quantidade de mensagens
        fig_1_cumulative_distribution = messages_fig.data[0]['y'] # Distribuição acumulada de mensagens
        self.assertEqual(list(fig_1_coord_x_values), [1, 1, 2, 2, 5, 8, 67, 90])

        df = pd.DataFrame({
            'quantidade_mensagens': fig_1_coord_x_values,
            'cdf': fig_1_cumulative_distribution
        })
        
        self.assertEqual(df['quantidade_mensagens'][3], 2)
        self.assertEqual(df['cdf'][3], 0.5)

        self.assertEqual(fig_1_cumulative_distribution[0], 0.125)
        self.assertEqual(fig_1_cumulative_distribution[7], 1)
        
        # Figura 2 referente ao CDF de usuários ativos
        fig_2_coord_x_values = active_users_fig.data[0]['x'] # Quantidade de usuários ativos
        fig_2_cumulative_distribution = active_users_fig.data[0]['y'] # Distribuição acumulada de usuários ativos
        self.assertEqual(list(fig_2_coord_x_values), [4, 5, 5, 12, 12, 12, 28, 32])

        dff = pd.DataFrame({
            'active_users': fig_2_coord_x_values,
            'cdf': fig_2_cumulative_distribution
        })

        self.assertEqual(dff['active_users'][3], 12)
        self.assertEqual(dff['cdf'][3], 0.5)
        
        self.assertEqual(fig_2_cumulative_distribution[0], 0.125)
        self.assertEqual(fig_2_cumulative_distribution[7], 1)

        # Figura 3 referente ao CDF da quantidade de dias com mensagem considerando o limiar de 'min_number_of_messages'
        fig_3_coord_x_values = days_distribution_fig.data[0]['x'] # Quantidade de dias com mensagens considerando o limiar de 'min_number_of_messages'
        fig_3_cumulative_distribution = days_distribution_fig.data[0]['y'] #  Distribuição acumulada de usuários ativos
        self.assertEqual(list(fig_3_coord_x_values), [2, 2, 10])

        dfff = pd.DataFrame({
            'num_dias_grupo_com_mensagem': fig_3_coord_x_values,
            'cdf': fig_3_cumulative_distribution
        })

        self.assertEqual(dfff['num_dias_grupo_com_mensagem'][2], 10)
        self.assertEqual(dfff['cdf'][2], 1)