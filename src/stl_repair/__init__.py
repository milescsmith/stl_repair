"""
.. module:: stl_repair
   :platform: Unix, Macos
   :synopsis: use the repair capabilities provided by blender's "3D Print Toolbox" plugin to repair stls

.. moduleauthor:: Miles Smith <mileschristiansmith@gmail.com>
"""

import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Annotated

import typer
from loguru import logger
from rich import print as rprint
from rich.progress import Progress

from stl_repair.__main__ import repair_stl
from stl_repair.logging import init_logger

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"


logger.disable("stl_repair")

app = typer.Typer(
    name="stl-repair",
    help="Use blender to repair stls",
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="rich",
)

verbosity_level = 0


def version_callback(value: bool) -> None:  # FBT001
    """Prints the version of the package."""
    if value:
        rprint(f"[yellow]stl-repair[/] version: [bold blue]{__version__}[/]")
        raise typer.Exit()


@app.callback()
def verbosity(
    verbose: Annotated[
        int,
        typer.Option(
            "-v",
            "--verbose",
            help="Control output verbosity. Pass this argument multiple times to increase the amount of output.",
            count=True,
        ),
    ] = 0,
) -> None:
    verbosity_level = verbose  # noqa: F841


@app.callback(invoke_without_command=True)
@app.command(name="repair_stls", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def stl_repair_cli(
    filepath: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=True,
            writable=True,
            readable=True,
            resolve_path=True,
            help="The path to either a single STL file to repair or a directory full of stls",
        ),
    ],
    output: Annotated[
        Path,
        typer.Option(
            "--output",
            "-o",
            help="Where to write repaired files to",
            exists=False,
        ),
    ],
    suffix: Annotated[str, typer.Option("--suffix", "-s", help="Suffix to append to output files")] = "_fixed",
    debug: Annotated[bool, typer.Option("--debug", help="Print extra information for debugging.")] = False,  # nFBT002
    version: Annotated[  # ARG001
        bool,
        typer.Option(
            "--version",
            callback=version_callback,
            help="Print version number.",
        ),
    ] = False,
):
    logger.remove()
    if debug:
        logger.add(
            sys.stderr,
            format="* <red>{elapsed}</red> - <cyan>{module}:{file}:{function}</cyan>:<green>{line}</green> - <yellow>{message}</yellow>",
            colorize=True,
        )
        init_logger(verbose=verbosity_level)
    else:
        logger.add(sys.stderr, format="* <yellow>{message}</yellow>", colorize=True)
        init_logger(verbose=1, msg_format="<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
    if not output.exists():
        output.mkdir()
    if filepath.is_file():
        repair_stl(filename=filepath, output_dir=output, suffix=suffix)
    else:
        with Progress() as progress_bar:
            stls = list(filepath.glob("*.stl"))
            task = progress_bar.add_task("Repairing files...", total=len(stls))
            for i in stls:
                progress_bar.console.print(f"Starting {i}")
                repair_stl(filename=i, output_dir=output, suffix=suffix)
                progress_bar.console.print(f"Repaired {i}")
                progress_bar.advance(task)
