from datetime import datetime, timedelta

from ImportHandler import ImportHandler


class Main:
    ImportHandler.handle_import_repositories()
    ImportHandler.handle_process_events_by_offset(datetime.now() - timedelta(minutes=10))
    ImportHandler.handle_process_events_by_offset(datetime.now() - timedelta(minutes=300))

