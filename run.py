import argparse
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


if __name__ == "__main__":
    parsed_args = parse_args(sys.argv[1:])
    path = pathlib.Path(parsed_args.path).resolve()

    if path.exists() and path.is_dir():
        if parsed_args.nosubs:
            print(f"Renaming all duplicates in '{path}' directory only unless empty, then remove '{path}'")
            rename_duplicates_in_directory(path, log_only=parsed_args.logonly)
        else:
            print(f"Renaming all duplicates in '{path}' and its subdirectories and removing empty directories")
            rename_duplicates_in_tree(path, log_only=parsed_args.logonly)
    else:
        print(f"{path} is not a valid directory")
