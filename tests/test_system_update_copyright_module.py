# Copyright (c) 2024 Benjamin Mummery

import subprocess

from pytest_git import GitRepo


class TestNothingToDo:
    @staticmethod
    def test_no_files_changed(git_repo: GitRepo, cwd):
        """No files have been changed, nothing to check."""
        with cwd(git_repo.workspace):
            process: subprocess.CompletedProcess = subprocess.run(
                ["update-copyright", "."], capture_output=True, text=True
            )

        assert process.returncode == 0, process.stdout
