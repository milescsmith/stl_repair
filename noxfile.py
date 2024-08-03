"""Nox sessions."""

import os
import sys
from pathlib import Path

import nox

PACKAGE = "revseq"
PYTHON_VERSIONS = ["3.10", "3.11", "3.12"]
os.environ["PDM_IGNORE_SAVED_PYTHON"] = "1"
os.environ["PDM_IGNORE_ACTIVE_VENV"] = "0"
nox.needs_version = ">=2024.4.15"
nox.options.sessions = (
    "mypy",
    "tests",
)

locations = (
    "src",
    "tests",
)


@nox.session(python="3.10")
def mypy(session: nox.Session) -> None:
    """Type-check using mypy."""
    session.run_always("pdm", "install", "--no-self", "--no-default", "--dev", external=True)
    session.run(
        "mypy",
        "--install-types",
        "--non-interactive",
        f"--python-executable={sys.executable}",
        "noxfile.py",
        external=True,
    )


@nox.session(python=PYTHON_VERSIONS)
def lockfile(session: nox.Session) -> None:
    """Run the test suite."""
    session.run_always("pdm", "lock", external=True)


@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    """Run the test suite."""
    session.run_always("pdm", "install", "--fail-fast", "--frozen-lockfile", "--dev", external=True)
    session.run(
        "coverage", "run", "--parallel", "-m", "pytest", "--numprocesses", "auto", "--random-order", external=True
    )


@nox.session(python="3.10")
def coverage(session: nox.Session) -> None:
    """Produce the coverage report."""
    args = session.posargs or ["report"]
    session.install("coverage[toml]", "codecov", external=True)

    if not session.posargs and any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")

    session.run("coverage", "json", "--fail-under=0")
    session.run("codecov", *args)
