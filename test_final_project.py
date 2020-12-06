import unittest
import sqlite3
from scrape_weather import WeatherScraper
from db_operations import DBOperations
# from plot_operations import PlotOperations
# from weather_processor import WeatherProcessor


class TestScraping(unittest.TestCase):
    def setUp(self):
        self.myweather = WeatherScraper()

    def test_scraper_type(self):
        self.assertIsInstance(self.myweather, WeatherScraper)

    def test_weather_return_type(self):
        year = 1996
        month = 1
        url = ("http://climate.weather.gc.ca/"
                           + "climate_data/daily_data_e.html"
                           + "?StationID=27174"
                           + "&timeframe=2&StartYear=1840"
                           + "&EndYear=" + str(year)
                           + "&Day=1&Year=" + str(year)
                           + "&Month=" + str(month) + "#")
        self.myweather.start_scraping(url, year)
        self.assertIs(type(self.myweather.weather), dict)
        daily = self.myweather.weather[list(self.myweather.weather.keys())[0]]
        self.assertIs(type(daily), dict)

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.dbname = "weather.sqlite"
        self.mydb = DBOperations(self.dbname)

    def test_db_type(self):
        self.assertIsInstance(self.mydb, DBOperations)

    def test_db_structure(self):
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()
        sql_select = """select id, sample_date, location,
                        min_temp, max_temp, avg_temp from weather"""
        self.assertIsNotNone(cur.execute(sql_select))

# class TestPlot(unittest.TestCase):
#     def setUp(self):
#         self.myplot = PlotOperations()
#
#     def test_plot_type(self):
#         self.assertIsInstance(self.myplot, PlotOperations)
#
# class TestWeatherProcessor(unittest.TestCase):
#     def setUp(self):
#         self.myweatherprocessor = WeatherProcessor()
#
#     def test_weather_processor_type(self):
#         self.assertIsInstance(self.myweatherprocessor, WeatherProcessor)


if __name__ == "__main__":
    unittest.main(verbosity=2)
