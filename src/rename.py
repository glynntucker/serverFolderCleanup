import argparse
import os
import pathlib
# import sys

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
    
    Files that are renamed will be logged."""

    if directory_is_empty(dirpath):
        if not log_only:
            dirpath.rmdir()
            if logfile is not None:
                with logfile.open("a") as f:
                    f.write(f"Removed {str(dirpath)}\n")
        else:
            if logfile is not None:
                with logfile.open("a") as f:
                    f.write(f"Will remove {str(dirpath)}\n")
        return

    # no point in creating a logfile in an empty directory -> perform after empty check
    if logfile is None:
        logfile = create_new_pathname(dirpath, LOGFILE_NAME)

    # find duplicates and rename
    completed_paths = set([])
    for path in dirpath.iterdir():
        if path.name.lower() in completed_paths:
            new_path = create_new_pathname(dirpath, path.name.lower())
            path.replace(new_path)

            with logfile.open("a") as f:
                f.write(f"Renamed {path.name} to {new_path.name}\n")
            completed_paths.add(new_path.name.lower())
        else:
            completed_paths.add(path.name.lower())


def rename_duplicates_in_tree(dirpath: pathlib.Path):
    logfile = create_new_pathname(dirpath, LOGFILE_NAME)
    # topdown false starts walking from the bottom of the tree instead of the top
    # vital for directory renaming
    for root, _, _ in os.walk(dirpath, topdown=False):
        rename_duplicates_in_directory(pathlib.Path(root), logfile=logfile)


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Rename any duplicate file or directory names in the given path."
                    " This is achieved by appending '_x' where x is an integer."
    )

    parser.add_argument(
        'path',
        help="Rename all duplicate names in the directory of the given path "
             "as well as those in its subdirectories (unless --nosubs is provided)"
    )

    parser.add_argument(
        '--nosubs',
        action="store_true",
        help='Use this option to deduplicate items in the given directory only '
             '(ie not in any of its sub-directories)'
    )

    return parser.parse_args(args)


if __name__ == "__main__":
    parsed_args = parse_args(sys.argv[1:])
    path = pathlib.Path(parsed_args.path).resolve()

    if path.exists() and path.is_dir():
        if parsed_args.nosubs:
            print("Renaming all duplicates in '{}' directory only".format(path))
            rename_duplicates_in_directory(path)
        else:
            print("Renaming all duplicates in '{}' and its subdirectories".format(path))
            rename_duplicates_in_tree(path)
    else:
        print("{} is not a valid directory".format(path))
