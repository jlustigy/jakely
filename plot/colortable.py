import os
import sys
import numpy as np
import scipy as sp
import scipy.optimize
import matplotlib as mpl
import matplotlib.colors as colors
import matplotlib.pyplot as plt
from matplotlib import gridspec, rc, ticker

sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from colorize import colorize

import platform
if platform.system() == 'Darwin':
    mpl.rc('font',**{'family':'serif','serif':['Computer Modern']})
    mpl.rc('text', usetex=True)
else:
    mpl.rc('font', family='Times New Roman')
    mpl.rc('text', usetex=False)

__all__ = ["ColorTable", "test_colortable"]

def ColorTable(xlabels, ylabels, data, savename = None,
               labelfontsize = 18, labelrotation = 45,
               spacing = 0.025, colormap = "Blues",
               fmt = "%.1f", title = None, cmin = None,
               cmax = None):
    '''
    Creates a `matplotlib.pyplot` version of a simple 2D
    table, where the values in each cell are color coded
    for easy viewing.
    '''

    assert len(xlabels) == data.shape[0]
    assert len(ylabels) == data.shape[1]

    # Dimensions
    Nx = len(xlabels)
    Ny = len(ylabels)

    # Create vector from 2d data
    datav = data.reshape([-1])

    # Get colormap for data range
    vcolors, smap, cnorm = colorize(datav, cmap=colormap, vmin = cmin,
                                    vmax = cmax)

    # Create figure
    fig, ax = plt.subplots(Ny ,Nx, figsize = (Nx,Ny))

    # Set title, optional
    if title is not None:
        fig.suptitle(title, va = "top")

    # Adjust spacing
    plt.subplots_adjust(wspace=spacing, hspace=spacing)

    # Loop over grid cells
    for ix in range(Nx):
        for iy in range(Ny):

            # Remove all ticks
            ax[iy, ix].set_xticks([])
            ax[iy, ix].set_yticks([])

            # Set boxcolor
            boxcolor = smap.cmap(cnorm(data[ix, iy]))
            ax[iy, ix].set_facecolor(boxcolor)

            # Get RGB
            R = smap.cmap(cnorm(data[ix, iy]))[0] * 255
            G = smap.cmap(cnorm(data[ix, iy]))[1] * 255
            B = smap.cmap(cnorm(data[ix, iy]))[2] * 255

            # Calculate grey "brightness"
            grey = (R*0.299 + G*0.587 + B*0.114)

            # Set text color based on brightness
            if grey > 186:
                textcolor = "#000000"
            else:
                textcolor = "#ffffff"

            # Determine if greater/less than signs are needed
            text = fmt %data[ix, iy]
            if cmax is not None:
                if data[ix, iy] > cmax:
                    text = r"$>$"+fmt %cmax
            if cmin is not None:
                if data[ix, iy] < cmin:
                    text = r"$<$"+fmt %cmin

            # Add text to plot
            ax[iy, ix].text(0.5, 0.5, text, ha="center", va="center",
                            bbox=dict(boxstyle="square", fc="w", ec="w", alpha=0.0),
                            color = textcolor)

            # Get rid of the axis frame
            for spine in ax[iy, ix].spines.values():
                spine.set_visible(False)

    # Loop over x
    for ix in range(Nx):
        # Set tick to be in middle
        ax[-1,ix].set_xticks([0.5])
        # Set tick label by user provided
        ax[-1,ix].set_xticklabels([xlabels[ix]], rotation = labelrotation, fontsize = labelfontsize, ha = "right")

    # Loop over y
    for iy in range(Ny):
        # Set tick to be in middle
        ax[iy,0].set_yticks([0.5])
        # Set tick label by user provided
        ax[iy,0].set_yticklabels([ylabels[iy]], rotation = labelrotation, fontsize = labelfontsize, ha = "right")

    # Save figure, optional
    if savename is not None:
        fig.savefig(savename, bbox_inches = "tight")

    return fig, ax

def test_colortable():
    '''
    '''

    # Dimensions
    Nx = 7
    Ny = 4

    try:

        # Generate random word
        import requests
        word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
        response = requests.get(word_site)
        WORDS = response.content.splitlines()

        # Set label names
        xlabels = [np.random.choice(WORDS) for i in range(Nx)]
        ylabels = [np.random.choice(WORDS) for i in range(Ny)]
    except:

        # Default back to boring test names
        xlabels = ["x-name %i" %(i+1) for i in range(Nx)]
        ylabels = ["y-name %i" %(i+1) for i in range(Ny)]

    # Create test data
    data = np.ones([Nx, Ny])
    for ix in range(Nx):
        for iy in range(Ny):
            data[ix, iy] = data[ix, iy] * np.fabs(np.random.randn()) * 10.0


    fig, ax = ColorTable(xlabels, ylabels, data)

    fig.subplots_adjust(bottom=0.25, left=0.25)

    plt.show()

    return
