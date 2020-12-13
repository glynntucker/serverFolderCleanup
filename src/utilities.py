from collections.abc import Sequence
import pathlib


def directory_is_empty(directory: pathlib.Path) -> bool:
    """Returns True if a directory is empty"""

    return next(directory.iterdir(), None) is None
    

def create_new_pathname(parent_path: pathlib.Path, chosen_name: str) -> pathlib.Path:
    """Creates a new pathname that does not conflict with current pathnames.

    If there is a conflicting pathname, a number will be appended onto the
    chosen_name."""

    new_name = parent_path / chosen_name
    new_name_stem = new_name.stem

    j=0
    while new_name.name.lower() in (p.name.lower() for p in parent_path.iterdir()):
        j += 1
        new_name = parent_path / f"{new_name_stem}_{j}{new_name.suffix}"
    return new_name


def find_duplicates(seq: Sequence) -> set:
    """Find case insensitive duplicates
    
    Adapted from stackoverflow - https://stackoverflow.com/a/9836685"""
    seen = set()
    seen2 = set()
    for item in seq:
        lowercase_item = str(item).lower()
        if lowercase_item in seen:
            seen2.add(item)
        else:
            seen.add(lowercase_item)
    return seen2