from context import remove, utilities
from fixtures import temp_path_with_files, info_caplog


def test_remove_empty_dir(temp_path_with_files, info_caplog):
    base_dir, content_dir = temp_path_with_files

    empty_dirs = [
        base_dir / 'empty_dir',
        content_dir / 'ADIR'
        ]

    for edir in empty_dirs:
        assert edir.exists()
    
    remove.remove_empty_dir(base_dir)
    
    assert empty_dirs[0].exists() is False
    assert empty_dirs[1].exists()

    assert str(empty_dirs[0]) in info_caplog.text
    assert str(empty_dirs[1]) not in info_caplog.text


def test_remove_empty_dir_log_only(temp_path_with_files, info_caplog):
    base_dir, content_dir = temp_path_with_files

    empty_dirs = [
        base_dir / 'empty_dir',
        content_dir / 'ADIR'
        ]

    for edir in empty_dirs:
        assert edir.exists()
    
    remove.remove_empty_dir(base_dir, log_only=True)
    
    for edir in empty_dirs:
        assert edir.exists()

    assert str(empty_dirs[0]) in info_caplog.text
    assert str(empty_dirs[1]) not in info_caplog.text


def test_remove_empty_dir_in_tree(temp_path_with_files, info_caplog):
    base_dir, content_dir = temp_path_with_files
    assert base_dir.exists()

    empty_dirs = [
        base_dir / 'empty_dir',
        content_dir / 'ADIR'
        ]

    remove.remove_empty_dir_in_tree(base_dir)

    for edir in empty_dirs:
        assert edir.exists() is False
        assert str(edir) in info_caplog.text


def test_remove_empty_dir_in_tree_log_only(temp_path_with_files, info_caplog):
    base_dir, content_dir = temp_path_with_files
    assert base_dir.exists()

    empty_dirs = [
        base_dir / 'empty_dir',
        content_dir / 'ADIR'
        ]
    remove.remove_empty_dir_in_tree(base_dir, log_only=True)
    
    for edir in empty_dirs:
        assert edir.exists()
        assert str(edir) in info_caplog.text


def test_remove_files_matching_pattern_in_dir(temp_path_with_files, info_caplog):
    _, content_dir = temp_path_with_files

    pattern = ".xls"

    original_contents = list(str(c) for c in content_dir.iterdir())
    assert len([fn for fn in original_contents if pattern in fn]) > 0

    remove.remove_filepattern_in_dir(content_dir, pattern)

    current_contents = list(str(c) for c in content_dir.iterdir())
    assert len([fn for fn in current_contents if pattern in fn]) == 0


def test_remove_files_matching_pattern_in_dir_log_only(temp_path_with_files, info_caplog):
    _, content_dir = temp_path_with_files

    pattern = ".xls"

    original_contents = list(str(c) for c in content_dir.iterdir())
    original_matches = [fn for fn in original_contents if pattern in fn]
    assert len(original_matches) > 0

    remove.remove_filepattern_in_dir(content_dir, pattern, log_only=True)

    current_contents = list(str(c) for c in content_dir.iterdir())
    current_matches = [fn for fn in current_contents if pattern in fn]
    assert current_matches == original_matches


def test_remove_files_matching_pattern_in_tree(temp_path_with_files, info_caplog):
    _, content_dir = temp_path_with_files

    pattern = ".xls"

    matches = [
        content_dir / 'adir' / "excel.xls",
        content_dir / 'blah.xls'
    ]

    for m in matches:
        assert m.exists()

    remove.remove_filepattern_in_tree(content_dir, pattern)

    for m in matches:
        assert m.exists() is False


def test_remove_files_matching_pattern_in_tree_log_only(temp_path_with_files, info_caplog):
    _, content_dir = temp_path_with_files

    pattern = ".xls"

    matches = [
        content_dir / 'adir' / "excel.xls",
        content_dir / 'blah.xls'
    ]

    for m in matches:
        assert m.exists()

    remove.remove_filepattern_in_tree(content_dir, pattern, log_only=True)

    for m in matches:
        assert m.exists()
