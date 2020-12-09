"""
Create a db_operations.py module with a DBOperations class inside.
• Use the Python sqlite3 module to store the weather data in an SQLite
database in the specified format. SQL queries to create and query the DB
can be provided if required. The DB format for your reference:
◦ id -> integer, primary key, autoincrement
◦ sample_date -> text
◦ location -> text
◦ min_temp -> real
◦ max_temp -> real
◦ avg_temp -> real
• Create a method called fetch_data that will return the requested data for
plotting.
• Create a method called save_data that will save new data to the DB, if it
doesn’t already exist (i.e. don’t duplicate data).
• Create a method called initialize_db to initialize the DB if it doesn’t
already exist.
• Create a method called purge_data to purge all the data from the DB for
when the program fetches all new weather data.
• Create a context manager called DBCM to manage the database
connections.
• All database operation should be self contained in the DBOperations class.
There should be no database code anywhere else in the program.

"""
import sqlite3
import pprint
from scrape_weather import WeatherScraper

class DBOperations():
    """docstring for DBOperations."""

    def __init__(self, db_name: str):
        """ initialize database connection """
        self.name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ close db connection """
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def initialize_db(self, table_name: str):
        """
        initialize the database and create the table.
        """
        create_table_sql =  f"""
                            create table if not exists {table_name} (
                                id integer primary key autoincrement not null,
                                sample_date text not null unique,
                                location text not null,
                                min_temp real not null,
                                max_temp real not null,
                                avg_temp real not null);
                            """
        with DBOperations(self.name) as dbcm:
            dbcm.execute(create_table_sql)

    def save_data(self, data_dict: dict, table_name: str):
        """
        receive a dictionary of dictionaries and correctly insert the data into the DB.
        """
        location = "Winnipeg, MB"
        insert_sql = f"""insert or ignore into {table_name}
                   (sample_date, location, min_temp, max_temp, avg_temp)
                   values
                   (?,?,?,?,?)"""

        with DBOperations(self.name) as dbcm:
            for date, temps in data_dict.items():
                data_tuple = (date, location, temps['Min'] ,temps['Max'], temps['Mean'])
                dbcm.execute(insert_sql, data_tuple)

    def fetch_data(self, table_name: str, year: int) -> list:
        """
        fetch the data base on year in the database.
        """
        with DBOperations(self.name) as dbcm:
            dbcm.execute(f"select * from {table_name} where sample_date like '{year}%';")
            fetch_weather = dbcm.fetchall()

        return fetch_weather


    def purge_data(self, table_name: str):
        """
        purge the data currently in the database.
        """
        with DBOperations(self.name) as dbcm:
            dbcm.execute(f"delete from {table_name} ;")


if __name__ == "__main__":
    WEATHER = WeatherScraper()
    WEATHER.start_scraping()
    weather_data_from_weather_scraper = WEATHER.weather
    DB_NAME = 'weather.sqlite'
    TABLE_NAME = 'weather'
    DB_OPERATIONS = DBOperations(DB_NAME)
    DB_OPERATIONS.initialize_db(TABLE_NAME)
    DB_OPERATIONS.purge_data(TABLE_NAME)
    DB_OPERATIONS.save_data(weather_data_from_weather_scraper, TABLE_NAME)
    pprint.pprint(DB_OPERATIONS.fetch_data(TABLE_NAME, 1996))
