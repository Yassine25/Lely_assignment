
class Event:

    def __init__(self, event_type, event_id, date_time_created):
        self.event_type = event_type
        self.event_id = event_id
        self.date_time_created = date_time_created

    def display_event(self):
        print("Event type created with type = ", self.event_type, "id = ", self.event_id, " datetime = ",
              self.date_time_created)