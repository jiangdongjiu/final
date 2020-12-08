import wx
from db_operations import DBOperations
from scrape_weather import WeatherScraper
from plot_operations import PlotOperations

class WeatherProcessor(wx.Frame):
    """docstring for WeatherProcessor."""

    def __init__(self):
        self.db_name = 'weather.sqlite'
        self.table_name = 'weather'

        super().__init__(parent=None, title='Weather Processor')
        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)

        # install all or update db buttons
        install_lbl = wx.StaticText(panel)
        big_font = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL)
        install_lbl.SetFont(big_font)
        install_lbl.SetLabel('Install All or Update Database')
        my_sizer.Add(install_lbl,0,wx.ALL | wx.ALIGN_LEFT,5)

        install_all_btn = wx.Button(panel, label='Install All')
        install_all_btn.Bind(wx.EVT_BUTTON, self.clear_db_and_install_all_weather_data)
        my_sizer.Add(install_all_btn, 0, wx.ALL | wx.LEFT, 5)

        update_btn = wx.Button(panel, label='Update Database')
        update_btn.Bind(wx.EVT_BUTTON, self.update_db)
        my_sizer.Add(update_btn, 0, wx.ALL | wx.LEFT, 5)

        # boxplot part
        boxplot_lbl = wx.StaticText(panel)
        boxplot_lbl.SetFont(big_font)
        boxplot_lbl.SetLabel('Boxplot Year Range')
        my_sizer.Add(boxplot_lbl,0,wx.ALL | wx.ALIGN_LEFT,5)

        from_lbl = wx.StaticText(panel)
        small_font = wx.Font(14, wx.ROMAN, wx.ITALIC, wx.NORMAL)
        from_lbl.SetFont(small_font)
        from_lbl.SetLabel('From: ')
        my_sizer.Add(from_lbl,0,wx.ALL | wx.ALIGN_LEFT,5)

        self.start_year_text_ctrl = wx.TextCtrl(panel)
        my_sizer.Add(self.start_year_text_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        to_lbl = wx.StaticText(panel)
        to_lbl.SetFont(small_font)
        to_lbl.SetLabel('To: ')
        my_sizer.Add(to_lbl,0,wx.ALL | wx.ALIGN_LEFT,5)

        self.end_year_text_ctrl = wx.TextCtrl(panel)
        my_sizer.Add(self.end_year_text_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        boxplot_btn = wx.Button(panel, label='Generate Boxplot')
        boxplot_btn.Bind(wx.EVT_BUTTON, self.boxplot)
        my_sizer.Add(boxplot_btn, 0, wx.ALL | wx.LEFT, 5)

        # lineplot part
        lineplot_lbl = wx.StaticText(panel)
        lineplot_lbl.SetFont(big_font)
        lineplot_lbl.SetLabel('Lineplot Year and Month')
        my_sizer.Add(lineplot_lbl,0,wx.ALL | wx.ALIGN_LEFT,5)

        year_lbl = wx.StaticText(panel)
        year_lbl.SetFont(small_font)
        year_lbl.SetLabel('Year: ')
        my_sizer.Add(year_lbl,0,wx.ALL | wx.ALIGN_LEFT,5)

        self.year_text_ctrl = wx.TextCtrl(panel)
        my_sizer.Add(self.year_text_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        month_lbl = wx.StaticText(panel)
        month_lbl.SetFont(small_font)
        month_lbl.SetLabel('Month: ')
        my_sizer.Add(month_lbl,0,wx.ALL | wx.ALIGN_LEFT,5)

        self.month_text_ctrl = wx.TextCtrl(panel)
        my_sizer.Add(self.month_text_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        lineplot_btn = wx.Button(panel, label='Generate Lineplot')
        lineplot_btn.Bind(wx.EVT_BUTTON, self.lineplot)
        my_sizer.Add(lineplot_btn, 0, wx.ALL | wx.LEFT, 5)


        panel.SetSizer(my_sizer)
        self.Show()

    def boxplot(self, event):
        start_year = self.start_year_text_ctrl.GetValue()
        end_year = self.end_year_text_ctrl.GetValue()
        db_name = 'weather.sqlite'
        table_name = 'weather'
        my_plot_operations = PlotOperations(db_name, table_name)
        my_plot_operations.generate_boxplot(int(start_year), int(end_year))

    def lineplot(self, event):
        year = self.year_text_ctrl.GetValue()
        month = self.month_text_ctrl.GetValue()
        db_name = 'weather.sqlite'
        table_name = 'weather'
        my_plot_operations = PlotOperations(db_name, table_name)
        my_plot_operations.generate_lineplot(int(year), int(month))

    def clear_db_and_install_all_weather_data(self, event):
        myweather = WeatherScraper()
        myweather.start_scraping()
        weather_data_from_weather_scraper = myweather.weather
        db_operations = DBOperations(self.db_name)
        db_operations.initialize_db(self.table_name)
        db_operations.purge_data(self.table_name)
        db_operations.save_data(weather_data_from_weather_scraper, self.table_name)

    def update_db(self, event):
        myweather = WeatherScraper()
        with DBOperations(self.db_name) as dbcm:
            dbcm.execute(f"select max(sample_date) from {self.table_name};")
            latest_date = dbcm.fetchall()[0][0]

        print('latest date in db', latest_date)
        myweather.start_scraping(latest_date)
        weather_data_from_weather_scraper = myweather.weather
        db_operations = DBOperations(self.db_name)
        db_operations.initialize_db(self.table_name)
        db_operations.save_data(weather_data_from_weather_scraper, self.table_name)

if __name__ == '__main__':
    app = wx.App()
    frame = WeatherProcessor()
    frame.SetSize(500,600)
    app.MainLoop()
    input("press enter to finish")
