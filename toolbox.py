# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 22:54:08 2016

@author: jlustigy
"""

import numpy as np

def find_nearest(array,value):
    """Finds index of array nearest to the value
    """
    idx = (np.abs(array-value)).argmin()
    return idx