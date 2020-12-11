import os
import pathlib

import pytest

from context import rename


@pytest.fixture
def temp_path_with_files(tmp_path):
    # Windows uses case insensitive files by default - we need to enable case sensitive files
    if os.name == 'nt':
        os.system(f'cmd /c "fsutil.exe file setCaseSensitiveInfo {str(tmp_path)} enable"')

    base_dir = tmp_path

    # add a folder containing files with same case-insensitive names for testing
    content_dir = base_dir / 'content_dir'
    content_dir.mkdir()
    names = "afile.txt Afile.txt morefile.txt aFile.txt singlefile.txt adir ADIR afile_1.txt AFile.txt".split(' ')
    for name in names:
        filename = content_dir / name
        filename.write_text("Text file contents")

    return base_dir, content_dir


def test_rename_duplicates_in_directory_empty_directory_without_logfile(tmp_path):
    assert tmp_path.exists()
    rename.rename_duplicates_in_directory(tmp_path)
    assert tmp_path.exists() is False


def test_rename_duplicates_in_directory_empty_directory_logfile(tmp_path):
    empty_dir = tmp_path / 'empty_dir'
    empty_dir.mkdir()
    assert empty_dir.exists()

    logfile = tmp_path / "logfile"
    rename.rename_duplicates_in_directory(empty_dir, logfile)
    assert empty_dir.exists() is False

    log_contents = logfile.read_text()
    assert "Removed" in log_contents
    assert str(empty_dir) in log_contents


def test_rename_duplicates_in_directory_empty_directory_log_only(tmp_path):
    empty_dir = tmp_path / 'empty_dir'
    empty_dir.mkdir()
    assert empty_dir.exists()

    logfile = tmp_path / "logfile"
    rename.rename_duplicates_in_directory(empty_dir, logfile, log_only=True)
    assert empty_dir.exists()

    log_contents = logfile.read_text()
    assert "Will remove" in log_contents
    assert str(empty_dir) in log_contents


def test_rename_duplicates_in_directory(temp_path_with_files):
    _, content_dir = temp_path_with_files
    original_contents = list(content_dir.iterdir())

    rename.rename_duplicates_in_directory(content_dir)
    current_contents = list(content_dir.iterdir())

    # the extra file is the logfile
    assert len(original_contents) == len(current_contents) - 1
    assert len(set(current_contents)) == len(current_contents)

    # check logfile
    logfile = content_dir / rename.LOGFILE_NAME
    assert logfile.exists()

def test_rename_duplicates_in_directory_given_logfile(temp_path_with_files):
    base_dir, content_dir = temp_path_with_files

    logfile = base_dir / rename.LOGFILE_NAME
    original_contents = list(content_dir.iterdir())

    rename.rename_duplicates_in_directory(content_dir, logfile)
    current_contents = list(content_dir.iterdir())

    assert len(original_contents) == len(current_contents)
    assert len(set(current_contents)) == len(current_contents)

    # check logfile
    assert logfile.exists()


def test_rename_duplicates_in_tree(temp_path_with_files):
    base_dir, content_dir = temp_path_with_files

    original_contents = list(content_dir.iterdir())

    rename.rename_duplicates_in_tree(base_dir)
    current_contents = list(content_dir.iterdir())

    assert len(original_contents) == len(current_contents)
    assert len(set(current_contents)) == len(current_contents)

    # check logfile
    assert (base_dir / rename.LOGFILE_NAME).exists()
