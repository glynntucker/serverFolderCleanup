import pathlib

from context import utilities


def test_directory_is_empty_true(tmp_path):
    assert tmp_path.exists()
    assert list(tmp_path.iterdir()) == []
    assert utilities.directory_is_empty(tmp_path)


def test_directory_is_empty_false(tmp_path):
    filename = tmp_path / "not_an_empty_directory.txt"
    filename.write_text("Truely this is not empty")
    assert tmp_path.exists()
    assert list(tmp_path.iterdir())
    assert utilities.directory_is_empty(tmp_path) is False


def test_create_new_path(tmp_path):
    names = ("a_file.txt", "another_file.txt")
    for name in names:
        filename = tmp_path / name
        filename.write_text("File contents")
    assert tmp_path.exists()
    assert list(tmp_path.iterdir())
    new_filename = utilities.create_new_path(tmp_path, "a_file.txt")
    assert new_filename not in names
