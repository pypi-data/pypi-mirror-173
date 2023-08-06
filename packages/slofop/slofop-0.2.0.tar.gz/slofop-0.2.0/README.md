# slofop

## The hell is this name?

The name 'slofop' stands for '**S**imple **lo**gger **fo**r **P**ython'.

## Showcase

After running the example.py file, ...

 - ...the terminal output is
 
![Example script output](readme_assets/example_screenshot.png)

 - ...the content of 'test.log' is
```log
DEBUG      MainThread   25.10.2022 17:00:49 CEST: {
                                                      "__name__": "__main__",
                                                      "__doc__": null,
                                                      "__package__": null,
                                                      "__loader__": "<_frozen_importlib_external.SourceFileLoader object at 0x7fab7107d510>",
                                                      "__spec__": null,
                                                      "__annotations__": {},
                                                      "__builtins__": "<module 'builtins' (built-in)>",
                                                      "__file__": "/run/media/paddecraft/4EE0F299E0F2870D/Dev/PythonScripting/slofop/example.py",
                                                      "__cached__": null,
                                                      "filesystem_handlers": "<module 'slofop.filesystem_handlers' from '/run/media/paddecraft/4EE0F299E0F2870D/Dev/PythonScripting/slofop/slofop/filesystem_handlers.py'>",
                                                      "util": "<module 'slofop.util' from '/run/media/paddecraft/4EE0F299E0F2870D/Dev/PythonScripting/slofop/slofop/util.py'>",
                                                      "slofop": "<module 'slofop.slofop' from '/run/media/paddecraft/4EE0F299E0F2870D/Dev/PythonScripting/slofop/slofop/slofop.py'>",
                                                      "Logger": "<class 'slofop.slofop.Logger'>",
                                                      "LoggingLevel": "<enum 'LoggingLevel'>",
                                                      "os": "<module 'os' from '/usr/lib/python3.10/os.py'>",
                                                      "time": "<module 'time' (built-in)>",
                                                      "atexit": "<module 'atexit' (built-in)>",
                                                      "pathlib": "<module 'pathlib' from '/usr/lib/python3.10/pathlib.py'>",
                                                      "threading": "<module 'threading' from '/usr/lib/python3.10/threading.py'>",
                                                      "NoneType": "<class 'NoneType'>",
                                                      "BaseFilesystemHandler": "<class 'slofop.filesystem_handlers.BaseFilesystemHandler'>",
                                                      "TimedFilesystemHandler": "<class 'slofop.filesystem_handlers.TimedFilesystemHandler'>",
                                                      "log": "Logger {colors: {DEBUG: [#c7dcff]#c7dcff[/#c7dcff], INFO: [#3caae6]#3caae6[/#3caae6], WARNING: [#e0c528]#e0c528[/#e0c528], ERROR: [#e61c5b]#e61c5b[/#e61c5b], CRITICAL: [#f50a19]#f50a19[/#f50a19]}, filesystem_handler: FilesystemHandler(BaseFilesystemHandler), level: LoggingLevel.DEBUG, file: ./test.log}"
                                                  }
INFO       MainThread   25.10.2022 17:00:49 CEST: Info
WARNING    MainThread   25.10.2022 17:00:49 CEST: Warn
ERROR      MainThread   25.10.2022 17:00:49 CEST: Error
CRITICAL   MainThread   25.10.2022 17:00:49 CEST: Critical
DEBUG      Thread-1     25.10.2022 17:00:49 CEST: Running in Thread-1 (testThread)
INFO       Thread-1     25.10.2022 17:00:49 CEST: Thread running time 1
DEBUG      Thread-1     25.10.2022 17:00:50 CEST: Running in Thread-1 (testThread)
INFO       Thread-1     25.10.2022 17:00:50 CEST: Thread running time 2
DEBUG      Thread-1     25.10.2022 17:00:51 CEST: Running in Thread-1 (testThread)
INFO       Thread-1     25.10.2022 17:00:51 CEST: Thread running time 3
DEBUG      Thread-1     25.10.2022 17:00:52 CEST: Running in Thread-1 (testThread)
INFO       Thread-1     25.10.2022 17:00:52 CEST: Thread running time 4
```

## Class tree

```py
class slofop.Logger:
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
    ) -> None

    def debug(*elements) -> None
    def info(*elements) -> None
    def warn(*elements) -> None
    def error(*elements) -> None
    def critical(*elements) -> None
```