import os.path as op
import re
from setuptools import setup


# Find version number from `__init__.py` without executing it.
curdir = op.dirname(op.realpath(__file__))
filename = op.join(curdir, 'pipo.py')
with open(filename, 'r') as f:
    version = re.search(r"__version__ = '([^']+)'", f.read()).group(1)


setup(
    name='pipo',
    version=version,
    py_modules=['pipo'],
    install_requires=[
        'pip',
        'click',
        'twine',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        pipo=pipo:cli
    ''',
)
