#!/usr/bin/env python3
from pathlib import Path
import shutil
import click
import sys

CONFIG_FILES = [Path('Configuration.h'), Path('Configuration_adv.h')]

BASE_CONFIG = Path('base/')
PRINTERS = Path("printers/")


@click.group()
def cli():
    pass


@cli.command()
@click.argument('path',
                type=click.Path(path_type=Path, file_okay=False, exists=True))
def diff(path: Path):
    """Show diff between current base files, and Marlin repo.

    PATH to root of Marlin checkout.
    """
    for file in CONFIG_FILES:
        if not (path / "Marlin" / file).exists():
            print(f"Missing file: {path / 'Marlin' /file}")
        if not (BASE_CONFIG / file).exists():
            print(f"Missing file: {BASE_CONFIG / file}")

    raise NotImplementedError(
        "The actual file diffing is not implemented, yet.")


@cli.command()
@click.argument('path',
                type=click.Path(path_type=Path, file_okay=False, exists=True))
def update(path: Path):
    """Update config files from Marlin repos.

    PATH to root of Marlin checkout.
    """
    for file in CONFIG_FILES:
        if not (path / "Marlin" / file).exists():
            print(f"Missing file: {path / file}, aborting")
            return

    for file in CONFIG_FILES:
        print(f"Copying {file}")
        shutil.copy((path / "Marlin" / file), BASE_CONFIG)


@cli.command()
@click.argument('name', type=str)
def new(name: str):
    """Create a new printer config, based off of the base config.

    NAME of printer.
    """

    target_folder = PRINTERS / Path(name)
    if target_folder.exists():
        print(
            f"Error: There are existing files or directories called '{name}', I will not overwrite."
        )

    target_folder.mkdir(parents=True, exist_ok=False)

    for file in CONFIG_FILES:
        shutil.copy((BASE_CONFIG / file), target_folder)


@cli.command()
@click.argument('name', type=str)
@click.argument('path',
                type=click.Path(path_type=Path, file_okay=False, exists=True))
def apply(name: str, path: Path):
    """Apply printer config to Marlin.
    
    NAME of printer.
    PATH to Marlin.
    """
    source_folder = PRINTERS / Path(name)
    if not source_folder.is_dir():
        print(f"No configuration found for printer named: {name}")
        sys.exit(1)

    for file in CONFIG_FILES:
        shutil.copy(source_folder / file, path / "Marlin")


if __name__ == '__main__':
    cli()
