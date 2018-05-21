# Rename Duplicates

Rename Duplicates renames all the files and directories with duplicate filenames in the given directory and all its subdirectories. It is case insensitive.

The files are renamed by appending '_x' to their name where x is an integer.

This program exists for my dad who discovered, upon trying to move files from an old harddrive, that he had files with duplicate names. He needed a way to rename the duplicates so he could copy them to the new filesystem.

To run the program either:
* run `python gui.py` for a simple graphical interface, or
* run `python rename.py <path>` (use -h for further help)

To run the tests:
* `pip install pytest`
* run `pytest` from the rename_dupes directory

This project is written in Python3 using only standard libraries (except for testing).