import logging
import pathlib
import re

from .utilities import directory_is_empty


log = logging.getLogger(__name__)
       

def remove_empty_dir(
    dirpath: pathlib.Path,
    log_only: bool = False
    ) -> bool:
    """Remove the provided directory if empty"""
    if directory_is_empty(dirpath):
        if log_only:
            log.info("Identified %s as an empty directory to remove", dirpath)
        else:
            dirpath.rmdir()
            log.info("Removed %s as it was empty", dirpath)
            