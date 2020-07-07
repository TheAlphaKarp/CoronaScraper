from bs4 import BeautifulSoup


class Beautify:
    __raw_content = None
    __content = None

    __death_count = 0
    __infected_count = 0
    __recovered_count = 0

    __statistics_template = [
        "country",
        "total_cases",
        "new_cases",
        "total_deaths",
        "new_deaths",
        "total_recovered",
        "active_cases",
        "serious_critical",
        "total_cases_per_1_million"
    ]

    __statistics_dict = {}

    def __init__(self, content):
        self.__raw_content = content

    def parse_content(self):
        self.__content = BeautifulSoup(self.__raw_content, 'html.parser')

    def filter_main_counters(self):
        counters = self.__content.find_all(id="maincounter-wrap")

        for index, tag in enumerate(counters):
            if index == 0:
                self.__infected_count = tag.find('span').text
            elif index == 1:
                self.__death_count = tag.find('span').text
            else:
                self.__recovered_count = tag.find('span').text

    def log_main_counters(self):
        print(f"Infected: {self.__infected_count}")
        print(f"dead: {self.__death_count}")
        print(f"recovered: {self.__recovered_count}")

    def parse_statistics(self, country):
        table_rows = self.__content.find_all('tr')

        for index, row in enumerate(table_rows):
            if row.findChild().text.strip().lower() != country:
                continue

            cols = row.findChildren()

            for i, col in enumerate(cols):
                self.__statistics_dict[self.__statistics_template[i]] = col.text

            break

    def get_local_statistics(self):
        return self.__statistics_dict

    def get_global_statistics(self):
        return {
            "total_infected": self.__infected_count,
            "total_dead": self.__death_count,
            "total_recovered": self.__recovered_count,
        }
