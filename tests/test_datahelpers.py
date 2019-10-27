from unittest import TestCase
import pandas as pd
from ticker.datahelpers import get_new_unique_data


class TestDataHelpers(TestCase):

    def test_duplicate_data_with_none(self):
        df = pd.DataFrame({'A':[1,2],'B':[2,3]})
        df_res = get_new_unique_data(old_df=None, new_df= df)
        self.assertEqual(len(df_res), len(df))

    def test_duplicate_data_both_same(self):
        df = pd.DataFrame({'A': [1, 2], 'B': [2, 3]})
        df_res = get_new_unique_data(old_df=df, new_df=df)
        self.assertEqual(len(df_res), 0)

    def test_duplicate_data_some_different(self):
        dfA = pd.DataFrame({'A': [1, 2], 'B': [2, 3]})
        dfB = pd.DataFrame({'A': [1, 2], 'B': [2, 4]})
        df_res = get_new_unique_data(old_df=dfA, new_df=dfB)
        self.assertEqual(len(df_res), 1)
        self.assertEqual(df_res.iloc[0]['B'], 4)

    def test_duplicate_data_series_difference(self):
        dfA = pd.DataFrame({'A': [1, 2], 'B': [2, 3]})
        dfB = pd.DataFrame({'A': [1, 2], 'B': [2, 4]})
        dfC = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})

        df_res = get_new_unique_data(old_df=dfA, new_df=dfB)
        self.assertEqual(df_res.iloc[0]['B'], 4)

        df_res = get_new_unique_data(old_df=dfB, new_df=dfC)
        self.assertEqual(df_res.iloc[0]['B'], 3)

