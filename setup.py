#!/usr/bin/env python
"""
TradeFlow - ალგორითმული ტრეიდინგის პლატფორმა
შექმნილი შაკო ჯინჭარაძის მიერ

Pythonic Algorithmic Trading Library - ბეკტესტინგი და ლაივ ტრეიდინგი
"""
from __future__ import print_function
import os
import re
import sys
from operator import lt, gt, eq, le, ge
from os.path import abspath, dirname, join
from distutils.version import StrictVersion
from setuptools import Extension, find_packages, setup

import versioneer


class LazyBuildExtCommandClass(dict):
    """
    Lazy command class that defers operations requiring Cython and numpy until
    they've actually been downloaded and installed by setup_requires.
    """
    def __contains__(self, key):
        return (
            key == 'build_ext'
            or super(LazyBuildExtCommandClass, self).__contains__(key)
        )

    def __setitem__(self, key, value):
        if key == 'build_ext':
            raise AssertionError("build_ext overridden!")
        super(LazyBuildExtCommandClass, self).__setitem__(key, value)

    def __getitem__(self, key):
        if key != 'build_ext':
            return super(LazyBuildExtCommandClass, self).__getitem__(key)

        from Cython.Distutils import build_ext as cython_build_ext
        import numpy

        class build_ext(cython_build_ext, object):
            def build_extensions(self):
                numpy_incl = numpy.get_include()
                for ext in self.extensions:
                    ext.include_dirs.append(numpy_incl)
                super(build_ext, self).build_extensions()
        return build_ext


def window_specialization(typename):
    """Make an extension for an AdjustedArrayWindow specialization."""
    return Extension(
        'tradeflow.lib._{name}window'.format(name=typename),
        ['tradeflow/lib/_{name}window.pyx'.format(name=typename)],
        depends=['tradeflow/lib/_windowtemplate.pxi'],
    )


ext_modules = [
    Extension('tradeflow.assets._assets', ['tradeflow/assets/_assets.pyx']),
    Extension('tradeflow.assets.continuous_futures',
              ['tradeflow/assets/continuous_futures.pyx']),
    Extension('tradeflow.lib.adjustment', ['tradeflow/lib/adjustment.pyx']),
    Extension('tradeflow.lib._factorize', ['tradeflow/lib/_factorize.pyx']),
    window_specialization('float64'),
    window_specialization('int64'),
    window_specialization('int64'),
    window_specialization('uint8'),
    window_specialization('label'),
    Extension('tradeflow.lib.rank', ['tradeflow/lib/rank.pyx']),
    Extension('tradeflow.data._equities', ['tradeflow/data/_equities.pyx']),
    Extension('tradeflow.data._adjustments', ['tradeflow/data/_adjustments.pyx']),
    Extension('tradeflow._protocol', ['tradeflow/_protocol.pyx']),
    Extension('tradeflow.finance._finance_ext',
              ['tradeflow/finance/_finance_ext.pyx']),
    Extension('tradeflow.gens.sim_engine', ['tradeflow/gens/sim_engine.pyx']),
    Extension('tradeflow.data._minute_bar_internal',
              ['tradeflow/data/_minute_bar_internal.pyx']),
    Extension('tradeflow.data._resample', ['tradeflow/data/_resample.pyx']),
    Extension('tradeflow.pipeline.loaders.blaze._core',
              ['tradeflow/pipeline/loaders/blaze/_core.pyx'],
              depends=['tradeflow/lib/adjustment.pxd']),
]


STR_TO_CMP = {
    '<': lt, '<=': le, '=': eq, '==': eq, '>': gt, '>=': ge,
}

SYS_VERSION = '.'.join(list(map(str, sys.version_info[:3])))


REQ_PATTERN = re.compile(
    r"(?P<name>[^=<>;]+)((?P<comp>[<=>]{1,2})(?P<spec>[^;]+))?"
    r"(?:(;\W*python_version\W*(?P<pycomp>[<=>]{1,2})\W*"
    r"(?P<pyspec>[0-9.]+)))?\W*"
)


