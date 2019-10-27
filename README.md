# Ticker
This project is supposed to be running on a server and gathering crypto currency information.
All data is stored on a mongo-db.
This ticker has two tasks, one fireing every 5 min to get data from eg coinmarketcap.
The other task is fireing every 15 minutes for more slowly changing information like news-data.

# Run
Run main.py to start the ticker.

# Files
* **main.py:** main-task, alter this to chose what data to be gathered.
* **data_getters.py:** Here you write your functions to save data to the mongo-db
* **datahelpers.py:** Helper functions
* **mongo_obj.py:** descriptors of the ORM for the mongo-db and initiating the database.
* **ticker_scheduler.py** scheduler for running the tasks and print all asserts preventing it from crashing.
* **test_***: unit-tests
