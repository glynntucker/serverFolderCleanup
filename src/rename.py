import argparse
import datetime as dt
import os
import pathlib
import sys

from .utilities import (
    directory_is_empty, create_new_pathname
)


LOGFILE_NAME = "rename_log.txt"


def rename_duplicates_in_directory(
    dirpath: pathlib.Path,
    logfile: pathlib.Path = None,
    log_only: bool = False,
    ) -> None:
    """Rename duplicate names within the given directory.
    
    Files that are renamed will be logged. An empty directory will be deleted."""

    if directory_is_empty(dirpath):
        if not log_only:
            dirpath.rmdir()
        if logfile is not None:
            with logfile.open("a") as f:
                f.write(f"Remove {str(dirpath)}\n")
        return

    # no point in creating a logfile in an empty directory -> perform after empty check
    if logfile is None:
        logfile = create_new_pathname(dirpath, LOGFILE_NAME)

    # find duplicates and rename
    completed_paths = set([])
    for path in dirpath.iterdir():
        if path.name.lower() in completed_paths:
            new_path = create_new_pathname(dirpath, path.name.lower())

            if not log_only:
                path.replace(new_path)

            with logfile.open("a") as f:
                f.write(f"Rename {path.name} to {new_path.name}\n")
            completed_paths.add(new_path.name.lower())
        else:
            completed_paths.add(path.name.lower())


def rename_duplicates_in_tree(
    dirpath: pathlib.Path,
    log_only: bool = False
    ) -> None:
    """Rename duplicate names within each subdirectory.

    Files that are renamed will be logged. Empty directories will be deleted."""

    logfile = None
    if not directory_is_empty(dirpath):
        logfile = create_new_pathname(dirpath, LOGFILE_NAME)
        with logfile.open("a") as f:
            f.write(f"\n{'*'*30} {dt.datetime.now()} {'*'*30}\n")

    # topdown false starts walking from the bottom of the tree instead of the top
    # vital for directory renaming
    for root, _, _ in os.walk(dirpath, topdown=False):
        rename_duplicates_in_directory(pathlib.Path(root), logfile=logfile, log_only=log_only)
