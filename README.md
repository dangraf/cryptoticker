# Ticker
This project is supposed to be running on a server and gathering crypto currency information.
All data is stored on a mongo-db.
This ticker has two tasks, one fireing every 5 min to get data from eg coinmarketcap.
The other task is fireing every 15 minutes for more slowly changing information like news-data.

# prepare before run:
* install mongodb
* add collection of type "SettingsList" (see mongo_doc.py) named "CryptoNewsUrls" and fill the list with urls from newspapers you want to follow
* add collection of type "SettingsList" and fill it with keywords it will search for in article titles. 

# Run
Run main.py to start the ticker.
go to 127.0.0.1:5000 to look at the log-file in a webbrowser.

# Files
* **main.py:** main-task, alter this to chose what data to be gathered.
* **data_getters.py:** Here you write your functions to save data to the mongo-db
* **datahelpers.py:** Helper functions
* **mongo_doc.py:** descriptors of mongodb documents.
* **mongo_func.py** functions to initialize, read and write info to mongodb
* **ticker_scheduler.py** scheduler for running the tasks and print all asserts preventing it from crashing.
* **test_***: unit-tests
