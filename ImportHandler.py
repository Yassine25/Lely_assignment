import datetime
import json
from urllib.request import urlopen

from Repository import Repository

repositories = []


class ImportHandler:

    @staticmethod
    def handle_import_repositories():
        url = "https://api.github.com/events"
        for data in ImportHandler.get_json_data(url):
            if str(data['type']).lower() == 'pullrequestevent':
                repository_items = data['repo']
                repo = Repository(repository_items['id'], repository_items['name'], repository_items['url'])
                repositories.append(repo)
                ImportHandler.handle_import_pull_requests(repo)

    @staticmethod
    def handle_calculation_average_duration(pull_requests):
        checked_date_times = []
        date_times = []
        index = 0
        for i in range(index, len(pull_requests)):
            first_date = getattr(pull_requests[i], 'date_time')
            if first_date not in checked_date_times:
                checked_date_times.append(first_date)
                for j in range(index + 1, len(pull_requests) - i):
                    second_date = getattr(pull_requests[j], 'date_time')
                    if datetime.date(first_date) == datetime.date(second_date):
                        date_times.append(first_date)
                        date_times.append(second_date)

                ImportHandler.calculate_average_duration(date_times)
                date_times.clear()
            index += 1

    # this method calculates the average duration of pull requests grouped by dates of the same date
    @staticmethod
    def calculate_average_duration(date_times):
        sorted_date_times = sorted(date_times)
        for i in sorted_date_times:
            print("ss", sorted_date_times[i])
        duration = 0
        avg = 0
        for i in range(0, len(sorted_date_times) - 1):
            start = int(round(datetime.strptime(str(sorted_date_times[i]), "%Y-%m-%d %H:%M:%S").timestamp()))
            end = int(round(datetime.strptime(str(sorted_date_times[i + 1]), "%Y-%m-%d %H:%M:%S").timestamp()))
            duration += end - start
        avg = duration / (len(sorted_date_times) - 1)
        return avg

    @staticmethod
    def get_json_data(url):
        try:
            response = urlopen(url)
            return json.loads(response.read())
        except Exception as ex:
            print(ex)
            return None
