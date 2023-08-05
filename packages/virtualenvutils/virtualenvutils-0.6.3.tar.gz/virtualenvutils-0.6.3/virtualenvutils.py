# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

import sys
import os
import subprocess
import datetime
import json

from ruamel.std.pathlib import Path


class VirtualEnvUtils(object):
    def __init__(self, args, config=None):
        self._args = args
        self._config = config
        self._venv_dirs = None
        self._link_dir = Path('/usr/local/bin')
        self._bpp = Path('/opt/python')

    @staticmethod
    def print_cmd(cmd):
        print(' '.join([s if s != '' else s for s in [str(x) for x in cmd]]))

    def link(self):
        """
        aliases is not such a good idea when dealing with crontab files etc
        starting with 0.4 make a link in self._link_dir (/usr/local/bin) instead
        the alias command still works, but if a target for the alias is found
        to be the destination of a symlink in self._link_dir it is commented out
        """
        aliases = dict()
        # for lb in self.linked_binaries:
        #     print('lb', lb)
        keys = []
        venv_dirs = self.venv_dirs[:]
        for d in venv_dirs[:]:
            # check for configuration file
            conf = d / 'virtualenvutils.conf'
            if not conf.exists():
                continue
            venv_dirs.remove(d)
            # print('conf file', d, file=sys.stderr)
            for line in conf.read_text().splitlines():
                line = line.strip()
                if not line:
                    continue
                # print('line', line, file=sys.stderr)
                if u':' in line:
                    util, full = line.strip().split(u":", 1)
                    full = d / 'bin' / full
                else:
                    util = line
                    full = d / 'bin' / util
                if not full.exists():
                    print('cannot find {}\n  from line {}\  in {}'.format(
                        full, line, conf), file=sys.stderr)
                if util in aliases:
                    print('virtualenvutils name clashes {}\n  {}\n  {}'.format(
                        util,
                        util,
                        aliases[util],
                    ), file=sys.stderr)
                else:
                    aliases[util] = full
                    keys.append(util)
        for d in venv_dirs[:]:
            util = d / 'bin' / (d.stem)
            if not util.exists():
                continue
            venv_dirs.remove(d)
            # print('matching virtualenv name', d, file=sys.stderr)
            if util.name in aliases:
                print('virtualenvutils name clashes {}\n  {}\n  {}'.format(
                    util.name,
                    util,
                    aliases[util.name],
                ), file=sys.stderr)
            else:
                aliases[util.stem] = util
                keys.append(util.stem)
        for d in venv_dirs[:]:
            for util in (d / 'bin').glob('*'):
                if not util.is_file():
                    continue
                for skip in ['activate', 'easy_install', 'python', 'pip', 'wheel']:
                    if util.stem.startswith(skip):
                        break
                else:
                    if d in venv_dirs:  # only first time
                        venv_dirs.remove(d)
                    if util.name.endswith('.so'):
                        continue
                    if util.name.endswith('.pyc'):
                        continue
                    if util.name.endswith('.py'):
                        # can make xyz.py into util xyz, or skip. Yeah, skip
                        continue
                    if util.name in aliases:
                        if self._args.verbose > 0:
                            print('skipping name clashes {}\n  {}\nin favor of\n  {}'.format(
                                util.name,
                                util,
                                aliases[util.name],
                            ), file=sys.stderr)
                    else:
                        aliases[util.name] = util
                        keys.append(util.name)
        assert not venv_dirs
        for k in sorted(keys):
            prefix = '# ' if aliases[k] in self.linked_binaries else ''
            print("{}alias {}='{}'".format(prefix, k, aliases[k]))

    @property
    def venv_dirs(self):

        def test_a_dir(sub_dir):
            if not sub_dir.is_dir():
                return False
            for x in ('bin', 'lib'):  # used to test for include, not installed on fip/vh2/py310
                sub_sub_dir = sub_dir / x
                if not sub_sub_dir.exists():
                    break
                if not sub_sub_dir.is_dir():
                    break
            else:
                activate = sub_dir / 'bin' / 'activate'
                if activate.exists() and activate.is_file():
                    self._venv_dirs.append(sub_dir)
                    return True
            return False

        if self._venv_dirs is not None:
            return self._venv_dirs
        self._venv_dirs = []
        for d in self._args.dir:
            d = Path(d).expanduser()
            if test_a_dir(d):
                continue
            for sub_dir in d.glob('*'):
                test_a_dir(sub_dir)
        return self._venv_dirs

    def update(self):
        import pkgutil  # NOQA
        import pkg_resources  # NOQA
        # pkg_resources.working_set is what pip relies upon, that is bound to the
        # pip/python that is running
        # print('x', [x for x in pkg_resources.working_set])
        # print('pip', pip.__file__)
        pre = ['--pre'] if self._args.pre else []
        # pip_args = ['list', '--outdated', '--format=freeze']  # no longer working in 22.3
        has_run = False
        pyupdate = 0
        if self._args.python:
            pyupdate += 1
        self._args.minor = False
        #if self._args.minor:
        #    pyupdate += 1
        if self._args.micro:
            pyupdate += 1
        if pyupdate > 1:
            print('select only one of --python, --minor and --micro')
            return
        for d in self.venv_dirs:
            has_run = True
            pkgs = None
            current_ver = None
            pip_cmd = [str(d / 'bin' / 'pip'), '--disable-pip-version-check']
            if (self._args.python or self._args.minor or self._args.micro):
                pkgs = self.packages_in_venv(d, freeze=True, all=self._args.packages)
                current_ver = self.python_version_in_venv(d)
                # print('pkgs', pkgs)
            if self._args.python:
                if self.latest > current_ver:
                    print('updating python', current_ver, '->', self.latest)
                    # self.backup_venv(d)
                    try:
                        self.erase_venv(d)
                        self.create_venv(d, self.latest)
                        self.install_packages(d, pkgs)
                    except Exception as e:
                        self.restore_from_backup(d)
                        raise
                else:
                    print('already on latest python version', self.latest)
            if self._args.micro:
                ds = str(d) + ':'
                #self.possible_upgrades((3, 8, 2), verbose=1)
                #self.possible_upgrades((2, 7, 5), verbose=1)
                #self.possible_upgrades((3, 5, 3), verbose=1)
                v, pb = self.possible_upgrades(current_ver).get('micro', (None, None))
                if v is None:
                    print(f'{ds:32s} no update necessary')
                    continue
                print(f'{ds:32s} updating python micro version to {v}')
                if self._args.test:
                    continue
                self.upgrade_venv(d, pb)
            if self._args.pip:
                print('updating pip:', d)
                res = check_output(pip_cmd + ['install', '-U', 'pip'])
                print(res)
                continue
            if not self._args.packages:
                if self._args.python or self._args.minor or self._args.micro:
                    continue
            res = self.packages_in_venv(d, outdated=True)
            print('updating packages', d, res)
            # NOT WORKING: this gives you the packages from the calling environment
            # for package in pip.get_installed_distributions():
            #     print('package', package)
            #
            # for p in (d / 'lib').glob('python*'):
            #     if p:
            #         break
            # else:
            #     continue  # no lib/python* found
            # pth = [str(p / 'site-packages')]
            # NOT WORKING: does give you only toplevel names and not in original dotted
            #              package form
            # for pkg in pkgutil.iter_modules(path=pth):
            #     continue
            #     if pkg[2]:
            #         print('pkg', pkg[1])
            #
            # NOT WORKING: only gives non-namespace packages
            # for pkg in pkgutil.walk_packages(path=pth):
            #     continue
            #     if pkg[2]:
            #         print('pkg', pkg[1])
            #
            if res:
                print(check_output(pip_cmd + ['install', '-U'] + pre + res))
            self.create_link(d)
        if not has_run:
            print('no project(s) found')

    def create_venv(self, d, version):
        versions = '.'.join([str(x) for x in version])
        cmd = [self._bpp / versions / 'bin' / 'python', '-m', 'venv', '--copies', d]
        if version[0] == 2:
            raise NotImplementedError
        check_output(cmd, verbose=2)
        cmd = [d / 'bin' / 'pip', 'install', 'wheel']
        check_output(cmd, verbose=2)

    def upgrade_venv(self, d, python_binary):
        cmd = [python_binary, '-m', 'venv', '--copies', '--upgrade', d]
        # self.print_cmd(cmd)
        check_output(cmd, verbose=2)


    def install_packages(self, d, pkgs):
        cmd = [d / 'bin' / 'pip', 'install']
        pkgs2 = []
        for p in pkgs:
            if p.startswith('pip==') or p.startswith('setuptools=='): # or p.startswith('wheel=='):
                continue
            pkgs2.append(p)
        cmd.extend(pkgs2)
        check_output(cmd, verbose=2)

    def backup_venv(self, d):
        print(type(d))
        cmd = ['tar', 'cJf', '{}_{:%Y%m%d_%H%M%S}.tar.xz'.format(d, datetime.datetime.now()),
               '-C', d.parent, d.name]
        check_output(cmd, verbose=2)

    def latest_backup(self, d):
        return sorted(d.parent.glob(d.name + "_*.tar.xz"))[-1]

    def restore_from_backup(self, d):
        l = self.latest_backup(d)
        cmd = ['tar', 'xf', l, '-C', d.parent]
        check_output(cmd, verbose=2)

    def erase_venv(self, d):
        print('deleting', d)
        d.rmtree()

