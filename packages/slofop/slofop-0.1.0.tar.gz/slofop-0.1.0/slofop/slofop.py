from typing import TypedDict, Type
from textwrap import wrap
from rich import print
from enum import Enum

from .filesystem_handlers import BaseFilesystemHandler
from .util import *

import threading
import datetime
import json
import re


class LoggingLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4


class ColorFormat(TypedDict):
    LoggingLevel.DEBUG: str
    LoggingLevel.INFO: str
    LoggingLevel.WARNING: str
    LoggingLevel.ERROR: str
    LoggingLevel.CRITICAL: str


class Logger:
    def __init__(
        self,
        logfile_path: str = None,
        show_threads: bool = True,
        level: LoggingLevel = LoggingLevel.INFO,
        colors: ColorFormat = {
            LoggingLevel.DEBUG: "#c7dcff",
            LoggingLevel.INFO: "#3caae6",
            LoggingLevel.WARNING: "#e0c528",
            LoggingLevel.ERROR: "#e61c5b",
            LoggingLevel.CRITICAL: "#f50a19",
        },
        time_format_file: str = "%d.%m.%Y %H:%M:%S",
        time_format_console: str = "%H:%M:%S",
        filesystem_handler: Type[BaseFilesystemHandler] = BaseFilesystemHandler(
        ),
    ) -> None:
        """Initialize a logger

        Args:
            logfile_path (str, optional): The path to the logfile. If none, no logs will be written to the filesystem. Defaults to None.
            show_threads (bool, optional): Show the threads in the console. Defaults to True.
            level (LoggingLevel, optional): The minimum logging level to be displayed in the console. Defaults to LoggingLevel.INFO.
            colors (TypedDict, optional): The colors to use for the console. Supports all colors rich is capable of. Defaults to { LoggingLevel.DEBUG: "#c7dcff", LoggingLevel.INFO: "#3caae6", LoggingLevel.WARNING: "#e0c528", LoggingLevel.ERROR: "#e61c5b", LoggingLevel.CRITICAL: "#f50a19", }.
            time_format_file (str, optional): The time format that is present in the log file. Defaults to "%d.%m.%Y %H:%M:%S".
            time_format_console (str, optional): The time format that is present in the console. Defaults to "%H:%M:%S".
            filesystem_handler (Type[BaseFilesystemHandler], optional): The filesystem handler. Defaults to BaseFilesystemHandler().
        """
        self.logfile = logfile_path
        self.show_threads = show_threads
        self.log_level = level
        self.colors = colors
        self.time_format_file = time_format_file
        self.time_format_console = time_format_console

        # File system handler
        self.filesystem_handler = filesystem_handler
        status, msg = self.filesystem_handler.init(logfile_path)
        if status:
            self.__log(LoggingLevel[status], [msg])

    def __log(self, level: LoggingLevel, elements) -> None:
        # ---------------------------------------------------------------------------- #
        #                                   Get time                                   #
        # ---------------------------------------------------------------------------- #
        # https://stackoverflow.com/a/39079819
        timezone = str(datetime.datetime.now(
            datetime.timezone.utc).astimezone().tzinfo)
        timeStrConsole = (
            datetime.datetime.now().strftime(self.time_format_console) + " " + timezone
        )
        timeStrFile = (
            datetime.datetime.now().strftime(self.time_format_file) + " " + timezone
        )
        # ---------------------------------------------------------------------------- #
        #                                  Get thread                                  #
        # ---------------------------------------------------------------------------- #
        thread = threading.current_thread().name
        if thread.split("-")[0] == "Thread":
            threadStr = "Thr" + thread.split("-")[1].split(" ")[0]
        elif thread == "MainThread":
            threadStr = "MainThr"
        else:
            threadStr = thread

        # ---------------------------------------------------------------------------- #
        #                               'Render' elements                              #
        # ---------------------------------------------------------------------------- #
        elementLines = []
        for e in elements:
            if type(e) in [list, dict, tuple]:
                elementLines += json.dumps(
                    replacePythonObjInJsonLike(e), indent=4
                ).split("\n")
            else:
                elementLines += wrap(str(e), width=35)

        # ---------------------------------------------------------------------------- #
        #                          Write to file if requested                          #
        # ---------------------------------------------------------------------------- #
        if self.logfile:
            ln = f"{level.name: <10} {thread.split(' ')[0]: <12} {timeStrFile}: "
            space = len(ln)
            lines = []
            for i, e in enumerate(elementLines):
                if i == 0:
                    lines.append(ln + e)
                else:
                    lines.append((" " * space) + e)

            self.filesystem_handler.write("\n".join(lines) + "\n")

        # ---------------------------------------------------------------------------- #
        #                   Print to console if level is high enough                   #
        # ---------------------------------------------------------------------------- #
        if level.value >= self.log_level.value:
            consoleThreadStr = (
                f"{threadStr: <8} " if self.show_threads else "")
            lvl = f"[{self.colors[level]}]{level.name: <10}[/{self.colors[level]}]"
            ln = f"[bold]{lvl} {consoleThreadStr}{timeStrConsole}:[/bold] "
            space = len(re.sub(r"\[[^\]]+\]", "", ln))
            lines = []
            for i, e in enumerate(elementLines):
                if i == 0:
                    lines.append(ln + e)
                else:
                    lines.append((" " * space) + e)
            print("\n".join(lines))

    def debug(self, *elements) -> None:
        self.__log(LoggingLevel.DEBUG, elements)

    def info(self, *elements) -> None:
        self.__log(LoggingLevel.INFO, elements)

    def warn(self, *elements) -> None:
        self.__log(LoggingLevel.WARNING, elements)

    def error(self, *elements) -> None:
        self.__log(LoggingLevel.ERROR, elements)

    def critical(self, *elements) -> None:
        self.__log(LoggingLevel.CRITICAL, elements)

    def __repr__(self) -> str:
        colors = {}
        for key, value in self.colors.items():
            colors[key.name] = f"[{value}]" + value + f"[/{value}]"

        cfg = {"colors": colors, "filesystem_handler": str(self.filesystem_handler),
               "level": str(self.log_level), "file": self.logfile}
        return "Logger " + json.dumps(cfg).replace("\"", "")
