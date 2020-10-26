# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import sys
import os
import shlex
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
import jakely

import sphinx_rtd_theme


# -- Project information -----------------------------------------------------

project = 'jakely'
copyright = '2020, Jacob Lustig-Yaeger'
author = 'Jacob Lustig-Yaeger'

# The short X.Y version
version = jakely.__version__
# The full version, including alpha/beta/rc tags
release = jakely.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'matplotlib.sphinxext.plot_directive',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.inheritance_diagram',
    'nbsphinx',
    'IPython.sphinxext.ipython_console_highlighting'
]

# Custom additions for exceptions
plot_include_source = False
plot_html_show_source_link = True
plot_html_show_formats = False
plot_formats = [('png', 200)]
plot_rcparams = {"figure.autolayout" : False, 'savefig.bbox': 'tight'}
# Remove ipython notebook prompt numbers
napoleon_use_ivar = True
# Make the order of the autodocs in the order they appear in the code
autodoc_member_order = 'bysource'

# Remove ipython notebook prompt numbers
nbsphinx_prolog = """
.. raw:: html

    <style>
        .nbinput .prompt,
        .nboutput .prompt {
        display: none;
        }
    </style>
"""

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
