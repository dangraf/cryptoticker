import mongoengine
from .mongo_doc import *
from typing import Dict
from pymongo import MongoClient
from datetime import datetime

__all__ = ['init_mongodb',
           'save_tickerdata2',
           'get_settingslist']
client:MongoClient
def init_mongodb():
    global client
    client = MongoClient(host='userver2', retryWrites=True)
    mongoengine.register_connection(alias='settings', name='apps_settings', host='userver2', port=27017)
    mongoengine.register_connection(alias='NewsDb', name='ticker2_db', host='userver2', port=27017)
    #mongoengine.register_connection(alias='ticker', name='ticker_db', host='userver2', port=27017)

def save_tickerdata2(data:Dict, collection_name: str):
    global client

    try:
        client.server_info()
    except:
        init_mongodb()
    ob = dict()
    ob['data'] = data
    ob['timestamp'] = datetime.now()
    client = MongoClient(host='userver2', retryWrites=True)
    client['ticker2_db'][collection_name].insert_one(ob)






def get_settingslist(listname: str) -> SettingsList:
    """
    Finds a list in the settings collection
    :param listname: name of the list to be found
    :return: returns a SettingsList object
    """
    setlist = SettingsList.objects(name=listname).first()
    return setlist
