import os

import main
from main import rename_dupes_in_directory, rename_duplicates_in_tree


def test_rename_dupes_in_directory(monkeypatch):
    dirlist = "afile.txt afile.txt morefile.txt afile.txt singlefile.txt adir adir afile_1.txt".split(' ')
    dirpath = os.path.normpath("A://fake/path")

    current_path_list = [os.path.join(dirpath, filename) for filename in dirlist]
    dupes_found = []
    dupes_renamed = []

    def mock_dir_list(path):
        nonlocal dirlist
        return dirlist

    def mock_replace(path, new_path):
        nonlocal current_path_list
        nonlocal dupes_found
        nonlocal dupes_renamed

        dupes_found.append(path)
        current_path_list.remove(path)

        dupes_renamed.append(new_path)
        current_path_list.append(new_path)

    def mock_path_exists(path):
        nonlocal current_path_list
        return path in current_path_list

    monkeypatch.setattr(os, 'listdir', mock_dir_list)
    monkeypatch.setattr(os, 'replace', mock_replace)
    monkeypatch.setattr(os.path, 'exists', mock_path_exists)

    rename_dupes_in_directory(dirpath)

    expected_dupes = sorted(os.path.join(dirpath, filename) for filename in
                            "afile.txt afile.txt afile.txt adir adir".split(' '))
    expected_new_names = sorted(os.path.join(dirpath, filename) for filename in
                                "afile_0.txt afile_2.txt afile_3.txt adir_0 adir_1".split(' '))

    expected_path_list = sorted(os.path.join(dirpath, filename) for filename in
                                "morefile.txt singlefile.txt afile_0.txt afile_1.txt"
                                " afile_2.txt afile_3.txt adir_0 adir_1".split(' '))

    assert sorted(dupes_found) == expected_dupes
    assert sorted(dupes_renamed) == expected_new_names
    assert sorted(current_path_list) == expected_path_list


def test_rename_duplicates_in_tree(monkeypatch):
    dirpath = os.path.normpath("A://fake/path")
    walk_called = False
    rename_dupes_in_directory_called = False
    called_path = ""

    def mock_walk(path, topdown):
        nonlocal walk_called
        nonlocal dirpath

        walk_called = True
        assert topdown is False

        return [[os.path.join(path, 'dirname'), ['another_dirname'], ['filename.txt']]]

    def mock_dir_list(path):
        return []

    def mock_replace(path, new_path):
        pass

    def mock_path_exists(path):
        return True

    def mock_rename_dupes_in_directory(path):
        nonlocal rename_dupes_in_directory_called
        nonlocal called_path

        rename_dupes_in_directory_called = True
        called_path = os.path.normpath("A://fake/path")

    monkeypatch.setattr(os, 'walk', mock_walk)
    monkeypatch.setattr(os, 'listdir', mock_dir_list)
    monkeypatch.setattr(os, 'replace', mock_replace)
    monkeypatch.setattr(os.path, 'exists', mock_path_exists)
    monkeypatch.setattr(main, 'rename_dupes_in_directory', mock_rename_dupes_in_directory)

    rename_duplicates_in_tree(dirpath)

    assert walk_called is True
    assert rename_dupes_in_directory_called is True
    assert called_path == dirpath
