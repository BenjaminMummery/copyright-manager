# Copyright (c) 2024 Benjamin Mummery

import os
from contextlib import contextmanager
from typing import Optional

import pytest


@pytest.fixture(scope="session")
def cwd():
    @contextmanager
    def cwd(path):
        oldcwd = os.getcwd()
        os.chdir(path)
        try:
            yield
        finally:
            os.chdir(oldcwd)

    return cwd


def assert_matching(
    name1: str, name2: str, value1, value2, message: Optional[str] = None
):
    """
    Assert that 2 values are the same, and print an informative output if they are not.

    We compare quite a few longish strings in this repo, this gives a better way to
    understand where they're clashing.
    """
    failure_message = (
        f"{name1} did not match {name2}:\n"
        f"= {name1.upper()} ============\n"
        f"{value1}\n"
        f"= {name2.upper()} ==========\n"
        f"{value2}\n"
        "============================="
    )
    if message:
        failure_message += f"\n{message}"
    assert value1 == value2, failure_message