def _filter_requirements(lines_iter, filter_names=None,
                         filter_sys_version=False):
    for line in lines_iter:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        match = REQ_PATTERN.match(line)
        if match is None:
            raise AssertionError("Could not parse requirement: %r" % line)
        name = match.group('name')
        if filter_names is not None and name not in filter_names:
            continue
        if filter_sys_version and match.group('pyspec'):
            pycomp, pyspec = match.group('pycomp', 'pyspec')
            comp = STR_TO_CMP[pycomp]
            pyver_spec = StrictVersion(pyspec)
            if comp(SYS_VERSION, pyver_spec):
                yield line.split(';')[0]
            continue
        yield line


def read_requirements(path, conda_format=False, filter_names=None):
    real_path = join(dirname(abspath(__file__)), path)
    with open(real_path) as f:
        reqs = _filter_requirements(f.readlines(), filter_names=filter_names,
                                    filter_sys_version=not conda_format)
        if conda_format:
            def _conda_format(req):
                def _sub(m):
                    name = m.group('name').lower()
                    if name == 'numpy':
                        return 'numpy x.x'
                    if name == 'tables':
                        name = 'pytables'
                    comp, spec = m.group('comp', 'spec')
                    if comp and spec:
                        formatted = '%s %s%s' % (name, comp, spec)
                    else:
                        formatted = name
                    pycomp, pyspec = m.group('pycomp', 'pyspec')
                    if pyspec:
                        selector = ' # [int(py) %s int(%s)]' % (
                            pycomp, ''.join(pyspec.split('.')[:2]).ljust(2, '0')
                        )
                        return formatted + selector
                    return formatted
                return REQ_PATTERN.sub(_sub, req, 1)
            reqs = map(_conda_format, reqs)
        return list(reqs)


def install_requires(conda_format=False):
    return read_requirements('etc/requirements.in', conda_format=conda_format)


def extras_requires(conda_format=False):
    extras = {
        extra: read_requirements('etc/requirements_{0}.in'.format(extra),
                                 conda_format=conda_format)
        for extra in ('dev', 'talib')
    }
    extras['all'] = [req for reqs in extras.values() for req in reqs]
    return extras


def setup_requirements(requirements_path, module_names, conda_format=False):
    module_names = set(module_names)
    module_lines = read_requirements(requirements_path,
                                     conda_format=conda_format,
                                     filter_names=module_names)
    if len(set(module_lines)) != len(module_names):
        raise AssertionError(
            "Missing requirements. Looking for %s, but found %s."
            % (module_names, module_lines)
        )
    return module_lines


conda_build = os.path.basename(sys.argv[0]) in ('conda-build',
                                                'conda-build-script.py')

setup_requires = setup_requirements(
    'etc/requirements_build.in',
    ('Cython', 'numpy'),
    conda_format=conda_build,
)

conditional_arguments = {
    'setup_requires' if not conda_build else 'build_requires': setup_requires,
}

setup(
    name='tradeflow',
    url='https://github.com/navyforses/TradeFlow',
    version=versioneer.get_version(),
    cmdclass=LazyBuildExtCommandClass(versioneer.get_cmdclass()),
    description='TradeFlow - ალგორითმული ტრეიდინგის პლატფორმა | Algorithmic Trading Platform',
    long_description=open('README.md', encoding='utf-8').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'tradeflow = tradeflow.__main__:main',
        ],
    },
    author='Shako Jincharadze',
    author_email='jincharadzeshako@gmail.com',
    packages=find_packages(include=['tradeflow', 'tradeflow.*']),
    ext_modules=ext_modules,
    include_package_data=True,
    package_data={root.replace(os.sep, '.'):
                  ['*.pyi', '*.pyx', '*.pxi', '*.pxd']
                  for root, dirnames, filenames in os.walk('tradeflow')
                  if '__pycache__' not in root},
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: Georgian',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    install_requires=install_requires(conda_format=conda_build),
    extras_require=extras_requires(conda_format=conda_build),
    python_requires='>=3.8',
    **conditional_arguments
)
