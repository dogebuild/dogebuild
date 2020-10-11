import argparse
import logging
import logging.config
import sys
from encodings import utf_8
from pathlib import Path

import pkg_resources

from dogebuild.common import DOGE_FILE
from dogebuild.dogefile import DogeFile, DogeFileFactory


def _load_version():
    version = pkg_resources.resource_string("dogebuild", "dogebuild.version")
    version = version.decode(utf_8.getregentry().name).strip()
    return version


class DogeController:

    COMMAND_MAP = {}

    def __init__(self, args):
        self.args = self._parse_args(args)
        self._config_logging()

    def run(self) -> int:
        self.doge = DogeFileFactory(Path()).create(self.args.file)
        if self.args.doge_task:
            params = self.doge.extract_parameters(self.args.parameters)
            tasks = params.tasks
            tasks_params = {**params.__dict__}
            tasks_params.pop("tasks")
            return self.doge.run_tasks(tasks, tasks_params)
        else:
            return self.args.command(self.doge, self.args.options)

    @staticmethod
    def _parse_args(args) -> argparse.Namespace:
        main_parser = argparse.ArgumentParser(prog="doge", description="")
        main_parser.add_argument("--version", "-V", action="version", version=_load_version())
        main_parser.add_argument("--file", "-f", default=DOGE_FILE, type=Path)
        main_parser.add_argument("parameters", nargs=argparse.REMAINDER)

        main_args = main_parser.parse_args(args)

        if main_args.parameters[0] in DogeController.COMMAND_MAP.keys():
            main_args.doge_task = False
            main_args.command = DogeController.COMMAND_MAP[main_args.parameters[0]]
            main_args.parameters = main_args.parameters[1:]
        else:
            main_args.doge_task = True
            main_args.command = DogeFile.run_tasks

        return main_args

    @staticmethod
    def _config_logging():
        console_format = "{log_color}{message}{reset}"
        console_level = "DEBUG"

        logging.config.dictConfig(
            {
                "version": 1,
                "formatters": {
                    "colored": {
                        "()": "colorlog.ColoredFormatter",
                        "format": console_format,
                        "style": "{",
                    },
                },
                "handlers": {
                    "console": {
                        "class": "logging.StreamHandler",
                        "formatter": "colored",
                        "level": console_level,
                        "stream": sys.stdout,
                    },
                },
                "loggers": {
                    "": {
                        "handlers": ["console"],
                        "level": console_level,
                    },
                },
            }
        )
