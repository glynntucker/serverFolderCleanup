import argparse


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Rename any duplicate file or directory names in the given path. "
                    "This is achieved by appending '_x' where x is an integer. "
    )

    parser.add_argument(
        'path',
        help="Rename all duplicate names in the directory of the given path "
             "as well as those in its subdirectories. "
    )

    parser.add_argument(
        '-n', '--nosubs',
        action="store_true",
        help="Use this option to deduplicate/remove items in the given directory only "
             "(eg `python run.py <pathname> --nosubs`)"
    )

    parser.add_argument(
        '-L', '--logonly',
        action="store_true",
        help="Use this option to log only without making actual changes "
             "(eg `python run.py <pathname> -L`)"
    )

    parser.add_argument(
        '-p', '--pattern',
        type=str,
        default=None,
        help="Use this option in conjunction with a regular expression to REMOVE matching files. "
             "Can be used in conjunction with --nosubs and/or --logonly"
             "(eg `python run.py <pathname> -r .xls` to recursively remove all .xls files in the given pathname)"
    )

    parser.add_argument(
        '-c', '--cleanup',
        action="store_true",
        help="Use this option to remove (clean up) all empty directories. "
             "Can be used in conjunction with --nosubs and/or --logonly "
             "(eg `python run.py <pathname> -c`)"
    )

    return parser.parse_args(args)