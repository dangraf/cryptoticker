import logging
import datetime as dt
from time import sleep
import _thread
import types
__all__ = ['Ticker_Scheduler']

# callback: get_name(), get_data(), vad händer om klassen krashar? får inte vara en klass..
class Ticker_Scheduler():
    def __init__(self, update_period_s, callback_list, taskname):
        self.update_period_s = update_period_s
        self.callback_list = callback_list
        self.taskname = taskname
        self.running = True
        self.logger = None
        self.LastUpdate = dt.datetime.fromtimestamp(0)
        self._get_logger()
        # _thread.start_new_thread(self.run())

    def start_thread(self):
        t = _thread.start_new_thread(self._run, ())

    def _get_logger(self):
        """ gets logger defined in main_scraper"""
        logger_name = 'main_scraper.' + self.taskname
        self.logger = logging.getLogger(logger_name)
        self.logger.info("started logging for{0}".format(logger_name))

    def _wait_until_next_update(self):
        current_time = dt.datetime.now()

        time_to_wait = self.update_period_s - (current_time - self.LastUpdate).total_seconds()
        logging.info(time_to_wait)
        if time_to_wait < 0:
            time_to_wait = self.update_period_s
        sleep(time_to_wait)
        self.LastUpdate = dt.datetime.now()

    def _run(self):
        while (self.running):
            for i, callback in enumerate(self.callback_list):
                try:
                    self.logger.info(f' Running: {callback}')
                    callback()


                except BaseException as e:
                    self.logger.error(f"callback:{callback}: {e}")
            self._wait_until_next_update()
