import click
import sys

from typing import List

from pilotis.commands.aws import infra_command
from pilotis.commands.git import git_command
from pilotis.commands.init import init_command


def python_within_version(versions: List[str]):
    major = sys.version_info[0]
    minor = sys.version_info[1]
    version = f"{major}.{minor}"
    return version in versions


@click.group(name="pilotis")
def main() -> None:
    # Check python version
    if python_within_version(versions=["3.7", "3.8"]):
        click.echo("\033[92mThank you for using Pilotis.")
    else:
        click.echo("\033[91m Pilotis dependencies only supports python 3.7 and 3.8")
        exit(1)


main.add_command(init_command)
main.add_command(git_command)
main.add_command(infra_command)

if __name__ == '__main__':
    main()
