# -*- coding: utf-8 -*-
# flake8: noqa

"""Command-line helper for setuptools and PyPI."""

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import os
import os.path as op

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


@cli.command()
def bump():
    """Bump the build number in the version.

    `__version__ = 'x.y.z'` => `__version__ = 'x.y.(z+1)'`.

    """
    regex = r"__version__ = '(\d+)\.(\d+)\.(\d+)'"
    name = op.basename(os.getcwd())
    path = op.join(name, '__init__.py')
    assert op.exists(path)
    with open(path, 'r+') as f:
        contents = f.read()
        m = re.search(regex, contents)
        major, minor, build = map(int, p.groups())
        new_version = "__version__ = '%d.%d.%d'" % (major, minor, build + 1)
        contents = re.sub(regex, new_version, contents)
        f.write(contents)


@cli.command()
def register():
    os.system('python setup.py register')


@cli.command()
def build():
    os.system('python setup.py sdist bdist_wheel')


@cli.command()
def release():
    os.system('twine upload dist/*')


if __name__ == '__main__':
    cli()
