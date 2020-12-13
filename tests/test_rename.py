import pathlib
import logging

from context import rename, utilities
from fixtures import temp_path_with_files, info_caplog


log = logging.getLogger(__name__)


def test_rename_duplicates_in_directory_empty_directory(tmp_path, info_caplog):
    assert tmp_path.exists()
    rename.rename_duplicates_in_directory(tmp_path)
    assert tmp_path.exists() is False
    assert str(tmp_path) in info_caplog.text


def test_rename_duplicates_in_directory_empty_directory_log_only(tmp_path, info_caplog):
    assert tmp_path.exists()
    rename.rename_duplicates_in_directory(tmp_path, log_only=True)
    assert tmp_path.exists()
    assert str(tmp_path) in info_caplog.text


def test_rename_duplicates_in_directory(temp_path_with_files, info_caplog):
    _, content_dir = temp_path_with_files

    original_contents = list(str(c) for c in content_dir.iterdir())
    rename.rename_duplicates_in_directory(content_dir)
    current_contents = list(str(c) for c in content_dir.iterdir())

    # check we haven't lost any files
    assert len(original_contents) == len(current_contents)

    # check that all the new files are uniquely named
    assert len(set([c.lower() for c in current_contents])) == len(current_contents)

    # check log
    duplicates = utilities.find_duplicates(original_contents)
    for filename in duplicates:
        assert filename in info_caplog.text


def test_rename_duplicates_in_directory_log_only(temp_path_with_files, info_caplog):
    _, content_dir = temp_path_with_files

    original_contents = list(str(c) for c in content_dir.iterdir())
    rename.rename_duplicates_in_directory(content_dir, log_only=True)
    current_contents = list(str(c) for c in content_dir.iterdir())

    assert original_contents == current_contents

    # check log
    duplicates = utilities.find_duplicates(original_contents)
    for filename in duplicates:
        assert filename in info_caplog.text


def test_rename_duplicates_in_tree(temp_path_with_files, info_caplog):
    base_dir, content_dir = temp_path_with_files

    original_contents = list(str(c) for c in content_dir.iterdir())
    rename.rename_duplicates_in_tree(base_dir)
    current_contents = list(str(c) for c in content_dir.iterdir())

    # check we haven't lost any files
    assert len(original_contents) == len(current_contents)

    # check that all the new files are uniquely named
    assert len(set([c.lower() for c in current_contents])) == len(current_contents)

    # check log
    duplicates = utilities.find_duplicates(original_contents)
    for filename in duplicates:
        assert filename in info_caplog.text


def test_rename_duplicates_in_tree_log_only(temp_path_with_files, info_caplog):
    base_dir, content_dir = temp_path_with_files

    original_contents = list(str(c) for c in content_dir.iterdir())
    rename.rename_duplicates_in_tree(base_dir, log_only=True)
    current_contents = list(str(c) for c in content_dir.iterdir())

    assert original_contents == current_contents

    # check log
    duplicates = utilities.find_duplicates(original_contents)
    for filename in duplicates:
        assert filename in info_caplog.text
