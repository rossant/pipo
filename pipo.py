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
import requests


#------------------------------------------------------------------------------
# Utils
#------------------------------------------------------------------------------

__version__ = '0.1.0'


VERSION_REGEX = re.compile(r"__version__ = '(\d+)\.(\d+)\.(\d+)'")


def lib_name():
    """Return the library name."""
    return op.basename(os.getcwd())


def lib_file_path():
    """Return the path to the file that presumably defines `__version__`."""
    # Find the file that contains the version.
    name = lib_name()
    # Try name/__init__.py
    path = op.join(name, '__init__.py')
    if not op.exists(path):
        # Try name.py
        path = name + '.py'
    return path


def parse_version(contents):
    """Parse the (major, minor, build) version of the library."""
    # Parse the version numbers.
    m = re.search(VERSION_REGEX, contents)
    return map(int, m.groups())


def _pipversion():
    url = 'https://pypi.python.org/pypi/%s' % lib_name()
    page = requests.get(url).text
    name = lib_name()
    r = re.search(r'%s (\d+\.\d+\.\d+)' % name, page)
    return r.group(1)


def _bump(increment=1):
    regex = VERSION_REGEX
    path = lib_file_path()
    with open(path, 'r') as f:
        contents = f.read()
    major, minor, build = parse_version(contents)
    # Increment the build number.
    with open(path, 'w') as f:
        build += increment
        new_version = "__version__ = '%d.%d.%d'" % (major, minor, build)
        contents = re.sub(regex, new_version, contents)
        f.write(contents)
    return (major, minor, build)


#------------------------------------------------------------------------------
# pipo CLI
#------------------------------------------------------------------------------

@click.group()
@click.version_option(version=__version__)
@click.help_option('-h', '--help')
def cli():
    """Command-line helper for setuptools and PyPI"""
    pass


@cli.command()
def bump():
    """Bump the build number in the version.

    `__version__ = 'x.y.z'` => `__version__ = 'x.y.(z+1)'`.

    """
    v = _bump(+1)
    click.echo("Bumped version to %s." % str(v))
    os.system('git diff')
    if click.confirm('Commit `Bump version`?'):
        os.system('git commit -am "Bump version"')


@cli.command()
def unbump():
    """Like bump, but in the other direction."""
    v = _bump(-1)
    click.echo("Unbumped version to %s." % str(v))


@cli.command()
def version():
    """Display the library version."""
    name = lib_name()
    path = lib_file_path()
    with open(path, 'r') as f:
        contents = f.read()
    major, minor, build = parse_version(contents)
    pipversion = _pipversion()
    click.echo("%s, version %d.%d.%d (%s on PyPI)" % (name,
                                                      major, minor, build,
                                                      pipversion,
                                                      ))


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
