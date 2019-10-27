import mongoengine
from .mongo_doc import *


def init_mongodb():
    mongoengine.register_connection(alias='settings', name='apps_settings', host='userver2', port=27017)
    mongoengine.register_connection(alias='NewsDb', name='ticker_db', host='userver2', port=27017)
    mongoengine.register_connection(alias='ticker', name='ticker_db', host='userver2', port=27017)


def save_tickerdata(*, data, collection_name: str):
    try:
        obj = TickerData()
        obj.data = data
        obj.switch_collection(collection_name)
        obj.save()
    except BaseException as e:
        print(e)


def get_settingslist(listname: str) -> SettingsList:
    """
    Finds a list in the settings collection
    :param listname: name of the list to be found
    :return: returns a SettingsList object
    """
    setlist = SettingsList.objects(name=listname).first()
    return setlist
