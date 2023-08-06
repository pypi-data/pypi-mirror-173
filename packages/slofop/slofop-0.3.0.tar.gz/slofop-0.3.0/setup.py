# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slofop']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.6.0,<13.0.0']

setup_kwargs = {
    'name': 'slofop',
    'version': '0.3.0',
    'description': 'A relatively simple and good-looking logging library for Python, with relatively good customisability.',
    'long_description': '# slofop\n\n## The hell is this name?\n\nThe name \'slofop\' stands for \'**S**imple **lo**gger **fo**r **P**ython\'.\n\n## Showcase\n\nAfter running the example.py file, ...\n\n - ...the terminal output is\n \n![Example script output](readme_assets/example_screenshot.png)\n\n - ...the content of \'test.log\' is\n```log\nDEBUG      MainThread   25.10.2022 17:00:49 CEST: {\n                                                      "__name__": "__main__",\n                                                      "__doc__": null,\n                                                      "__package__": null,\n                                                      "__loader__": "<_frozen_importlib_external.SourceFileLoader object at 0x7fab7107d510>",\n                                                      "__spec__": null,\n                                                      "__annotations__": {},\n                                                      "__builtins__": "<module \'builtins\' (built-in)>",\n                                                      "__file__": "/run/media/paddecraft/4EE0F299E0F2870D/Dev/PythonScripting/slofop/example.py",\n                                                      "__cached__": null,\n                                                      "filesystem_handlers": "<module \'slofop.filesystem_handlers\' from \'/run/media/paddecraft/4EE0F299E0F2870D/Dev/PythonScripting/slofop/slofop/filesystem_handlers.py\'>",\n                                                      "util": "<module \'slofop.util\' from \'/run/media/paddecraft/4EE0F299E0F2870D/Dev/PythonScripting/slofop/slofop/util.py\'>",\n                                                      "slofop": "<module \'slofop.slofop\' from \'/run/media/paddecraft/4EE0F299E0F2870D/Dev/PythonScripting/slofop/slofop/slofop.py\'>",\n                                                      "Logger": "<class \'slofop.slofop.Logger\'>",\n                                                      "LoggingLevel": "<enum \'LoggingLevel\'>",\n                                                      "os": "<module \'os\' from \'/usr/lib/python3.10/os.py\'>",\n                                                      "time": "<module \'time\' (built-in)>",\n                                                      "atexit": "<module \'atexit\' (built-in)>",\n                                                      "pathlib": "<module \'pathlib\' from \'/usr/lib/python3.10/pathlib.py\'>",\n                                                      "threading": "<module \'threading\' from \'/usr/lib/python3.10/threading.py\'>",\n                                                      "NoneType": "<class \'NoneType\'>",\n                                                      "BaseFilesystemHandler": "<class \'slofop.filesystem_handlers.BaseFilesystemHandler\'>",\n                                                      "TimedFilesystemHandler": "<class \'slofop.filesystem_handlers.TimedFilesystemHandler\'>",\n                                                      "log": "Logger {colors: {DEBUG: [#c7dcff]#c7dcff[/#c7dcff], INFO: [#3caae6]#3caae6[/#3caae6], WARNING: [#e0c528]#e0c528[/#e0c528], ERROR: [#e61c5b]#e61c5b[/#e61c5b], CRITICAL: [#f50a19]#f50a19[/#f50a19]}, filesystem_handler: FilesystemHandler(BaseFilesystemHandler), level: LoggingLevel.DEBUG, file: ./test.log}"\n                                                  }\nINFO       MainThread   25.10.2022 17:00:49 CEST: Info\nWARNING    MainThread   25.10.2022 17:00:49 CEST: Warn\nERROR      MainThread   25.10.2022 17:00:49 CEST: Error\nCRITICAL   MainThread   25.10.2022 17:00:49 CEST: Critical\nDEBUG      Thread-1     25.10.2022 17:00:49 CEST: Running in Thread-1 (testThread)\nINFO       Thread-1     25.10.2022 17:00:49 CEST: Thread running time 1\nDEBUG      Thread-1     25.10.2022 17:00:50 CEST: Running in Thread-1 (testThread)\nINFO       Thread-1     25.10.2022 17:00:50 CEST: Thread running time 2\nDEBUG      Thread-1     25.10.2022 17:00:51 CEST: Running in Thread-1 (testThread)\nINFO       Thread-1     25.10.2022 17:00:51 CEST: Thread running time 3\nDEBUG      Thread-1     25.10.2022 17:00:52 CEST: Running in Thread-1 (testThread)\nINFO       Thread-1     25.10.2022 17:00:52 CEST: Thread running time 4\n```\n\n## Class tree\n\n```py\nclass slofop.Logger:\n    def __init__(\n        self,\n        logfile_path: str = None,\n        show_threads: bool = True,\n        level: LoggingLevel = LoggingLevel.INFO,\n        colors: ColorFormat = {\n            LoggingLevel.DEBUG: "#c7dcff",\n            LoggingLevel.INFO: "#3caae6",\n            LoggingLevel.WARNING: "#e0c528",\n            LoggingLevel.ERROR: "#e61c5b",\n            LoggingLevel.CRITICAL: "#f50a19",\n        },\n        time_format_file: str = "%d.%m.%Y %H:%M:%S",\n        time_format_console: str = "%H:%M:%S",\n        filesystem_handler: Type[BaseFilesystemHandler] = BaseFilesystemHandler(\n        ),\n    ) -> None\n\n    def debug(*elements) -> None\n    def info(*elements) -> None\n    def warn(*elements) -> None\n    def error(*elements) -> None\n    def critical(*elements) -> None\n```',
    'author': 'PaddeCraft',
    'author_email': 'paddecraft@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/PaddeCraft/slofop',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
