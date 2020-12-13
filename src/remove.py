import logging
import os
import pathlib
import re

from .utilities import directory_is_empty


log = logging.getLogger(__name__)
        

def remove_empty_dir(
    dirpath: pathlib.Path,
    log_only: bool = False
    ) -> None:
    """Remove the provided directory if empty"""

    directories_to_check = [dirpath]
    if not directory_is_empty(dirpath):
        directories_to_check = (path for path in dirpath.iterdir() if path.is_dir())

    for directory in directories_to_check:
        if directory_is_empty(directory):
            if log_only:
                log.info("Identified %s as an empty directory to remove", directory)
            else:
                directory.rmdir()
                log.info("Removed %s as it was empty", directory)


def remove_empty_dir_in_tree(
    dirpath: pathlib.Path,
    log_only: bool = False
    ) -> None:
    """Remove empty directories within the given directory tree"""
    # topdown false starts walking from the bottom of the tree instead of the top
    for root, _, _ in os.walk(dirpath, topdown=False):
        remove_empty_dir(pathlib.Path(root), log_only=log_only)


def remove_filepattern_in_dir(
    dirpath: pathlib.Path,
    pattern: str,
    log_only: bool = False,
    ) -> None:
    """Remove files within the given directory if they match the given pattern"""

    regex = re.compile(pattern, re.IGNORECASE)
    
    matches = [path for path in dirpath.iterdir() for m in [regex.search(path.name)] if m]
    for path in matches:
        if log_only:
            log.info("Identified %s for removal as it matches %s", path, pattern)
        else:
            path.unlink()
            log.info("Removed %s as it matched %s", path, pattern)


def remove_filepattern_in_tree(
    dirpath: pathlib.Path,
    pattern: str,
    log_only: bool = False,
    ) -> None:
    """Remove files within the given directory tree if they match the given pattern"""
    # topdown false starts walking from the bottom of the tree instead of the top
    for root, _, _ in os.walk(dirpath, topdown=False):
        remove_filepattern_in_dir(pathlib.Path(root), pattern, log_only=log_only)
