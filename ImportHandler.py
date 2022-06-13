import json
from datetime import datetime, timedelta
from urllib.request import urlopen

from PullRequest import PullRequest
from Repository import Repository

repositories = []


class ImportHandler:

    # this method is responsible for the import of repositories reads and holds the id, name and url
    # the repository object wil be passed to handle_import_pull_requests
    @staticmethod
    def handle_import_repositories():
        url = "https://api.github.com/events"
        if not ImportHandler.get_json_data(url) is None:
            for data in ImportHandler.get_json_data(url):
                if str(data['type']).lower() == 'pullrequestevent':
                    repository_items = data['repo']
                    repository = Repository(repository_items['id'], repository_items['name'], repository_items['url'])
                    repositories.append(repository)
                    ImportHandler.handle_import_pull_requests(repository)

    # this method is responsible for the import of pull requests. important info like id, number and created_at will
    # hold. Only repositories with more than one pull request will be passed
    @staticmethod
    def handle_import_pull_requests(repository):
        url = repository.url + "/pulls"
        if not ImportHandler.get_json_data(url) is None:
            for data in ImportHandler.get_json_data(url):
                pull_request_url = data['url']
                pull_request_data = ImportHandler.get_json_data(pull_request_url)
                pull_request = PullRequest(pull_request_data['id'], pull_request_data['number'],
                                           datetime.strptime(pull_request_data['created_at'], '%Y-%m-%dT%H:%M:%Sz'))
                repository.pull_requests.append(pull_request)

            if len(repository.pull_requests) > 1:
                ImportHandler.handle_calculation_average_duration(repository)
            else:
                print("no pull requests available for this repository")

    # this method is part of the calculation of the average duration of pull requests
    # average duration of pull requests will be only calculated if there are more than one pull request
    # for the same date. The end result is average duration time of pull requests for a given repository for
    # different dates
    @staticmethod
    def handle_calculation_average_duration(repository):
        checked_date_times = []
        date_times = []
        index = 0
        avg_duration = 0
        date_times_counter = 0
        for i in range(index, len(repository.pull_requests)):
            first_date = repository.pull_requests[i].date_time
            if datetime.date(first_date) not in checked_date_times:
                checked_date_times.append(datetime.date(first_date))
                date_times.append(first_date)
                for j in range(index + 1, len(repository.pull_requests) - 1):
                    second_date = repository.pull_requests[j].date_time
                    if datetime.date(first_date) == datetime.date(second_date):
                        date_times.append(second_date)
                if len(date_times) > 1:
                    date_times_counter += 1
                    avg_duration += ImportHandler.calculate_average_duration(date_times)
                    date_times.clear()
            avg_duration = avg_duration / date_times_counter
            index += 1

        if (avg_duration / 60) > 3600:
            print(str.format("avg duration for repository {0}, in hours = {1}").format(repository.name,
                                                                                       avg_duration / 3600))
        elif (avg_duration / 60) < 3600:
            print(str.format("avg duration for repository {0}, in minutes = {1}").format(repository.name,
                                                                                         avg_duration / 60))

    # this method calculates the average duration of pull requests grouped by dates of the same date
    @staticmethod
    def calculate_average_duration(date_times):
        sorted_date_times = sorted(date_times)
        duration = 0
        for i in range(0, len(sorted_date_times) - 1):
            start = int(round(datetime.strptime(str(sorted_date_times[i]), "%Y-%m-%d %H:%M:%S").timestamp()))
            end = int(round(datetime.strptime(str(sorted_date_times[i + 1]), "%Y-%m-%d %H:%M:%S").timestamp()))
            duration += end - start
        avg = duration / (len(sorted_date_times) - 1)
        return avg

    # responsible for counting events from the same event by a given timeunit
    # prints the amount for each event type as a result
    @staticmethod
    def handle_process_events_by_offset():
        events = ImportHandler.handle_import_events()
        processed_events = []

        if events is not None:
            for event in events:
                if event.event_type not in processed_events:
                    processed_events.append(event.event_type)
                    grouped_by_events = ImportHandler.get_grouped_by_events(event.event_type, events)

                    off_set = datetime.now() - timedelta(minutes=5)
                    events_by_offset_counter = 0
                    for e in grouped_by_events:
                        date_time = datetime.strptime(event.date_time_created, '%Y-%m-%dT%H:%M:%Sz')
                        if date_time > off_set:
                            events_by_offset_counter += 1

                    print(str.format("total events for {0} = {1}", e.event_type, events_by_offset_counter))

    # responsible for grouping the same event types by each other and returns a list of the same event types
    @staticmethod
    def get_grouped_by_events(event_type, events):
        grouped_by_events = []
        for event in events:
            if event.event_type == event_type:
                grouped_by_events.append(event)

        return grouped_by_events

    # returns json data
    @staticmethod
    def get_json_data(url):
        try:
            response = urlopen(url)
            return json.loads(response.read())
        except Exception as ex:
            print(ex)
            return None
