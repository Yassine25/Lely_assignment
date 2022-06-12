class PullRequest:

    def __init__(self, id, number, date_time):
        self.id = id
        self.number = number
        self.date_time = date_time
        self.display_pull_request()

    def display_pull_request(self):
        print("a new pull request is created with id = : ", self.id, ", name = ", self.number, "datetime ",
              self.date_time)
