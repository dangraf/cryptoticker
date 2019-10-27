from unittest import TestCase
from ticker.ticker_scheduler import Ticker_Scheduler
from time import sleep

cntr = 0


def happy_callback():
    global cntr
    cntr += 1
    return


def assert_callback():
    global cntr
    cntr += 1
    assert "Simulates fail"


class TestTickerScheduler(TestCase):

    def test_wait_until_next_update_allOK(self):
        # setup
        global cntr
        cntr = 0
        s = Ticker_Scheduler(update_period_s=0.25, callback_list=[happy_callback], taskname="Unit test")
        # test that happy, callback is called
        s.start_thread()
        sleep(0.3)
        s.running = False
        # verify that it was called
        self.assertEqual(cntr, 2)

    def test_wait_until_next_update_when_assert(self):
        # setup
        global cntr
        cntr = 0
        s = Ticker_Scheduler(update_period_s=0.25, callback_list=[assert_callback], taskname="Unit test")
        # test that happy, callback is called
        s.start_thread()
        sleep(0.3)
        s.running = False
        # verify that it was called
        self.assertEqual(cntr, 2)
