from __future__ import (division as _, print_function as _,
                absolute_import as _, unicode_literals as _)

import numpy as np
import sys, os
import subprocess
import platform
import imp
from types import ModuleType, FunctionType

__all__ = ["print2", "say", "find_nearest", "alphabet", "Deluxetable", "Input",
           "LoadIn"]

def print2(value, files = [sys.stdout]):
    """
    Use `print` with multiple `file` arguments

    Parameters
    ----------
    value : str
        Value to be printed
    files : list
        A list of file-like objects (streams); defaults to the current sys.stdout.

    Example
    -------
    >>> f = open("test.txt", "a")
    >>> print2("Hello, World!", files=[sys.stdout, f])
    >>> f.close()
    """

    for f in files:
        print(value, file = f)

    return

def say(value, rate = 180):
    """
    Similar to the `print()` function, but for spoken text using the `say` command
    on Mac OS

    Parameters
    ----------
    value : str
        String to be spoken
    rate : int
        Rate of speech in words per minute (default is 180)
    """

    if platform.system() != 'Darwin':
        print("`Say` only works on Macs")

    output = subprocess.call(["say", "-r %i" %rate, '"%s"' %value])

    return

def find_nearest(array,value):
    """Finds index of array nearest to the value
    """
    idx = (np.abs(array-value)).argmin()
    return idx

def alphabet():
    alphabetlist=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    for value in alphabetlist:
        yield value

class Deluxetable:
    """
    Note
    ----
    Originally written by Zhu, Weiwei
    (https://sites.google.com/site/zhuweiweipku/my-python-projects-2/tex-table-class)
    """

    def alphabet(self):
        alphabetlist=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        for value in alphabetlist:
            self.commentslines += '\\tablenotetext{%s}{%s}\n' % (value, self.comments.next())
            #print '\tablenotetext{%s}{%s}' % (value, self.comments.next())
            yield value

    def __init__(self, Caption='', colsetting='', colnames=[], data=[],
                 comments=[],label='', fmt="%.2f", half_width=False):
        """
        Create a LaTeX deluxetable.

        Parameters
        ----------
        Caption : str
            Table caption
        colsetting : str
            Column alignment (e.g. 'cccc')
        colnames : list
            List of table column name strings
        data : list
            List of table column data
        comments : list
            Table comments
        label : str
            Table label (e.g. "tab:example")
        fmt : str or list
            Table column formatting
        half_width: bool
            Make a table spanning the half page width (for two column)
        """

        if colnames == []: raise InputError('must have column names specified!')

        if data == []: raise InputError('must have data provided!')

        if not len(colnames) == len(data):
            raise InputError('number of column names does match number of columns in the data!')
        elif not colsetting == '' and not len(colsetting) == len(colnames):
            raise InputError('number of control characters in the colsetting does not match number of columns')
        elif colsetting == '':
            colsetting = 'c' * len(colnames)
        else:pass

        if type(fmt) == str:
            fmts = [fmt for i in range(len(colnames))]
        else:
            fmts = fmt

        if half_width:
            # Using multicol, half page width
            table_call = "deluxetable"
            table_width = "0.47\linewidth"
        else:
            # Using full page width
            table_call = "deluxetable*"
            table_width = "\linewidth"

        self.comments = comments
        self.commentslines = ''
        cols=''
        abc = self.alphabet()
        for name in colnames:
            while not name.find('#') == -1:name = name.replace('#',r'\tablenotemark{%s}' % abc.next(), 1)
            cols += '\colhead{%s}  &' % name
        cols = cols[:-1]
        rowcounts = len(data[0])
        colcounts = len(data)
        datalines = []
        for irow in range(rowcounts):
            datarow = fmts[0] %(data[0][irow])
            for icol in range(1,colcounts):
                datarow += '&  ' + fmts[icol] %(data[icol][irow])
            datalines.append(datarow)
        datatable = '\\\\\n'.join(datalines)
        while not datatable.find('#') == -1:datatable = datatable.replace('#',r'\tablenotemark{%s}' % abc.next(), 1)



        self.parsestring = r"""
\begin{%(table_call)s}{%(colsetting)s}
\tablewidth{%(table_width)s}
\tablecaption{\label{%(label)s} %(Caption)s }
\tablehead{ %(colnames)s }
\startdata
%(data)s
\enddata
\tablecomments{%(comments)s}
\end{%(table_call)s}
""" % {'label':label,
       'colsetting':colsetting,
       'Caption':Caption,
       'colnames':cols,
       'data':datatable,
       'comments':self.comments,
       'table_call':table_call,
       'table_width':table_width}


    def __str__(self):
        return self.parsestring

################################################################################
# BEGIN EASY INPUTS
################################################################################

INPATH = "inputs/"
relpath = os.path.join(os.path.dirname(__file__), INPATH)

class Input(object):
    """
    Reads default and user input files and creates a class where the input file
    variables are attributes. See inputs/ to customize.

    """
    def __init__(self, input_type = ''):

        if (input_type == 'telescope') or (input_type == 'planet') or (input_type == 'star'):
            pass
        else:
            print("Error: unrecognized input_type. Please use 'telescope', 'planet', or 'star'.")
            return

        try:
            del sys.modules['input_usr']
            del sys.modules['input']
        except KeyError:
            pass

        default_input_file = os.path.join(relpath,'input_default_'+input_type+'.py')
        user_input_file = os.path.join(relpath,'input_user_'+input_type+'.py')

        self._input = imp.load_source("input", default_input_file)            # Load default inputs into self._input

        self._input_usr = imp.load_source("input_usr", user_input_file)       # Load user inputs into self._input_usr

        self._input.__dict__.update(self._input_usr.__dict__)                 # Update self._input with user values

        inp_dict = self._input.__dict__

        for key, value in inp_dict.items():
            if key.startswith('__') or isinstance(value, ModuleType) or isinstance(value, FunctionType):
                inp_dict.pop(key, None)

        self.__dict__.update(inp_dict)                                        # Make all parameters accessible as self.param

        del self._input
        del self._input_usr

class LoadIn(object):
    """
    Reads default and user input files and creates a class where the input file
    variables are attributes. See inputs/ to customize.

    """
    def __init__(self, path):

        if not path.endswith('.py'):
            print("Incompatible file.")
            return

        try:
            del sys.modules['input']
        except KeyError:
            pass

        user_input_file = path

        self._input = imp.load_source("input", user_input_file)            # Load inputs into self._input

        inp_dict = self._input.__dict__

        for key, value in inp_dict.items():
            if key.startswith('__') or isinstance(value, ModuleType) or isinstance(value, FunctionType):
                inp_dict.pop(key, None)

        self.__dict__.update(inp_dict)                                        # Make all parameters accessible as self.param

        del self._input
