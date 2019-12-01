from time import sleep
from .datahelpers import GetUrlData, get_data
from .mongo_doc import *
from .mongo_func import *
import pandas as pd
# from  Projects.mongo_data.settings_data import SettingsList, get_safe_settingslist
import krakenex
import newspaper
import logging
import requests

# df_prev = None
__all__ = ['get_coinmarketcap',
           'get_fear_greed_index',
           'get_kraken_orderdepth',
           'get_global_cap',
           'get_bitcoincharts_data',
           'get_bitcoin_fees',
           'get_blockchain_stats',
           'get_news_data']


def get_coinmarketcap():
    # global df_prev
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'f96a1bb1-20b7-428f-9cbc-e76606d2b2f3',
    }
    ints = ['rank', 'last_updated']
    floats = ['price_usd', 'price_btc', '24h_volume_usd', 'market_cap_usd', 'available_supply', 'total_supply',
              'max_supply', 'percent_change_1h', 'percent_change_24h',
              'percent_change_7d']
    data = get_data(url='http://api.coinmarketcap.com/v1/ticker/?limit=100', headers=headers)
    df = pd.DataFrame(data)
    for i in ints:
        df[i] = df[i].astype(int)
    for f in floats:
        df[f] = df[f].astype(float)
    save_tickerdata2(data=df.to_dict(orient='records'), collection_name="coinmarketcap_top100")



def get_fear_greed_index():
    r = requests.get("https://money.cnn.com/data/fear-and-greed/")
    data = r.text
    search_str = "Greed Now:"
    start = data.find("Greed Now:") + len(search_str)
    substr = data[start:start + 10]
    end = substr.find('(')
    greed_index = int(substr[:end].strip())
    data = dict()
    data['fear_greed_idx'] = greed_index
    save_tickerdata2(data=data, collection_name='fear_and_greed_index')



pair_idx = 0  # used by kraken_orderdepths


def get_kraken_orderdepth():
    """
    This getter is a bit special it's a generator instead of a single function because we want the order depth
    often for many currencies.

    :return: status if it was oK or not.
    """
    retries = 3
    depth = '30'
    kraken = krakenex.API()
    pairs = ['ATOMUSD',
             'ADAUSD',
             'DAIUSD',
             'DASHUSD',
             'XETHZUSD',
             'XLTCZUSD',
             'XTZUSD',
             'XXBTZUSD',
             'EOSUSD',
             'XXRPZUSD']
    global pair_idx
    pair = pairs[pair_idx]
    for i in range(retries):
        response = kraken.query_public('Depth', {'pair': pair, 'count': depth})
        if 'error' in response.keys() and len(response['error']) > 0:
            continue
        df1 = pd.DataFrame(response['result'][pair]['asks'], columns=['price', 'volume', 'timestamp'])
        df2 = pd.DataFrame(response['result'][pair]['bids'], columns=['price', 'volume', 'timestamp'])
        df1[['price', 'volume']] = df1[['price', 'volume']].astype(float)
        df2[['price', 'volume']] = df2[['price', 'volume']].astype(float)
        df1['timestamp'].astype(int)
        df2['timestamp'].astype(int)
        # restructure data for better searchability
        data = {'bids': df2.to_dict(orient='list'),
                'asks': df1.to_dict(orient='list'),
                'pair': pair}

        save_tickerdata2(data=data, collection_name='kraken_orderdepth')

        break
    pair_idx += 1
    pair_idx = pair_idx % len(pairs)
    if i > 0:
        raise Exception(f"Needed {i} tries for pair {pair}")
    return


def get_global_cap():
    data = get_data(url='http://api.coinmarketcap.com/v1/global/')
    save_tickerdata2(data=data, collection_name='global_market')



# max every 15 minutes
def get_bitcoincharts_data():
    data = get_data(url='http://api.bitcoincharts.com/v1/markets.json')
    df = pd.DataFrame(data)
    df = df[df['volume'] > 0.1]
    save_tickerdata2(data=df.to_dict(orient='records'), collection_name='bitcoincharts_global')



def get_bitcoin_fees():
    data = get_data(url='https://bitcoinfees.earn.com/api/v1/fees/recommended')
    save_tickerdata2(data=data, collection_name='bitcoin_fees')



def get_blockchain_stats():
    data = get_data(url='https://api.blockchain.info/stats')
    save_tickerdata2(data=data, collection_name='blockchain_stats')



# get every 30 minutes? 15 seems too fast sometimes
def get_news_data():
    # Get list of settings
    try:
        urllist: SettingsList = get_settingslist('CryptoNewsUrls')
        keylist: SettingsList = get_settingslist('CrytoNewsKeywords')
    except BaseException as e:
        raise BaseException(f"{e}: When getting settings lists for bitcoin news")

    logger_name = 'main_scraper.' + "bitcoin_news"
    logger = logging.getLogger(logger_name)

    for url in urllist.list:
        paper = newspaper.build(url, language='en')
        for article in paper.articles:
            try:
                sleep(0.5)
                article.download()
                article.parse()

                keys = [key for key in keylist.list if key in article.title.lower()]
                if len(keys) > 0:
                    # check if article already exists
                    obj = CryptoNews.objects(title=article.title).first()
                    if obj is None:
                        news = CryptoNews()
                        news.title = article.title
                        news.description = article.meta_description
                        news.text = article.text
                        news.tags = keys
                        news.url = article.url
                        # article.nlp()  # how to handle updates, save first then do npl?
                        news.time_posted = article.publish_date
                        news.summary = article.summary
                        news.keywords = article.keywords

                        news.save()
                        logger.info(article.title)

                        # article.keywords
                        # article.summary
                        # article.publish_date
                        # source_url

            except BaseException as e:
                pass
