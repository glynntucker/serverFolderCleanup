import os
import pathlib
from tempfile import TemporaryDirectory

import rename
from rename import (
    rename_dupes_in_directory, rename_duplicates_in_tree
)


def test_rename_dupes_in_directory(monkeypatch):
    dirpath = pathlib.Path("A://fake/path")
    dirname_list = "afile.txt afile.txt morefile.txt afile.txt singlefile.txt adir adir afile_1.txt AFile.txt".split(' ')
    dirlist = [dirpath / filename for filename in dirname_list]

    current_path_list = dirlist[:]
    dupes_found = []
    dupes_renamed = []

    def mock_iterdir(path):
        nonlocal dirlist
        return iter(dirlist)

    def mock_replace(path, new_path):
        nonlocal current_path_list
        nonlocal dupes_found
        nonlocal dupes_renamed

        dupes_found.append(path)
        current_path_list.remove(path)

        dupes_renamed.append(new_path)
        current_path_list.append(new_path)

    monkeypatch.setattr(pathlib.Path, 'iterdir', mock_iterdir)
    monkeypatch.setattr(pathlib.Path, 'replace', mock_replace)

    rename_dupes_in_directory(dirpath)

    expected_dupes = sorted(
        dirpath / filename for filename in "afile.txt afile.txt adir AFile.txt".split(' ')
        )
    expected_new_names = sorted(
        dirpath / filename for filename in "afile_0.txt afile_2.txt adir_0 AFile_3.txt".split(' ')
        )

    expected_path_list = sorted(
        dirpath / filename for filename in
        "morefile.txt singlefile.txt afile_0.txt afile_1.txt"
        " afile_2.txt afile.txt adir_0 adir AFile_3.txt".split(' ')
        )

    assert sorted(dupes_found) == expected_dupes
    assert sorted(dupes_renamed) == expected_new_names
    assert sorted(current_path_list) == expected_path_list


def test_rename_duplicates_in_tree(monkeypatch):
    dirpath = pathlib.Path("A://fake/path")
    walk_called = False
    rename_dupes_in_directory_called = False
    called_path = ""

    def mock_walk(path, topdown):
        nonlocal walk_called
        nonlocal dirpath

        walk_called = True
        assert topdown is False

        return [[os.path.join(path, 'dirname'), ['another_dirname'], ['filename.txt']]]

    def mock_iterdir(path):
        return []

    def mock_replace(path, new_path):
        pass

    def mock_rename_dupes_in_directory(path):
        nonlocal rename_dupes_in_directory_called
        nonlocal called_path

        rename_dupes_in_directory_called = True
        called_path = path.parent

    monkeypatch.setattr(os, 'walk', mock_walk)
    monkeypatch.setattr(pathlib.Path, 'iterdir', mock_iterdir)
    monkeypatch.setattr(pathlib.Path, 'replace', mock_replace)
    monkeypatch.setattr(rename, 'rename_dupes_in_directory', mock_rename_dupes_in_directory)

    rename_duplicates_in_tree(dirpath)

    assert walk_called is True
    assert rename_dupes_in_directory_called is True
    assert called_path == dirpath
