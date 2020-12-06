from db_operations import DBOperations
from scrape_weather import WeatherScraper
import pprint

class PlotOperations(object):
    """docstring for PlotOperations."""

    def __init__(self, db: str, table: str):
        self.db_name = db
        self.table_name = table

    def scrape_and_save_weather_data(self, end_year:int):
        myweather = WeatherScraper()
        myweather.start_scraping('url', end_year)
        weather_data_from_weather_scraper = myweather.weather
        db_operations = DBOperations(self.db_name)
        db_operations.initialize_db(self.table_name)
        db_operations.purge_data(self.table_name)
        db_operations.save_data(weather_data_from_weather_scraper, self.table_name)

    def receive_and_format_data(self, year: int) -> dict:
        db_operations = DBOperations(self.db_name)
        weather_data = db_operations.fetch_data(self.table_name, year)

        mean_temps_for_plot = {}
        for daily_temps in weather_data:
            month = daily_temps[1][5:7]
            mean_temp = daily_temps[-1]

            if int(month) in mean_temps_for_plot:
                mean_temps_for_plot[int(month)].append(mean_temp)
            else:
                mean_temps_for_plot[int(month)] = [mean_temp]

        return mean_temps_for_plot

if __name__ == "__main__":
    db_name = 'weather.sqlite'
    table_name = 'weather'
    my_plot_operations = PlotOperations(db_name, table_name)
    my_plot_operations.scrape_and_save_weather_data(1997)
    pprint.pprint(my_plot_operations.receive_and_format_data(1996))
