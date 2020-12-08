"""
Create a scrape_weather.py module with a WeatherScraper class inside.
• Use the Python HTMLParser class to scrape Winnipeg weather data (min,
max & mean temperatures) from the Environment Canada website, from
the current date, as far back in time as is available.
◦ http://climate.weather.gc.ca/climate_data/daily_data_e.html?
StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=
1&Year=2018&Month=5#
◦ Notice the year and month is encoded directly in the URL.
• Your code must automatically detect when no more weather data is
available for scraping. In other words, you are not allowed to hard code the
last available date into your program. You are also not allowed to fetch the
last date from any dropdown menus on the site.
◦ You can try using a web browser to go back to the earliest available
weather url. Then modify the date in the url to go back earlier, and see
what happens. Use that knowledge to write your code in a way that
detects when it can’t go back any further in time.
• All scraping code should be self-contained inside the WeatherScraper
class. There should be no scraping code anywhere else in the program.
"""

from datetime import datetime
from html.parser import HTMLParser
import urllib.request
import pprint
import threading

class WeatherScraper(HTMLParser):
    """docstring for WeatherScraper."""

    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = 0
        self.data_list = []
        self.weather = {}
        self.stop = False

    def handle_starttag(self, tag, attrs):
        if tag == 'abbr':
            if attrs[0][1]:
                try:
                    date = attrs[0][1]
                    self.data_list.append(datetime.strptime(date, '%B %d, %Y').strftime('%Y-%m-%d'))
                except Exception as e:
                    return

        if tag not in ['td']:
            return

        if self.recording:
            self.recording += 1
            return

        if tag in ['td']:
            self.recording = 1


    def handle_endtag (self, tag):
        if tag in ['td'] and self.recording:
            self.recording -= 1


    def handle_data (self, data):
        if self.recording:
            self.data_list.append(data)

    def monthly_scraping(self, year:int, month:int, date_for_stop:str = None):
        """
        Input The starting URL to scrape, base on year and month.
        Output A dictionary of dictionaries. For example:
        • daily_temps = {“Max”: 12.0, “Min”: 5.6, “Mean”: 7.1}
        • weather = {“2018-06-01”: daily_temps, “2018-06-02”: daily_temps}
        """
        url = ("http://climate.weather.gc.ca/"
                           + "climate_data/daily_data_e.html"
                           + "?StationID=27174"
                           + "&timeframe=2&StartYear=1840"
                           + "&EndYear=" + str(year)
                           + "&Day=1&Year=" + str(year)
                           + "&Month=" + str(month) + "#")
        try:
            myparser = WeatherScraper()
            with urllib.request.urlopen(url) as response:
                html = str(response.read())
            myparser.feed(html)
        except Exception as e:
            print(e)

        useful_data = myparser.data_list
        if date_for_stop:
            if date_for_stop in useful_data:
                useful_data = useful_data[useful_data.index(date_for_stop)+1:]
                self.stop = True

        daily_temps = {}
        count = 0
        current_date = ""

        for d in useful_data:
            try:
                datetime.strptime(d, '%Y-%m-%d')
                current_date = d
                if current_date in self.weather:
                    self.stop = True

                daily_temps[current_date] = []
                count = 0
            except Exception as e:
                if d and current_date:
                    if 'Legend' not in d and d != 'E':
                        count += 1
                        if count <= 3:
                            try:
                                daily_temps[current_date].append(float(d))
                            except:
                                daily_temps.pop(current_date, None)
        keys = ["Max", "Min", "Mean"]
        for date, temp in daily_temps.items():
            daily_temps[date] = {keys[i]: temp[i] for i in range(len(keys))}

        self.weather.update(daily_temps)



    def start_scraping(self, date_for_stop: str = None):
        """
        Input The starting URL to scrape, encoded with today’s date.
        Output A dictionary of dictionaries. For example:
        • daily_temps = {“Max”: 12.0, “Min”: 5.6, “Mean”: 7.1}
        • weather = {“2018-06-01”: daily_temps, ... “2020-12-1”: daily_temps}
        """
        today = datetime.today()
        year = 1998
        month = today.month
        while not self.stop:
            self.monthly_scraping(year, month, date_for_stop)
            print(year, month)
            month -= 1
            if month == 0:
                month = 12
                year -= 1
        # while not self.stop:
        #     x = threading.Thread(target=self.monthly_scraping, args=(year, month, date_for_stop,))
        #     x.start()
        #     month -= 1
        #     if month == 0:
        #         month = 12
        #         year -= 1


if __name__=="__main__":
    myweather = WeatherScraper()
    # myweather.start_scraping()
    myweather.start_scraping('1996-11-05')
    pprint.pprint(myweather.weather)
