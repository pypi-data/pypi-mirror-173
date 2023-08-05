# coding: utf-8

from __future__ import print_function
from __future__ import absolute_import

_package_data = dict(
    full_package_name='virtualenvutils',
    version_info=(0, 6, 3),
    __version__='0.6.3',
    version_timestamp='2022-10-24 11:50:51',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description='manage virtualenv/-m venv based utilities',
    keywords='virtualenv utilities',
    entry_points='virtualenvutils=virtualenvutils.__main__:main',
    # entry_points=None,
    license='MIT License',
    since=2016,
    # status: "α|β|stable",  # the package status on PyPI
    # data_files="",
    # universal=True,
    install_requires=[
        'ruamel.std.pathlib',
    ],
    python_requires='>=3',
)


version_info = _package_data['version_info']
__version__ = _package_data['__version__']


_cligen_data = """\
!Cli 0:
- !Instance virtualenvutils.virtualenvutils.VirtualEnvUtils
- !Opt [verbose, v, !Help increase verbosity level, !Action count, const: 1, nargs: 0, default: 0]
# - !PSO [version, !Action version, version: 'version: 0.5.8']
- alias:
  - !Arg [dir, nargs: +]
  - !Help deprecated
- link:
  - !Arg [dir, nargs: +]
  - !Help 'generate link from virtualenv utility installations to link dir '
- update:
  - !Opt [python, !Action store_true, !Help upgrade Python to latest stable (resolved from link /opt/python/3)]
  - !Opt [micro, !Action store_true, !Help upgrade Python micro version (resolved from link /opt/python/major.minor)]
  - !Opt [packages, !Action store_true, !Help also upgrade the packages when upgrading Python (assumes --python/--micro]
  - !Opt [pre, !Action store_true, !Help pass on --pre to 'pip update']
  - !Opt [pip, !Action store_true, !Help only update pip in all virtualenvs]
  - !Opt [test, !Action store_true, !Help don't execute actual command (currently --micro only)]
  - !Arg [dir, nargs: +]
  - !Help update packages in virtualenv. Can update Python in virtualenvs (this assumes versions and links under /opt/python/major.minor.micro
- install:
  - !Opt [python, p, type: pathlib.Path, !Help path to python binary to be used for virtualenv (resolved)]
  - !Opt [pkg, !Help 'name of the package to be installed (default: taken fromlast part of dir)']
  - !Opt [link, !Action store_true, !Help create a link in site-packages to current directory]
  - !Arg [dir, nargs: +]
  - !Help install package(s) in virtualenvs
- version:
  - !Opt [py, !Action store_true, !Help only show python versions]
  - !Arg [dir, nargs: +]
  - !Help scan versions of python and packages
"""
