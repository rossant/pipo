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

## Usage

```bash
pipo register    # register your new project on PyPI
pipo build       # build tar.gz and wheel
pipo release     # upload your files on PyPI using twine
pipo pipversion  # get the latest version on PyPI
pipo bump        # bump the build version number as defined in your __init__.py
pipo --help      # show the list of commands
```
