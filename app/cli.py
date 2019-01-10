import os
import sys
import json
import click

from flask.cli import FlaskGroup
from flask import current_app
from flask_azure_storage import create_all

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def create_application(info):
    from app import create_app
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_application)
def cli():
    """This is a management script for the Operations-Web application."""
    pass


@cli.command()
@click.option('-a', '--all', 'scope', flag_value='all', default=True, help='Seeds/updates all the database tables.')
@click.option('-p', '--permissions', 'scope', flag_value='permissions', help='Seeds/updates the permissions tables.')
def seed(scope):
    """Seeds the database."""
    from app.models import Role, Permission
    with open(os.path.join(BASE_DIR, 'seedfiles', 'permissions.json')) as perm_file:
        perm = json.load(perm_file)
    with open(os.path.join(BASE_DIR, 'seedfiles', 'roles.json')) as role_file:
        roles = json.load(role_file)

    if scope == 'all':
        click.secho('All scope selected.', fg='blue', bold=True)

        click.echo('Seeding Permission table.')
        Permission.insert_permissions(perm)
        click.secho('Completed!', fg='green')

        click.echo('Seeding Role table.')
        Role.insert_roles(roles)
        click.secho('Completed!', fg='green')

    elif scope == 'permissions':
        click.secho('Permissions scope selected.', fg='blue', bold=True)

        click.echo('Seeding Permission table.')
        Permission.insert_permissions(perm)
        click.secho('Completed!', fg='green')

        click.echo('Seeding Role table.')
        Role.insert_roles(roles)
        click.secho('Completed!', fg='green')

        click.echo('Cleaning Permission table.')
        Permission.clean_permissions(perm)
        click.secho('Completed!', fg='green')

        click.secho('Seed operation completed.', fg='green', bold=True)

    else:
        raise click.BadParameter('Invalid parameter.')


@cli.command()
def static():
    """Uploads static assets to Azure Storage"""
    create_all(current_app)
    click.echo('Static assets uploaded.')


def main(as_module=False):
    this_module = __package__ + '.cli'
    args = sys.argv[1:]

    if as_module:
        if sys.version_info >= (2, 7):
            name = 'python -m ' + this_module.rsplit('.', 1)[0]
        else:
            name = 'python -m ' + this_module
        sys.argv = ['-m', this_module] + sys.argv[1:]
    else:
        name = None

    cli.main(args=args, prog_name=name)


if __name__ == '__main__':
    main(as_module=True)
