#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
from setuptools import setup

# Hackishly inject a constant into builtins to enable importing of the
# module in "setup" mode. Stolen from `kplr`
import sys
if sys.version_info[0] < 3:
    import __builtin__ as builtins
else:
    import builtins
builtins.__JAKELY_SETUP__ = True
import jakely

long_description = \
    """Jake LY's suite of simple python tools."""

# Setup!
setup(name='jakely',
      version=jakely.__version__,
      description="Jake LY's suite of simple python tools.",
      long_description=long_description,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering :: Astronomy',
      ],
      url='http://github.com/jlustigy/jakely',
      author='Jacob Lustig-Yaeger',
      author_email='jlustigy@gmail.com',
      license = 'MIT',
      packages=['jakely'],
      install_requires=[
                        'numpy',
                        'scipy',
                        'matplotlib >= 2.0.0',
                        #'colorpy'
                        ],
      dependency_links=[],
      scripts=[],
      include_package_data=True,
      zip_safe=False,
      data_files=[]
      )
