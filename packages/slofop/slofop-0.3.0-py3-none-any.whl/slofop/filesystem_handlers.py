import os
import time
import atexit
import pathlib
import threading

from types import NoneType


class BaseFilesystemHandler:
    def __init__(self) -> None:
        pass

    def init(self, path: str | NoneType) -> None | str:
        if not path:
            self.enabled = False
            return None, None
        self.logfile = path
        dir = os.path.split(path)[0]
        try:
            pathlib.Path(dir).mkdir(parents=True, exist_ok=True)
            self.enabled = True
            return None, None
        except PermissionError:
            self.enabled = False
            return (
                "WARNING",
                "Not enough permission to create root directory for the logs, logs will not be written to disk.",
            )

    def write(self, log: str):
        if self.enabled:
            with open(self.logfile, "a+", encoding="UTF-8") as lf:
                lf.write(log)

    def __repr__(self) -> str:
        return f"FilesystemHandler({self.__class__.__name__})"


class TimedFilesystemHandler(BaseFilesystemHandler):
    def __init__(self, interval: int = 1) -> None:
        """Write logs to disk every x seconds

        Args:
            interval (int, optional): The interval between writes. Defaults to 1.
        """
        self.logs = []
        self.interval = interval
        threading.Thread(target=self.thread, args=(self,))
        atexit.register(self.__write)

    def __write(self):
        current_logs = []
        [self.logs, current_logs] = [current_logs, self.logs]
        if self.enabled:
            with open(self.logfile, "a+", encoding="UTF-8") as lf:
                lf.write("".join(current_logs))

    def thread(self):
        while True:
            self.__write()
            time.sleep(self.interval)

    def write(self, log: str):
        self.logs.append(log)
