from context import remove, utilities
from fixtures import temp_path_with_files, info_caplog


def test_remove_empty_dir(tmp_path, info_caplog):
    assert tmp_path.exists()
    remove.remove_empty_dir(tmp_path)
    assert tmp_path.exists() is False
    assert str(tmp_path) in info_caplog.text

def test_remove_empty_dir_log_only(tmp_path, info_caplog):
    assert tmp_path.exists()
    remove.remove_empty_dir(tmp_path, log_only=True)
    assert tmp_path.exists()
    assert str(tmp_path) in info_caplog.text