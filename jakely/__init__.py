#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division as _, print_function as _,
                absolute_import as _, unicode_literals as _)

# Version number
__version__ = "1.0.0"

# Was jakely imported from setup.py?
try:
    __JAKELY_SETUP__
except NameError:
    __JAKELY_SETUP__ = False

if not __JAKELY_SETUP__:
    from . import colorvision
    from . import ispectrum
    from . import plot
    from . import toolbox
