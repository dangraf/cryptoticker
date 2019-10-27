from unittest import TestCase
import pandas as pd
from ticker.datahelpers import get_new_unique_data




def test_duplicate_data_with_none():
    df = pd.DataFrame({'A':[1,2],'B':[2,3]})
    df_res = get_new_unique_data(old_df=None, new_df= df)
    assert len(df_res) == len(df)

def test_duplicate_data_both_same():
    df = pd.DataFrame({'A': [1, 2], 'B': [2, 3]})
    df_res = get_new_unique_data(old_df=df, new_df=df)
    assert len(df_res) == 0

def test_duplicate_data_some_different():
    dfA = pd.DataFrame({'A': [1, 2], 'B': [2, 3]})
    dfB = pd.DataFrame({'A': [1, 2], 'B': [2, 4]})
    df_res = get_new_unique_data(old_df=dfA, new_df=dfB)
    assert len(df_res) == 1
    assert df_res.iloc[0]['B'] == 4

def test_duplicate_data_series_difference():
    dfA = pd.DataFrame({'A': [1, 2], 'B': [2, 3]})
    dfB = pd.DataFrame({'A': [1, 2], 'B': [2, 4]})
    dfC = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})

    df_res = get_new_unique_data(old_df=dfA, new_df=dfB)
    assert df_res.iloc[0]['B'] == 4

    df_res = get_new_unique_data(old_df=dfB, new_df=dfC)
    assert df_res.iloc[0]['B'] == 3

