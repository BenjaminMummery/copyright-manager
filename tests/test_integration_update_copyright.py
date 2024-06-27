# Copyright (c) 2024 Benjamin Mummery

from pathlib import Path

from freezegun import freeze_time
from pytest import CaptureFixture
from pytest_mock import MockerFixture

from conftest import assert_matching
from src import update_copyright


class TestNothingToDo:
    """Tests representing cases where the module should do nothing."""

    @staticmethod
    def test_called_on_empty_dir(
        capsys: CaptureFixture,
        mocker: MockerFixture,
        tmp_path: Path,
        cwd,
    ):
        # GIVEN
        mocker.patch("sys.argv", ["stub_name", "."])

        # WHEN
        with cwd(tmp_path):
            assert update_copyright.main() == 0

        # THEN
        captured = capsys.readouterr()
        assert_matching("captured stdout", "expected stdout", captured.out, "")
        assert_matching("captured stderr", "expected stderr", captured.err, "")

    @staticmethod
    def test_called_on_dir_with_no_supported_files(
        capsys: CaptureFixture,
        mocker: MockerFixture,
        tmp_path: Path,
        cwd,
    ):
        # GIVEN
        mocker.patch("sys.argv", ["stub_name", "."])
        (tmp_path / "file.fake").write_text("")

        # WHEN
        with cwd(tmp_path):
            assert update_copyright.main() == 0

        # THEN
        captured = capsys.readouterr()
        assert_matching("captured stdout", "expected stdout", captured.out, "")
        assert_matching("captured stderr", "expected stderr", captured.err, "")

    @staticmethod
    @freeze_time("1923-01-01")
    def test_called_on_dir_where_all_files_already_have_up_to_date_copyright(
        capsys: CaptureFixture,
        mocker: MockerFixture,
        tmp_path: Path,
        cwd,
    ):
        # GIVEN
        mocker.patch("sys.argv", ["stub_name", "."])
        (tmp_path / "file.py").write_text("# Copyright 1923 William Shackleton")

        # WHEN
        with cwd(tmp_path):
            assert update_copyright.main() == 0

        # THEN
        captured = capsys.readouterr()
        assert_matching("captured stdout", "expected stdout", captured.out, "")
        assert_matching("captured stderr", "expected stderr", captured.err, "")

    @staticmethod
    @freeze_time("1923-01-01")
    def test_called_on_file_with_up_to_date_copyright(
        capsys: CaptureFixture,
        mocker: MockerFixture,
        tmp_path: Path,
        cwd,
    ):
        # GIVEN
        (filepath := (tmp_path / "file.py")).write_text(
            "# Copyright 1923 William Shackleton"
        )
        mocker.patch("sys.argv", ["stub_name", filepath])

        # WHEN
        with cwd(tmp_path):
            assert update_copyright.main() == 0

        # THEN
        captured = capsys.readouterr()
        assert_matching("captured stdout", "expected stdout", captured.out, "")
        assert_matching("captured stderr", "expected stderr", captured.err, "")
