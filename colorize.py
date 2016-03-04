# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 21:44:34 2016

@author: jlustigy
"""

import matplotlib.cm as cmx
import matplotlib.colors as colors
import matplotlib.pylab as plt
import numpy as np

def colorize(vector,cmap='plasma', vmin=None, vmax=None):
    """Convert a vector to RGBA colors.

    Parameters
    ----------
    vector : array
        Array of values to be represented by relative colors     
    cmap : str (optional)
        Matplotlib Colormap name
    vmin : float (optional)
        Minimum value for color normalization. Defaults to np.min(vector)
    vmax : float (optional)
        Maximum value for color normalization. Defaults to np.max(vector)
        
    Returns
    -------
    vcolors : np.ndarray
        Array of RGBA colors
    scalarmap : matplotlib.cm.ScalarMappable
        ScalerMap to convert values to colors
    cNorm : matplotlib.colors.Normalize
        Color normalization
    """
    
    if vmin is None: vmin = np.min(vector)
    if vmax is None: vmax = np.max(vector)    
    
    cm = plt.get_cmap(cmap)
    cNorm  = colors.Normalize(vmin=vmin, vmax=vmax)
    scalarmap = cmx.ScalarMappable(norm=cNorm, cmap=cm)
    vcolors = scalarmap.to_rgba(vector)
    
    return vcolors,scalarmap,cNorm
        
