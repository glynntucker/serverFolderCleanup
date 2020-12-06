import argparse
import os
import pathlib
import sys


def rename_dupes_in_directory(dirpath, log_only=False):
    if next(dirpath.iterdir(), None) is None:
        # directory is empty
        dirpath.rmdir
        return

    entries = sorted(dirpath.iterdir())
    checked = set([x.name.lower() for x in entries])
    for i, entry in enumerate(entries[1:]):
        if entry.name.lower() == entries[i].name.lower():
            j = 0
            new_name = "{}_{}{}".format(entry.stem, j, entry.suffix)
            while new_name.lower() in checked:
                j += 1
                new_name = "{}_{}{}".format(entry.stem, j, entry.suffix)

            new_path = entry.parent / new_name
            print("Renaming {} as {}".format(entry.name, new_path.name))
            entry.replace(new_path)
            checked.add(new_path.name.lower())


def rename_duplicates_in_tree(dirpath):
    # topdown false starts walking from the bottom of the tree instead of the top
    # vital for directory renaming
    for root, _, _ in os.walk(dirpath, topdown=False):
        rename_dupes_in_directory(pathlib.Path(root))


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
            rename_dupes_in_directory(path)
        else:
            print("Renaming all duplicates in '{}' and its subdirectories".format(path))
            rename_duplicates_in_tree(path)
    else:
        print("{} is not a valid directory".format(path))