#            if 'python2' in py_paths or '2.7' in py_paths:
#                cmd = ['virtualenv']
#                cmd.extend(['--python', py_path])
#            else:
#                cmd = [py_paths, '-m', 'venv']
#            full_cmd = cmd + [p]
#            check_output(full_cmd, verbose=2)
#            check_output([p / 'bin' / 'pip', 'install', pkg], verbose=2)
#            self.create_link(p, pkg)


    @property
    def linked_binaries(self):
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            x = [f.resolve() for f in self._link_dir.glob('*') if f.is_symlink()]
            setattr(self, attr, x)
        return getattr(self, attr)

    @property
    def py2_path(self):
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            setattr(self, attr, (self._bpp / '2').resolve())
        return getattr(self, attr)

    @property
    def py2(self):
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            setattr(self, attr, tuple(int(x) for x in self.py2_path.name.split('.')))
        return getattr(self, attr)

    @property
    def py3_path(self):
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            setattr(self, attr, (self._bpp / '3').resolve())
        return getattr(self, attr)

    @property
    def py3(self):
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            setattr(self, attr, tuple(int(x) for x in self.py3_path.name.split('.')))
        return getattr(self, attr)

    @property
    def latest(self):
        return self.py3

    def latest_versions(self, out=sys.stdout):
        print('py2', self.py2, file=out)
        print('py3', self.py3, file=out)

    def python_version_in_venv(self, d):
        python_cmd = [str(d / 'bin' / 'python'), '--version']
        res = check_output(python_cmd, stderr=subprocess.STDOUT).split()[-1]
        return tuple(int(x) for x in res.split('.'))

    # update all with
    # for x in /opt/util/*/bin/pip ; do $x install -U pip;  done
    def packages_in_venv(self, d, pre=False, outdated=False, freeze=False, all=False):
        pre = ['--pre'] if pre else []
        pip_args = ['--disable-pip-version-check', 'list']
        if outdated:
            # pip_args = ['list', '--outdated', '--format=freeze']  # no longer working in 22.3
            pip_args.extend(['--outdated', '--format=json'])
        if freeze or all:
            # pip_args.extend(['--format=freeze'])
            pip_args.extend(['--format=json'])
        # pip_args_no_legacy = ['list']
        pip_cmd = [str(d / 'bin' / 'pip')]
        res = []
        # for line in check_output(pip_cmd + pip_args + pre,
        #                          stderr=subprocess.STDOUT).splitlines():
        #     if line.startswith('-----'):
        #         continue
        #     if line.startswith('Package '):
        #         continue
        #     if outdated or all:
        #         res.append(line.split('==')[0])
        #     else:
        #         res.append(line)
        for x in json.loads(check_output(pip_cmd + pip_args + pre,
                            stderr=subprocess.STDOUT)):
            res.append(x['name'])
        return res

    def possible_upgrades(self, v, verbose=0):
        if isinstance(v, list):
            v = tuple(v)
        if verbose > 0:
            print(f'{v=}')
        result = {}
        micro_bin = (self._bpp / f'{v[0]}.{v[1]}').resolve()
        micro = tuple(int(x) for x in micro_bin.name.split('.'))
        if micro != v:
            result['micro'] = (micro, micro_bin / 'bin' / 'python')
        minor_bin = (self._bpp / f'{v[0]}').resolve()
        minor = tuple(int(x) for x in minor_bin.name.split('.'))
        if minor[:2] != v[:2]:
            result['minor'] = (minor, minor_bin / 'bin' / 'python')
        major_bin = sorted(self._bpp.glob('?'))[-1].resolve()
        major = tuple(int(x) for x in major_bin.name.split('.'))
        if major[0] != v[0]:
            result['major'] = (major, major_bin / 'bin' / 'python')
        if verbose > 0:
            for k in result:
                print(f'{k} -> {result[k][0]}')
            print()
        return result


    def upgrade_version(self, v, py3=False):
        alt = ''
        python_bin = None
        if py3 or v[0] == 3:
            if v < self.py3:
                alt = str(self.py3)
                python_bin = self.py3_path / 'bin' / 'python'
            elif v > self.py3:
                raise NotImplementedError
        elif v[0] == 2:
            if v < self.py2:
                alt = str(self.py2)
                python_bin = self.py2_path / 'bin' / 'python'
            elif v > self.py2:
                raise NotImplementedError
        else:
            raise NotImplementedError
        return alt, python_bin

    def version(self):
        self.latest_versions()
        dir_len = 0
        for d in self.venv_dirs:
            if len(str(d)) > dir_len:
                dir_len = len(str(d))

        for d in self.venv_dirs:
            v = self.python_version_in_venv(d)
            alt, pb = self.upgrade_version(v)
            print('{0:{1}s} {2:10s}  {3:10s}  {4}'.format(str(d), dir_len, str(v), alt, pb))
            if alt and not self._args.py:
                for line in (self.packages_in_venv(d)):
                    print(' ', line)
            sys.stdout.flush()

    def install(self):
        os.environ['PATH'] = os.path.dirname(sys.executable) + ':' + os.environ['PATH']
        for d in self._args.dir:
            p = Path(d)
            if self._args.pkg:
                assert len(self._args.dir) == 1
                pkg = self._args.pkg
            else:
                pkg = Path(d).name
            print('pkg', pkg)
            if self._args.python:
                py_path = self._args.python.resolve()
            else:
                # if not set explicitly, would get the version from virtualenv
                py_path = self.py3_path / 'bin' / 'python'
            py_paths = str(py_path)
            print('py_paths', py_paths)
            if 'python2' in py_paths or '2.7' in py_paths:
                cmd = ['virtualenv']
                cmd.extend(['--python', py_path])
            else:
                cmd = [py_paths, '-m', 'venv', '--copies']
            full_cmd = cmd + [p]
            check_output(full_cmd, verbose=2)
            # looks like you don't need --disable-pip-version-check when upgrading pip
            check_output([p / 'bin' / 'pip', 'install', '-U', 'pip', 'wheel'], verbose=0)
            check_output([p / 'bin' / 'pip', 'install', pkg], verbose=2)
            self.create_link(p, pkg)
            if self._args.link:
                lib_dir = p / 'lib'
                lib_dir = list(lib_dir.glob('python*'))[0]
                site_packages = lib_dir / 'site-packages'
                print('sp', site_packages)

    def create_link(self, path, pkg=None):
        util = path / 'bin' / (path.stem)
        if pkg is None:
            pkg = path.stem  # lazy...
        alt_util = path / 'bin' / (pkg)
        if not util.exists() and not alt_util.exists():
            print('util', util, 'not found create link by hand')
            return
        if not util.exists():
            util = alt_util
        src = self._link_dir / util.stem
        if src.exists():
            return
        print('creating link for', util, 'from', src)
        print()
        try:
            src.symlink_to(util)
        except:
            cmd = 'sudo ln -s {} {}'.format(util, src)
            print('running', cmd, 'to try and install symlink')
            os.system(cmd)


def check_output(*args, **kw):
    import subprocess
    verbose = kw.pop('verbose', 0)
    largs = list(args)
    largs[0] = [str(s) for s in largs[0]]
    if verbose > 1:
        print('cmd', largs[0])
    res = subprocess.check_output(*largs, **kw).decode('utf-8')
    if verbose > 0:
        print(res)
    return res


if __name__ == "__main__":
    print("change directory if you're doing python -m virtualenvutils")
