from Requester import Requester
from Beautify import Beautify
from Firestore import FirePost
from time import sleep


class PageScraper:
    __page_content = None
    __requester = None
    __beautify = None

    def __init__(self, url):
        self.__requester = Requester(url)

    def initialize(self):
        self.__page_content = self.__requester.get_page_content()
        self.__beautify = Beautify(self.__page_content)

    def run(self):
        while True:
            self.__beautify.parse_content()
            self.__beautify.filter_main_counters()
            self.__beautify.log_main_counters()
            self.__beautify.parse_statistics('belgium')

            local_data = self.__beautify.get_local_statistics()
            global_data = self.__beautify.get_global_statistics()

            FirePost.send_global_data_to_firebase(
                total_dead=global_data['total_dead'],
                total_infected=global_data['total_infected'],
                total_recovered=global_data['total_recovered']
            )

            FirePost.send_local_data_to_firebase(
                country=local_data['country'],
                total_cases=local_data['total_cases'],
                new_cases=local_data['new_cases'],
                total_deaths=local_data['total_deaths'],
                new_deaths=local_data['new_deaths'],
                total_recovered=local_data['total_recovered'],
                active_cases=local_data['active_cases'],
                critical=local_data['serious_critical'],
                total_case_per_million=local_data['total_cases_per_1_million']
            )

            # sleep 24 hours
            sleep(60 * 60 * 24)


scraper = PageScraper('https://www.worldometers.info/coronavirus/')
scraper.initialize()
scraper.run()
