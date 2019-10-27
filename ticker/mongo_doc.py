from mongoengine import DynamicDocument, DateTimeField, Document, StringField, ListField
from datetime import datetime

__all__ = ['TickerData',
           'SettingsList',
           'CryptoNews']

class TickerData(DynamicDocument):
    timestamp = DateTimeField(default=datetime.now, unique=True)
    meta = {
        'db_alias': 'ticker',
        'collection': 'Uninitiated'
    }
class SettingsList(Document):
    name = StringField(unique=True, required=True)
    list = ListField(StringField())
    meta = {
        'db_alias': 'settings',
        'collection': 'lists'
    }

class CryptoNews(Document):
    timestamp = DateTimeField(default=datetime.now)
    tags = ListField(StringField(), required=True)
    title = StringField(max_length=200, required=True, unique=True)
    description = StringField(max_length=400, required=True)
    text = StringField(required=True)
    url = StringField(max_length=200, required=True)
    time_posted = DateTimeField(required=False)
    summay = StringField(required=False)
    keywords = ListField(StringField(), required=False)
    meta = {
        'db_alias': 'NewsDb',
        'collection': 'CryptoNews'
    }