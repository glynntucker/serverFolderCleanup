import argparse
import os
import sys


def rename_dupes_in_directory(dirpath):
    entries = sorted(os.listdir(dirpath), key=lambda s: s.lower())
    if not entries:
        os.rmdir(dirpath)
        return

    checked = set([x.lower() for x in entries])
    for i, entry in enumerate(entries[1:]):
        if entry.lower() == entries[i].lower():
            file_to_rename = os.path.join(dirpath, entry)
            j = 0

            head, tail = os.path.splitext(entry)
            entry = "{}_{}{}".format(head, j, tail)
            while entry.lower() in checked:
                j += 1
                entry = "{}_{}{}".format(head, j, tail)

            new_filename = os.path.join(dirpath, entry)
            print("Renaming {} as {}".format(file_to_rename, new_filename))
            os.replace(file_to_rename, new_filename)
            checked.add(entry.lower())


def rename_duplicates_in_tree(dirpath):
    # topdown false starts walking from the bottom of the tree instead of the top
    # vital for directory renaming
    for root, _, _ in os.walk(dirpath, topdown=False):
        rename_dupes_in_directory(root)


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Rename any duplicate file or directory names in the given path."
                    " This is achieved by appending '_x' where x is an integer"
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

    if os.path.exists(parsed_args.path):
        if parsed_args.nosubs:
            print("Renaming all duplicates in '{}' directory only".format(parsed_args.path))
            rename_dupes_in_directory(parsed_args.path)
        else:
            print("Renaming all duplicates in '{}' and its subdirectories".format(parsed_args.path))
            rename_duplicates_in_tree(parsed_args.path)
    else:
        print("{} is not a valid path".format(parsed_args.path))
