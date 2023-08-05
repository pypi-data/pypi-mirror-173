# coding: utf-8
# flake8: noqa
# cligen: 0.1.5, dd: 2021-09-20

import argparse
import importlib
import pathlib
import sys

from . import __version__


class CountAction(argparse.Action):
    """argparse action for counting up and down

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action=CountAction, const=1,
            nargs=0)
    parser.add_argument('--quiet', '-q', action=CountAction, dest='verbose',
            const=-1, nargs=0)
    """

    def __call__(self, parser, namespace, values, option_string=None):
        if self.const is None:
            self.const = 1
        try:
            val = getattr(namespace, self.dest) + self.const
        except TypeError:  # probably None
            val = self.const
        setattr(namespace, self.dest, val)


def main(cmdarg=None):
    cmdarg = sys.argv if cmdarg is None else cmdarg
    parsers = []
    parsers.append(argparse.ArgumentParser())
    parsers[-1].add_argument('--verbose', '-v', nargs=0, dest='_gl_verbose', metavar='VERBOSE', default=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--version', action='store_true', help='show program\'s version number and exit')
    subp = parsers[-1].add_subparsers()
    px = subp.add_parser('alias', help='deprecated')
    px.set_defaults(subparser_func='alias')
    parsers.append(px)
    parsers[-1].add_argument('dir', nargs='+')
    parsers[-1].add_argument('--verbose', '-v', nargs=0, help='increase verbosity level', action=CountAction, const=1)
    px = subp.add_parser('link', help='generate link from virtualenv utility installations to link dir ')
    px.set_defaults(subparser_func='link')
    parsers.append(px)
    parsers[-1].add_argument('dir', nargs='+')
    parsers[-1].add_argument('--verbose', '-v', nargs=0, help='increase verbosity level', action=CountAction, const=1)
    px = subp.add_parser('update', help='update packages in virtualenv. Can update Python in virtualenvs (this assumes versions and links under /opt/python/major.minor.micro')
    px.set_defaults(subparser_func='update')
    parsers.append(px)
    parsers[-1].add_argument('--python', action='store_true', help='upgrade Python to latest stable (resolved from link /opt/python/3)')
    parsers[-1].add_argument('--micro', action='store_true', help='upgrade Python micro version (resolved from link /opt/python/major.minor)')
    parsers[-1].add_argument('--packages', action='store_true', help='also upgrade the packages when upgrading Python (assumes --python/--micro')
    parsers[-1].add_argument('--pre', action='store_true', help="pass on --pre to 'pip update'")
    parsers[-1].add_argument('--pip', action='store_true', help='only update pip in all virtualenvs')
    parsers[-1].add_argument('--test', action='store_true', help="don't execute actual command (currently --micro only)")
    parsers[-1].add_argument('dir', nargs='+')
    parsers[-1].add_argument('--verbose', '-v', nargs=0, help='increase verbosity level', action=CountAction, const=1)
    px = subp.add_parser('install', help='install package(s) in virtualenvs')
    px.set_defaults(subparser_func='install')
    parsers.append(px)
    parsers[-1].add_argument('--python', '-p', type=pathlib.Path, help='path to python binary to be used for virtualenv (resolved)')
    parsers[-1].add_argument('--pkg', help='name of the package to be installed (default: taken fromlast part of dir)')
    parsers[-1].add_argument('--link', action='store_true', help='create a link in site-packages to current directory')
    parsers[-1].add_argument('dir', nargs='+')
    parsers[-1].add_argument('--verbose', '-v', nargs=0, help='increase verbosity level', action=CountAction, const=1)
    px = subp.add_parser('version', help='scan versions of python and packages')
    px.set_defaults(subparser_func='version')
    parsers.append(px)
    parsers[-1].add_argument('--py', action='store_true', help='only show python versions')
    parsers[-1].add_argument('dir', nargs='+')
    parsers[-1].add_argument('--verbose', '-v', nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers.pop()
    if '--version' in cmdarg[1:]:
        if '-v' in cmdarg[1:] or '--verbose' in cmdarg[1:]:
            return list_versions(pkg_name='virtualenvutils', version=None, pkgs=['ruamel.std.pathlib', 'virtualenv'])
        print(__version__)
        return
    args = parsers[0].parse_args(args=cmdarg[1:])
    for gl in ['verbose']:
        if getattr(args, gl, None) is None:
            setattr(args, gl, getattr(args, '_gl_' + gl))
        delattr(args, '_gl_' + gl)
    cls = getattr(importlib.import_module("virtualenvutils.virtualenvutils"), "VirtualEnvUtils")
    obj = cls(args)
    funcname = getattr(args, 'subparser_func', None)
    if funcname is None:
        parsers[0].parse_args('--help')
    fun = getattr(obj, args.subparser_func)
    return fun()

def list_versions(pkg_name, version, pkgs):
    version_data = [
        ('Python', '{v.major}.{v.minor}.{v.micro}'.format(v=sys.version_info)),
        (pkg_name, __version__ if version is None else version),
    ]
    for pkg in pkgs:
        try:
            version_data.append((pkg,  getattr(importlib.import_module(pkg), '__version__', '--')))
        except ModuleNotFoundError:
            version_data.append((pkg, 'NA'))
        except KeyError:
            pass
    longest = max([len(x[0]) for x in version_data]) + 1
    for pkg, ver in version_data:
        print('{:{}s} {}'.format(pkg + ':', longest, ver))


if __name__ == '__main__':
    sys.exit(main())
