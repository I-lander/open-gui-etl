import os
import sys
from datetime import datetime


class LoggerDualOutput:
    def __init__(self, logfile):
        self.terminal = sys.__stdout__
        self.logfile = logfile

    def write(self, message):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        if message == "\n":
            timestamp = ""
        self.terminal.write(timestamp + message)
        self.logfile.write(timestamp + message)
        self.flush()

    def flush(self):
        self.terminal.flush()
        self.logfile.flush()


def init_logs(log_file_name: str):
    logs_dir = "logs"
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    os.makedirs(logs_dir, exist_ok=True)
    full_log_file_name = f"{log_file_name}-{timestamp}.log"
    log_filename = os.path.join(logs_dir, full_log_file_name)

    log_file = open(log_filename, "w", encoding="utf-8")
    sys.stdout = LoggerDualOutput(log_file)
    sys.stderr = LoggerDualOutput(log_file)
