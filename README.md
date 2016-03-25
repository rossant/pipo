# pipo

setuptools, pip, PyPI made easy.

## Installation

```bash
pip install pipo
```

Dependencies:

* Python 2 or 3
* pip
* twine
* click
* requests

## Usage

```bash
pipo register    # register your new project on PyPI
pipo build       # build tar.gz and wheel
pipo release     # upload your files on PyPI using twine
pipo pipversion  # get the latest version on PyPI
pipo bump        # bump the build version number as defined in your __init__.py
pipo --help      # show the list of commands
```

## Notes

This tool has been tailored to my needs and to the way I structure my Python packages. You may have to fork and adapt it to your own projects.

It is assumed that your library matches one of the following structures:

```
mylib/                  # root of the git repository
  |- mylib/             # package directory
       |- __init__.py
```

or for smaller projects:

```
mylib/                  # root of the git repository
  |- mylib.py           # main file
```

### About `pipo bump`

The `pipo bump` command bumps the **build number** of the version as defined in either `libname.py` or `libname/__init__.py` by:

```python
__version__ = 'X.Y.Z'
```

This command asks for confirmation to commit the change with the `Bump version` commit message.
