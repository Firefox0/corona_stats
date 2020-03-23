import requests
from bs4 import BeautifulSoup

class Corona: 

    url = "https://www.worldometers.info/coronavirus/"
    main_counters = {"Total Infected": "-", "Total Deaths": "-", "Total Recovered": "-"}
    countries = {}

    def __init__(self):
        self.update_stats()

    def update_stats(self): 
        stats = requests.get(self.url)
        soup = BeautifulSoup(stats.content, "html.parser")

        main_content_class = soup.find("div", class_="content-inner")
        main_counters = [e.findChild().string.strip() 
                        for e in main_content_class.find_all("div", class_="maincounter-number")]
        counter = 0
        for e in self.main_counters:
            self.main_counters[e] = main_counters[counter]
            counter += 1

        table = soup.find("table", attrs={"id": "main_table_countries_today"})
        table_body = table.find("tbody")
        table_countries = table_body.find_all("tr", attrs={"style": ""})

        for e in table_countries: 
            country_class = e.find("td", attrs={"style": "font-weight: bold; font-size:15px; text-align:left;"})
            country = country_class.string

            cases = []
            for e in e.findAll("td")[1:]:
                try:
                    cases.append(e.string.strip())
                except AttributeError: 
                    cases.append("-")

            self.countries[country] = {"Total Cases": "", "New Cases": "", "Total Deaths": "",
                        "New Deaths": "", "Total Recovered": "", "Active Cases": "",
                        "Serious, Critical": "", "Tot Cases": ""}

            counter = 0
            for e in self.countries[country]:
                self.countries[country][e] = cases[counter]
                counter += 1

    def get_countries(self):
        return self.countries.keys()

    def get_countries_stats(self):
        return self.countries

    def get_country_stats(self, country):
        return self.countries[country]
    
    def get_main_counters(self):
        return self.main_counters

    def prettify(self, iterable):
        return "\n".join(f"{key}: {value}" for key, value in iterable.items())