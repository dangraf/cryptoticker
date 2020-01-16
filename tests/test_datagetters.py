import pytest
from unittest.mock import patch
from ticker.data_getters import *
from ticker.mongo_func import *
from ticker.mongo_doc import *
from time import sleep



@patch('ticker.data_getters.save_tickerdata2')
def test_coinmarketcap(mock_save_tickerdata):
    # test
    get_coinmarketcap()
    # verify
    assert mock_save_tickerdata.called
    colname = mock_save_tickerdata.call_args[1]['collection_name']
    data = mock_save_tickerdata.call_args[1]['data']
    assert colname == 'coinmarketcap_top100'
    assert len(data) == 100

@patch('ticker.data_getters.save_tickerdata2')
def test_globalcap(mock_save_tickerdata):
    # test
    get_global_cap()
    # verify
    assert mock_save_tickerdata.called
    colname = mock_save_tickerdata.call_args[1]['collection_name']
    data = mock_save_tickerdata.call_args[1]['data']
    assert colname == 'global_market'
    assert len(data) == 7

@patch('ticker.data_getters.save_tickerdata2')
def test_bitcoin_fees( mock_save_tickerdata):
    get_bitcoin_fees()
    assert mock_save_tickerdata.called
    colname = mock_save_tickerdata.call_args[1]['collection_name']
    data = mock_save_tickerdata.call_args[1]['data']
    assert colname == 'bitcoin_fees'
    assert len(data) == 3

@patch('ticker.data_getters.save_tickerdata2')
def atest_bitcoinaverage_ticker(mock_save_tickerdata):
    #get_bitcoinaverage_ticker_data()
    assert mock_save_tickerdata.called
    colname = mock_save_tickerdata.call_args[1]['collection_name']
    data = mock_save_tickerdata.call_args[1]['data']
    assert colname == 'bitcoinaverage_ticker'
    assert len(data) == 12

@patch('ticker.data_getters.save_tickerdata2')
def test_bitcoincharts(mock_save_tickerdata):
    get_bitcoincharts_data()
    assert mock_save_tickerdata.called
    colname = mock_save_tickerdata.call_args[1]['collection_name']
    data = mock_save_tickerdata.call_args[1]['data']
    assert colname == 'bitcoincharts_global'
    assert len(data)> 30

@patch('ticker.data_getters.save_tickerdata2')
def test_fear_and_greed_index(mock_save_tickerdata):
    get_fear_greed_index()
    assert mock_save_tickerdata.called
    colname = mock_save_tickerdata.call_args[1]['collection_name']
    data = mock_save_tickerdata.call_args[1]['data']
    assert colname == 'fear_and_greed_index'
    assert type(data) is dict
    assert type(data['fear_greed_idx']) is int

@patch('ticker.data_getters.save_tickerdata2')
def test_get_kraken_orderdepth(mock_save_tickerdata):
    for i in range(7):
        get_kraken_orderdepth()
        assert mock_save_tickerdata.called
        colname = mock_save_tickerdata.call_args[1]['collection_name']
        data = mock_save_tickerdata.call_args[1]['data']
        assert colname == 'kraken_orderdepth'
        assert type(data) is dict
        sleep(1.0)

    assert i > 5

@patch('ticker.data_getters.save_tickerdata2')
@patch('ticker.data_getters.get_settingslist')
def test_get_news_data(m_get_settings, m_save_ticker ):
    urllist = SettingsList()
    urllist.list = ["https://coingeek.com"]
    keylist = SettingsList()
    keylist.list = ["bitcoin", "ripple", 'crypto']

    m_get_settings.side_effect= [urllist,keylist ]


    init_mongodb()
    get_news_data()

@patch('ticker.data_getters.save_tickerdata2')
def test_get_kraken_ticker(mock_save_tickerdata):
    get_kraken_trades()
    assert mock_save_tickerdata.called
    colname = mock_save_tickerdata.call_args[1]['collection_name']
    data = mock_save_tickerdata.call_args[1]['data']
    assert colname == 'kraken_trades_ADA/USD'
    assert type(data) is list
