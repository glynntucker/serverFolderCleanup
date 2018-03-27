import os
from collections import Counter


def rename_dupes_in_directory(dirpath):
    entries = Counter(os.listdir(dirpath))
    duplicates = {key: value for (key, value) in entries.items() if value > 1}

    for dupe in duplicates:
        i = 0
        for _ in range(duplicates[dupe]):
            file_to_rename = os.path.join(dirpath, dupe)
            head, tail = os.path.splitext(file_to_rename)

            new_filename = "{}_{}{}".format(head, i, tail)
            while os.path.exists(new_filename):
                i += 1
                new_filename = "{}_{}{}".format(head, i, tail)
            print("Renaming {} as {}".format(file_to_rename, new_filename))
            os.replace(file_to_rename, new_filename)


def rename_duplicates_in_tree(dirpath):
    # topdown false starts walking from the bottom of the tree instead of the top
    # vital for directory renaming
    for root, _, _ in os.walk(dirpath, topdown=False):
        rename_dupes_in_directory(root)
