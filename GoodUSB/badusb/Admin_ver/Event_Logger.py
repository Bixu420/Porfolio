import logging
from logging.handlers import NTEventLogHandler
import win32evtlogutil

class EventLogger:
    def __init__(self, app_name="GoodUSB", log_level=logging.INFO):
        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(log_level)
        self.setup_event_log_handler(app_name, log_level)

    def setup_event_log_handler(self, app_name, log_level):
        # Create an NTEventLogHandler
        event_log_handler = NTEventLogHandler(app_name)
        event_log_handler.setLevel(log_level)

        # Formatter for the logs
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        event_log_handler.setFormatter(formatter)

        # Adding the handler to the logger
        self.logger.addHandler(event_log_handler)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)
