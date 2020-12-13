import logging
import os

import pytest


@pytest.fixture
def temp_path_with_files(tmp_path):
    # Windows uses case insensitive files by default - we need to enable case sensitive files
    if os.name == 'nt':
        os.system(f'cmd /c "fsutil.exe file setCaseSensitiveInfo {str(tmp_path)} enable"')

    base_dir = tmp_path

    # add an empty dir
    (base_dir / "empty_dir").mkdir()

    # add a folder containing files with same case-insensitive names for testing
    content_dir = base_dir / 'content_dir'
    content_dir.mkdir()

    filename = ("afile.txt Afile.txt morefile.txt aFile.txt singlefile.txt "
               "afile_1.txt AFile.txt blah.xls adoc.doc backup.BAK").split(' ')
    dirnames = "adir ADIR".split(' ')
    for name in filename:
        (content_dir / name).touch()

    for name in dirnames:
        (content_dir / name).mkdir()

    # make more xls files
    (content_dir / 'adir'/ "excel.xls").touch()

    yield base_dir, content_dir


@pytest.fixture
def info_caplog(caplog):
    caplog.set_level(logging.INFO)
    yield caplog
