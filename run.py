import argparse
import logging
from logging.config import dictConfig
import os
import pathlib
import sys

from src.rename import rename_duplicates_in_directory, rename_duplicates_in_tree

def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Rename any duplicate file or directory names in the given path."
                    " This is achieved by appending '_x' where x is an integer."
                    " Additionally, any empty directories are removed."
    )

    parser.add_argument(
        'path',
        help="Rename all duplicate names in the directory of the given path "
             "as well as those in its subdirectories (unless --nosubs is provided). "
             "Additionally, remove all empty directories."
    )

    parser.add_argument(
        '--nosubs',
        action="store_true",
        help='Use this option to deduplicate/remove items in the given directory only '
             '(ie not in any of its sub-directories)'
    )

    parser.add_argument(
        '-L', '--logonly',
        action="store_true",
        help='Use this option to log only without making actual changes '
             '(except creating the log file)',
    )

    parser.add_argument(
        '-p', '--pattern',
        type=str,
        default=None,
        help='Use this option in conjunction with a regular expression to delete matching files '
             'This pattern is case insensitive.'
    )

    return parser.parse_args(args)


class LevelFilter():
    """A filter class for logging one level only"""
    def __init__(self, level):
        self.__level = level
    
    def filter(self, log_record):
        return log_record.levelno == self.__level


# set up logging
default_logfile_name = "default.log"

logging_config = dict(
    version = 1,
    disable_existing_loggers = False,
    filters = {
        "info_only": {
            "()": "__main__.LevelFilter",
            "level": logging.INFO
        }
    },
    formatters = {
        "info_formatter": {"format": "[%(levelname)s] %(asctime)s | %(message)s"},
        "console_formatter": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"}
    },
    handlers = {
        "info_handler": {"class": "logging.FileHandler",
                         "formatter": "info_formatter",
                         "level": logging.INFO,
                         "filename": default_logfile_name,
                         "filters": ["info_only"]},
        "console_handler": {"class": "logging.StreamHandler",
                            "formatter": "console_formatter",
                            "level": logging.DEBUG,
                            "stream": "ext://sys.stdout"}         
    },
    root = {
        "handlers": ["info_handler", "console_handler"],
        "level": logging.DEBUG,
    },
)
dictConfig(logging_config)
log = logging.getLogger(__name__)

log.debug("Log saved in %s\n", pathlib.Path(os.getcwd(), default_logfile_name))

# parse arguments
parsed_args = parse_args(sys.argv[1:])
path = pathlib.Path(parsed_args.path).resolve()

if path.exists() and path.is_dir():
    if parsed_args.nosubs:
        log.info("**** Looking for all duplicates in %s only", path)
        rename_duplicates_in_directory(path, log_only=parsed_args.logonly)
    else:
        log.info("**** Looking for all duplicates in %s and its subdirectories", path)
        rename_duplicates_in_tree(path, log_only=parsed_args.logonly)
else:
    log.error("%s is not a valid directory", path)

log.info("END\n")
