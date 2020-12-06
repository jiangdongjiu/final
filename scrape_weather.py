from datetime import datetime
from html.parser import HTMLParser
import urllib.request
import pprint

class WeatherScraper(HTMLParser):
    """docstring for WeatherScraper."""

    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = 0
        self.data_list = []
        self.weather = {}

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

    def start_scraping(self, url, year):
        current_year = year
        current_month = 12
        while True:
            url = ("http://climate.weather.gc.ca/"
                               + "climate_data/daily_data_e.html"
                               + "?StationID=27174"
                               + "&timeframe=2&StartYear=1840"
                               + "&EndYear=" + str(current_year)
                               + "&Day=1&Year=" + str(current_year)
                               + "&Month=" + str(current_month) + "#")
            myparser = WeatherScraper()
            current_url = url + ""
            with urllib.request.urlopen(url) as response:
                html = str(response.read())
            myparser.feed(html)

            daily_temps = {}
            count = 0
            current_date = ""
            for d in myparser.data_list:
                try:
                    datetime.strptime(d, '%Y-%m-%d')
                    current_date = d
                    if current_date in self.weather:
                        return
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
            print(current_year, current_month)
            current_month -= 1
            if current_month == 0:
                current_month = 12
                current_year -= 1

if __name__=="__main__":
    url = 'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2020&Day=1&Year=2020&Month=12'
    year = 2020
    myweather = WeatherScraper()
    myweather.start_scraping(url, year)
    pprint.pprint(myweather.weather)

    # datetime.date.today()-datetime.timedelta(1)
