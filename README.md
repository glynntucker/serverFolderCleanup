# serverFolderCleanup

serverFolderCleanup can do the following:

- The default behaviour (given just a pathname) renames files and directories with duplicate filenames in the given directory and all its subdirectories recursively. It is case insensitive.  
  `python run.py <path>`
- `-p` flag or `--pattern` argument deletes files matching the provided pattern using regex eg `python run.py <path> -p /.xls` will remove all files whose names contain the pattern `.xls`
- `-c` flag or `--cleanup` argument removes empty directories found in the provided directory and its subdirectories recursively eg `python run.py -c`
- `-n` flag limits its actions to the provided directory only (no subdirectories)
- `-L` flag logs the actions it would've taken without making modifications

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

## If running on PyCharm

1. Open run.py
1. Open 'Edit configurations...' dropdown in top right corner
1. Either edit an existing configuration or create a new one
1. Enter the script path, eg, `/Users/pat/PycharmProjects/serverFolderCleanup/run.py`
1. Enter the arguments,eg, `-c /Volumes/jobs/2020` or  `-p /.bak -L /Volumes/jobs/2020`
1. Enter the working directory, eg, `/Users/pat/PycharmProjects/serverFolderCleanup`
1. Press OK button to save the configuration
1. Run the program using this configuration from the main menu - Run / Run 'config name'
1. Rename the default.log file saved in the working directory to something meaningful - eg `serverFileCleanup deletion log jobs_2020 20210508.log`
1. Copy the log file to the top directory of the tree actioned by the script - eg `jobs/2020`

