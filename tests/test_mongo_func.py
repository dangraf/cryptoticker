from ticker.mongo_func import *
from ticker.mongo_doc import *
from pymongo import MongoClient

init_mongodb()

def test_save_ticker_data():
    # verify no objects in database

    collection_name = 'unittest'
    db = 'ticker2_db'
    client = MongoClient('userver2', 27017)
    a = client[db][collection_name].find_one()
    if a is not None:
        client[db][collection_name].delete_many({})
        a = client[db][collection_name].find_one()
    assert a is None

    data = {'apa':1, 'bepa':'hej'}
    save_tickerdata2(data=data, collection_name=collection_name)

    a = client[db][collection_name].find_one()
    assert a is not None
    assert a['data']['apa'] == 1
    assert a['data']['bepa'] == 'hej'
    # cleanup
    client[db][collection_name].delete_many({})
    a = client[db][collection_name].find_one()
    assert a is None
