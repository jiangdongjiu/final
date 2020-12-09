"""
• Create a plot_operations.py module with a PlotOperations class inside.
• Use Python matplotlib to create a basic boxplot of mean temperatures in a
date range (year to year, ex. 2000 to 2020) supplied by the user:
◦ https://matplotlib.org/examples/pylab_examples/boxplot_demo.html
• In addition to the above box plot, display a line plot of a particular months
mean temperature data, based on user input. For example, display all the
daily mean temperatures from January 2020, with the x axis being the day,
and the y axis being temperature.
◦ https://matplotlib.org/tutorials/introductory/pyplot.html#sphx-glrtutorials-introductory-pyplot-py
• All plotting code should be self contained in the PlotOperations class.
There should be no plotting code anywhere else in the program.
"""

from db_operations import DBOperations
from scrape_weather import WeatherScraper
import pprint
from datetime import date
from pathlib import Path
import matplotlib.pyplot as plt

class PlotOperations():
    """docstring for PlotOperations."""

    def __init__(self, db: str, table: str):
        self.db_name = db
        self.table_name = table

    def receive_and_format_data(self, year: int, specific_month: int = 0) -> dict:
        """
        input year and output a dictionary
        output when month is not specified:
            daily mean temperatures of each month for the year
            weather_data = {1: [1.1, 5.5, 6.2, 7.1], 2: [8.1, 5.4, 9.6, 4.7]}
            The dictionary key is the month: January = 1, February = 2 etc...
        output when month is specified:
            weather_data = {1: 1.1, 2: 8.1}
            The dictionary key is the day
        """
        db_operations = DBOperations(self.db_name)
        weather_data = db_operations.fetch_data(self.table_name, year)

        mean_temps_for_plot = {}
        if not specific_month:
            for daily_temps in weather_data:
                month = daily_temps[1][5:7]
                mean_temp = daily_temps[-1]

                if int(month) in mean_temps_for_plot:
                    mean_temps_for_plot[int(month)].append(mean_temp)
                else:
                    mean_temps_for_plot[int(month)] = [mean_temp]
        else:
            for daily_temps in weather_data:
                month = daily_temps[1][5:7]
                day = daily_temps[1][-2:]
                mean_temp = daily_temps[-1]

                if int(month) == specific_month:
                    mean_temps_for_plot[int(day)] = mean_temp
        return mean_temps_for_plot

    def generate_boxplot(self, start_year: int, end_year: int):
        """
        generate a boxplot for temperature distributions monthly
        from start year to end year
        """
        # save all years weather in one dictionary monthly {1:[all January]...}
        years = range(start_year, end_year+1)
        monthly_weather_data = {}
        for year in years:
            weather_data_year = self.receive_and_format_data(year)
            for month, temps in weather_data_year.items():
                if month in monthly_weather_data:
                    monthly_weather_data[month] += temps
                else:
                    monthly_weather_data[month] = temps

        # check exiting month data and use [] for missing month [[],[Feb]]
        monthly_weather_data_for_plot = []
        for month in range(1, 13):
            if month in monthly_weather_data:
                monthly_weather_data_for_plot.append(monthly_weather_data[month])
            else:
                monthly_weather_data_for_plot.append([])

        # boxplot
        plot_title = 'Monthly Temperature Distribution for:' + str(start_year) + ' to ' + str(end_year)
        plt.figure()
        plt.boxplot(monthly_weather_data_for_plot)
        plt.xlabel('Month')
        plt.ylabel('Temperature (Celsius)')
        plt.title(plot_title)
        plt.xlim(0, 13)
        Path("./images").mkdir(parents=True, exist_ok=True)
        save_path = f'./images/boxplot_from{start_year}to{end_year}.jpg'
        plt.savefig(save_path)
        plt.show()

    def generate_lineplot(self, year: int, month: int) -> dict:
        """
        generate a lineplot for temperature changing for specific year and month
        """
        weather_data_month = self.receive_and_format_data(year, month)
        days = weather_data_month.keys()
        temps = weather_data_month.values()
        plt.plot(days, temps)
        plt.xlabel('Day')
        plt.ylabel('Temperature (Celsius)')
        plot_title = 'Daily Temperature Distribution for:'+ str(year) + '/' + str(month)
        plt.title(plot_title)
        Path("./images").mkdir(parents=True, exist_ok=True)
        save_path = f'./images/lineplot_{year}-{month}.jpg'
        plt.savefig(save_path)
        plt.show()

if __name__ == "__main__":
    db_name = 'weather.sqlite'
    table_name = 'weather'
    my_plot_operations = PlotOperations(db_name, table_name)
    my_plot_operations.generate_boxplot(2018, 2020)
    my_plot_operations.generate_lineplot(2011, 10)
