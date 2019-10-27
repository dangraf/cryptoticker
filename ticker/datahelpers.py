import urllib.request as urlreq
import json
import numpy as np
import pandas as pd

def get_new_unique_data(old_df:pd.DataFrame, new_df:pd.DataFrame)->pd.DataFrame:
    if old_df is None:
        return new_df
    mask = np.ones(len(new_df), dtype=bool)

    for col in new_df.columns:
        mask &= new_df[col].isin(old_df[col])

    return new_df[~mask].dropna()

class GetUrlData:
    def __init__(self, url):
        self.result = None
        self.e = None
        self.url = url

    def do_work(self):
        req = urlreq.Request(url=self.url, headers={'User-Agent': 'Magic Browser'})
        try:
            responce = urlreq.urlopen(req)
            the_page = responce.read()
            encoding = responce.info().get_content_charset('utf-8')
            self.result = json.loads(the_page.decode(encoding))
        except BaseException as e:
            self.e = e

    def get_result(self):
        if self.e:
            raise self.e
        else:
            return self.result
