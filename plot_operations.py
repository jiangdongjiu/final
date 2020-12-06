class PlotOperations(object):
    """docstring for PlotOperations."""

    def __init__(self, arg):
        super(PlotOperations, self).__init__()
        self.arg = arg

    def receive_and_processe_weather_data(self, year: int):
        mean_temps_for_plot = {}
        for daily_temps in fetch_weather:
            year = daily_temps[1][:4]
            month = daily_temps[1][5:7]
            mean_temp = daily_temps[-1]

            if year in mean_temps_for_plot:
                if month in mean_temps_for_plot[year]:
                    mean_temps_for_plot[year][month].append(mean_temp)
                else:
                    mean_temps_for_plot[year][month] = [mean_temp]
            else:
                mean_temps_for_plot[year]= {}
                mean_temps_for_plot[year][month] = [mean_temp]


        return mean_temps_for_plot
