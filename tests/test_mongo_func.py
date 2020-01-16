from ticker.mongo_func import *
from ticker.mongo_doc import *
from pymongo import MongoClient

init_mongodb()

def test_save_ticker_data():
    # verify no objects in database

    collection_name = 'unittest'
    client = MongoClient('userver2', 27017)
    a = client['ticker_db'][collection_name].find_one()
    assert a is None

    data = {'apa':1, 'bepa':'hej'}
    save_tickerdata(data=data, collection_name=collection_name)

    a = client['ticker_db'][collection_name].find_one()
    assert a is not None
    assert a['data']['apa'] == 1
    assert a['data']['bepa'] == 'hej'
    # cleanup
    client['ticker_db'][collection_name].delete_many({})
    a = client['ticker_db'][collection_name].find_one()
    assert a is None
