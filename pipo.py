# -*- coding: utf-8 -*-
# flake8: noqa

"""Command-line helper for setuptools and PyPI."""

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import os
import os.path as op
import re

import click


#------------------------------------------------------------------------------
# pipo
#------------------------------------------------------------------------------

__version__ = '0.1.0'


@click.group()
@click.version_option(version=__version__)
@click.help_option('-h', '--help')
def cli():
    """Command-line helper for setuptools and PyPI"""
    pass


def _bump(increment=1):
    regex = r"__version__ = '(\d+)\.(\d+)\.(\d+)'"
    # Find the file that contains the version.
    name = op.basename(os.getcwd())
    # Try name/__init__.py
    path = op.join(name, '__init__.py')
    if not op.exists(path):
        # Try name.py
        path = name + '.py'
    # Read the file.
    with open(path, 'r') as f:
        contents = f.read()
        # Parse the version numbers.
        m = re.search(regex, contents)
        major, minor, build = map(int, m.groups())
    # Increment the build number.
    with open(path, 'w') as f:
        build += increment
        new_version = "__version__ = '%d.%d.%d'" % (major, minor, build)
        contents = re.sub(regex, new_version, contents)
        f.write(contents)
    return (major, minor, build)


@cli.command()
def bump():
    """Bump the build number in the version.

    `__version__ = 'x.y.z'` => `__version__ = 'x.y.(z+1)'`.

    """
    v = _bump(+1)
    click.echo("Bumped version to %s." % str(v))


@cli.command()
def unbump():
    """Like bump, but in the other direction."""
    v = _bump(-1)
    click.echo("Unbumped version to %s." % str(v))


@cli.command()
def register():
    """Register the new project."""
    os.system('python setup.py register')


@cli.command()
def build():
    """Make builds."""
    os.system('python setup.py sdist bdist_wheel')


@cli.command()
def clear():
    """Delete the build and dist subdirectories."""
    os.system('rm -rf dist build')
    click.echo("Deleted build/ and dist/.")


@cli.command()
@click.pass_context
def release(ctx):
    """Upload the build."""
    ctx.invoke(clear)
    ctx.invoke(build)
    os.system('twine upload dist/*')


@cli.command
def kickstart():
    """Kickstart a new project.

    Generate template files for a new Python package.

    """
    # TODO
    pass


if __name__ == '__main__':
    cli()
