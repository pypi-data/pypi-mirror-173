import stat
from enum import Enum, auto
from os import path, chmod
from pathlib import Path
from typing import Dict

import click
import inquirer
from click import Context

from pilotis.commands import OPTION_PROJECT_NAME, OPTION_PROJECT_SLUG, OPTION_PYTHON_PACKAGE_NAME
from pilotis.commands.aws import infra_command
from pilotis.commands.copier_utils import populate_and_copy
from pilotis.commands.git import git_command
from pilotis.commands.project_slug import slugify
from pilotis.commands.shell_utils import call_shell
from pilotis.domain.pilotis_project_config import init_config

OPTION_TOOLS_TO_SETUP = 'add_other_commands'


class Tools(Enum):
    AWS = 'AWS'
    GIT = 'Git'


PYENV_CONFIG_BASH_FILE_NAME = "pyenv_config.bash"
CHECK_TOOLS_BASH_FILE_NAME = "check_tools.bash"

SCRIPTS_DIR = Path("scripts")

_current_directory_path = Path(path.realpath(__file__)).parent
_templates_dir = _current_directory_path.parent.parent / 'templates'
_main_templates_path = _templates_dir / 'init'


@click.command("init", help="Initialize project: generate base folders & files.")
@click.option('--project-parent-dir',
              type=click.Path(exists=True, file_okay=False, resolve_path=True),
              default='.',
              callback=lambda _, __, value: Path(value),
              help="Directory where the project will be created")
@click.option('--skip-install',
              type=bool,
              default=False,
              is_flag=True,
              help="Skip post installation scripts")
@click.pass_context
def init_command(ctx: Context, project_parent_dir: Path, skip_install: bool) -> None:
    answers_to_inquiries = _inquire_user_inputs()
    substitution_data = _init_substitution_data(answers_to_inquiries)
    generate(project_parent_dir, skip_install=skip_install, substitution_data=substitution_data)

    if Tools.GIT.value in answers_to_inquiries[OPTION_TOOLS_TO_SETUP]:
        ctx.invoke(git_command,
                   project_dir=project_parent_dir / substitution_data[OPTION_PROJECT_SLUG],
                   skip_install=skip_install)
    if Tools.AWS.value in answers_to_inquiries[OPTION_TOOLS_TO_SETUP]:
        ctx.invoke(infra_command,
                   project_dir=project_parent_dir / substitution_data[OPTION_PROJECT_SLUG],
                   skip_install=skip_install)
    print("\033[92mInitialization succeed. Enjoy !")


def generate(project_parent_dir: Path, substitution_data: Dict[str, str] = None, skip_install: bool = False) -> None:
    _write_files(project_parent_dir, substitution_data)
    if not skip_install:
        _post_install_scripts(project_parent_dir, substitution_data)


def _inquire_user_inputs() -> Dict[str, str]:
    questions = [
        inquirer.Text(OPTION_PROJECT_NAME, message="Project name?"),
        inquirer.Checkbox(OPTION_TOOLS_TO_SETUP,
                          message="Which tool do you want Pilotis to setup in your project?",
                          choices=[possible_value.value for possible_value in Tools]),
    ]
    return inquirer.prompt(questions)


def _init_substitution_data(answers_to_inquiries: Dict[str, str]) -> Dict[str, str]:
    project_name = answers_to_inquiries[OPTION_PROJECT_NAME]
    project_slug = slugify(project_name)
    python_package_name = project_slug.replace('-', '_')

    return {
        OPTION_PROJECT_NAME: project_name,
        OPTION_PROJECT_SLUG: project_slug,
        OPTION_PYTHON_PACKAGE_NAME: python_package_name
    }


def _post_install_scripts(project_parent_dir: Path, substitution_data: Dict[str, str]) -> None:
    call_shell("make setup-env", working_dir=project_parent_dir / substitution_data[OPTION_PROJECT_SLUG])


def _write_files(project_parent_dir: Path, substitution_data: Dict[str, str]) -> None:
    populate_and_copy(_main_templates_path, project_parent_dir, substitution_data)
    _make_env_scripts_executable(project_parent_dir, substitution_data)
    _make_build_scripts_executable(project_parent_dir, substitution_data)
    init_config(project_parent_dir, substitution_data[OPTION_PROJECT_SLUG])


def _make_env_scripts_executable(project_parent_dir: Path, substitution_data: Dict[str, str]) -> None:
    setup_env_script_path = project_parent_dir / substitution_data[OPTION_PROJECT_SLUG] / SCRIPTS_DIR
    _make_script_executable_for_user(setup_env_script_path / CHECK_TOOLS_BASH_FILE_NAME)
    _make_script_executable_for_user(setup_env_script_path / PYENV_CONFIG_BASH_FILE_NAME)


def _make_build_scripts_executable(project_parent_dir: Path, substitution_data: Dict[str, str]) -> None:
    project_dir = project_parent_dir / substitution_data[OPTION_PROJECT_SLUG]
    container_dir = project_dir / "containers"
    containers = ["base", "dash", "tests"]
    for container_name in containers:
        build_script = container_dir / container_name / "build.sh"
        _make_script_executable_for_user(build_script)


def _make_script_executable_for_user(build_script):
    chmod(build_script, stat.S_IXUSR | stat.S_IRUSR)
