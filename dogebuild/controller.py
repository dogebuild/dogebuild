import argparse
import logging
import logging.config
import pkg_resources
import sys
from pathlib import Path
from encodings import utf_8

from dogebuild.common import DOGE_FILE
from dogebuild.doge import DogeFile, DogeFileFactory


def _load_version():
    version = pkg_resources.resource_string("dogebuild", "dogebuild.version")
    version = version.decode(utf_8.getregentry().name).strip()
    return version


class DogeController:

    COMMAND_MAP = {}

    def __init__(self, args):
        self.args = self._parse_args(args)
        self._config_logging()
        self.doge = DogeFileFactory(Path()).create(self.args.file)

    def run(self) -> int:
        return self.args.command(self.doge, self.args.options)

    @staticmethod
    def _parse_args(args) -> argparse.Namespace:
        main_parser = argparse.ArgumentParser(prog="doge", description="")
        main_parser.add_argument("--version", "-V", action="version", version=_load_version())
        main_parser.add_argument("--file", "-f", default=DOGE_FILE, type=Path)
        main_parser.add_argument("command", nargs=1)
        main_parser.add_argument("options", nargs=argparse.REMAINDER)

        main_args = main_parser.parse_args(args)

        if main_args.command[0] in DogeController.COMMAND_MAP.keys():
            main_args.command = DogeController.COMMAND_MAP[main_args.command[0]]
        else:
            main_args.options = main_args.command + main_args.options
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
                    "colored": {"()": "colorlog.ColoredFormatter", "format": console_format, "style": "{",},
                },
                "handlers": {
                    "console": {
                        "class": "logging.StreamHandler",
                        "formatter": "colored",
                        "level": console_level,
                        "stream": sys.stdout,
                    },
                },
                "loggers": {"": {"handlers": ["console"], "level": console_level,},},
            }
        )
