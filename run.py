import logging
from logging.config import dictConfig
import os
import pathlib
import sys

from src.rename import rename_duplicates_in_directory, rename_duplicates_in_tree
from src.remove import (
    remove_empty_dir, remove_empty_dir_in_tree, remove_filepattern_in_dir,
    remove_filepattern_in_tree
)
from src.parseargs import parse_args


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
parsed = parse_args(sys.argv[1:])
path = pathlib.Path(parsed.path).resolve()

if path.exists() and path.is_dir():
    msg_start = "****"

    if parsed.cleanup:
        msg_action = "Looking for empty directories in"
        if parsed.nosubs:
            log.info("%s %s %s only", msg_start, msg_action, path)
            remove_empty_dir(path, log_only=parsed.logonly)
        else:
            log.info("%s %s %s and its subdirectories recursively", msg_start, msg_action, path) 
            remove_empty_dir_in_tree(path, log_only=parsed.logonly)
    
    elif parsed.pattern:
        msg_action = "Looking for files that match the pattern"
        if parsed.nosubs:
            log.info("%s %s %s in %s only",
                     msg_start, msg_action, parsed.pattern, path)
            remove_filepattern_in_dir(path, parsed.pattern, log_only=parsed.logonly)
        else:
            log.info("%s %s %s in %s and its subdirectories recursively",
                     msg_start, msg_action, parsed.pattern, path)
            remove_filepattern_in_tree(path, parsed.pattern, log_only=parsed.logonly)
    else:
        msg_action = "Looking for all duplicates in"
        if parsed.nosubs:
            log.info("%s %s %s in %s only",
                     msg_start, msg_action, parsed.pattern, path)
            rename_duplicates_in_directory(path, log_only=parsed.logonly)
        else:
            log.info("%s %s %s in %s and its subdirectories recursively",
                     msg_start, msg_action, parsed.pattern, path)
            rename_duplicates_in_tree(path, log_only=parsed.logonly)

else:
    log.error("%s is not a valid directory", path)

log.info("END\n")
