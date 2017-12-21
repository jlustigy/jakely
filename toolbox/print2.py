from __future__ import print_function as _
import sys

__all__ = ["print2"]

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