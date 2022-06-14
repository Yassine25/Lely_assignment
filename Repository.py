class Repository:

    def __init__(self, id, name, url):
        self.id = id
        self.name = name
        self.url = url
        self.pull_requests = []
        self.display_repository()

    def display_repository(self):
        print("a new repository is created with id = : ", self.id, ", name = ", self.name, ", url = ", self.url)
