# Rename Duplicates

Rename Duplicates can do the following:

- The default behaviour (given just a pathname) renames all the files and directories with duplicate filenames in the given directory and all its subdirectories recursively. It is case insensitive.  
  `python run.py <path>`
- When used with the `-p` flag or `--pattern` argument, it will delete the files it finds matching the provided pattern. eg `python run.py <path> -p .xls` will remove all files whose names contain the pattern `.xls`
- When used with the `-c` flag or `--cleanup` argument, it will remove any empty directories it finds within the provided directory and its subdirectories recursively.  
  `python run.py -c`
- Given the `-n` flag, the program will limit its actions to the provided directory only (no subdirectories)
- Given the `-L` flag, the program will log the actions it would've taken without making modifications

Files that are renamed are done so by appending '_x' to their name, where x is an integer.

This program exists for my dad who discovered, upon trying to move files from an old harddrive, that he had files with duplicate names. He needed a way to rename the duplicates so he could copy them to the new filesystem. I occassionally add on more functionality as he requests.

## Quickstart

To run the program:

- `python rename.py <path>` (use -h for further help).

To run the tests:

1. `pip install pytest`
2. run `pytest` from the rename_duplicates directory

To type check:

1. `pip install mypy`
1. Run `mypy .` from the rename_duplicates directory

This project requires Python 3.6 using only standard libraries to run. Development work may require pytest and mypy.
