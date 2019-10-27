from time import sleep

from .ticker_logger import *
from .data_getters import *
from .ticker_scheduler import Ticker_Scheduler
from .mongo_func import init_mongodb


# todo, add automatic updates: https://hackthology.com/how-to-write-self-updating-python-programs-using-pip-and-git.html
# todo, create HTML report to be able to login
task_3sec = Ticker_Scheduler(update_period_s=3,
                             callback_list=get_kraken_orderdepth,
                             taskname='1min tasks' )


task_5min = Ticker_Scheduler(update_period_s=60 * 5, callback_list=[get_coinmarketcap,
                                                                    get_fear_greed_index,
                                                                    get_global_cap,
                                                                    get_bitcoincharts_data,
                                                                    get_bitcoin_fees,
                                                                    get_blockchain_stats],
                             taskname='5min tasks')

task_15min = Ticker_Scheduler(update_period_s=60 * 60, callback_list=[get_news_data,
                                                                      get_bitcoincharts_data],
                              taskname='15min tasks')
if __name__ == "__main__":
    init_mongodb()
    create_logger()
    task_5min.start_thread()
    task_15min.start_thread()
    task_3sec.start_thread()
    while 1:
        sleep(20)
