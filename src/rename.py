import argparse
import datetime as dt
import logging
import os
import pathlib
import sys

from .utilities import (
    directory_is_empty, create_new_pathname
)

log = logging.getLogger(__name__)


def rename_duplicates_in_directory(
    dirpath: pathlib.Path,
    log_only: bool = False,
    ) -> None:
    """Rename duplicate names within the given directory"""
    completed_paths = set([])
    for path in dirpath.iterdir():
        if path.name.lower() in completed_paths:
            new_path = create_new_pathname(dirpath, path.name.lower())

            if not log_only:
                path.replace(new_path)
                log.info("Renamed %s to %s", path, new_path)
            else:
                log.info("Identified %s as a duplicate to rename to %s", path, new_path)

            completed_paths.add(new_path.name.lower())
        else:
            completed_paths.add(path.name.lower())


def rename_duplicates_in_tree(
    dirpath: pathlib.Path,
    log_only: bool = False
    ) -> None:
    """Rename duplicate names within each subdirectory"""
    # topdown false starts walking from the bottom of the tree instead of the top
    # vital for directory renaming
    for root, _, _ in os.walk(dirpath, topdown=False):
        rename_duplicates_in_directory(pathlib.Path(root), log_only=log_only)
