import unittest
from unittest.mock import patch
import pandas as pd

from embedding import embedding_trajectory

class TestGroupTrajectories(unittest.TestCase):

    def test_group_trajectorie(self):
        df = pd.DataFrame({
            'dim1': [1, 2, 3, 4, 5],
            'dim2': [1, 2, 3, 4, 5],
            'dim3': [1, 2, 3, 4, 5],
            'dim4': [1, 2, 3, 4, 5],
            'dim5': [1, 2, 3, 4, 5],
            'dim6': [1, 2, 3, 4, 5],
            'dim7': [1, 2, 3, 4, 5],
            'dim8': [1, 2, 3, 4, 5],
            'dim9': [1, 2, 3, 4, 5],
            'dim10': [1, 2, 3, 4, 5],
            'label': ['um texto aqui', 'a conversa do Telegram', 'c', 'd', 'e'],
            'ID': [1, 1, 1, 4, 5],
            'date': ['2023-01-06', '2023-01-07', '2023-01-07', '2023-01-07', '2023-01-07']
        })

        group_trajectory = embedding_trajectory.get_group_trajectory(1, df)
        value_trajectory = group_trajectory[0]

        # Ao fazermos a conta definida na função para calcular a trajetória do grupo 1,
        # chegamos no valor de raiz quadrada de 10, que é 3.1622 aproximadamente.
        decimalPlace = 3
        self.assertAlmostEqual(value_trajectory, 3.1622, places = decimalPlace)



