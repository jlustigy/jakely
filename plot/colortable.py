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

__all__ = ["ColorTable", "test_colortable", "ColorTableLinks"]

def ColorTable(xlabels, ylabels, data, savename = None,
               labelfontsize = 18, labelrotation = 45, textsize = 18,
               spacing = 0.025, colormap = "Blues",
               fmt = "%.1f", title = None, cmin = None,
               cmax = None, xlabel = None, ylabel = None,
               xlabel_spacing = 0.00, ylabel_spacing = 0.00,
               nancolor = (0.0, 0.0, 0.0), nantext = "", titlefontsize = 20,
               data_pm = None):
    '''
    Creates a `matplotlib.pyplot` version of a simple 2D
    table, where the values in each cell are color coded
    for easy viewing.

    Parameters
    ----------
    xlabels : list or `numpy.array`
    ylabels : list or `numpy.array`
    data : `numpy.array`
    data_pm : list or tuple
        List or tuple of two `numpy.array`  e.g. ``[data_plus, data_minus]``, one
        array to display as the upper percentile and one array for the lower
        percentile.
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
    fig, ax = plt.subplots(Ny, Nx, figsize = (Nx,Ny))

    # Set title, optional
    if title is not None:
        ax[0, int(Nx/2)].set_title(title, fontsize = titlefontsize)

    # Adjust spacing
    plt.subplots_adjust(wspace=spacing, hspace=spacing)

    # Loop over grid cells
    for ix in range(Nx):
        for iy in range(Ny):

            # Remove all ticks
            ax[iy, ix].set_xticks([])
            ax[iy, ix].set_yticks([])

            # Set boxcolor by colormap
            boxcolor = smap.cmap(cnorm(data[ix, iy]))

            if np.isnan(data[ix, iy]):
                boxcolor = nancolor

            # Set the facecolor to boxcolor
            ax[iy, ix].set_facecolor(boxcolor)

            # Get RGB
            R = boxcolor[0] * 255
            G = boxcolor[1] * 255
            B = boxcolor[2] * 255

            # Calculate grey "brightness"
            grey = (R*0.299 + G*0.587 + B*0.114)

            # Set text color based on brightness
            if grey > 186:
                textcolor = "#000000"
            else:
                textcolor = "#ffffff"

            # Catch nans and infs
            if np.isfinite(data[ix, iy]):

                # Baseline text
                text = fmt %data[ix, iy]

                # Add percentile text if proided
                if data_pm is not None:
                    text += "$^{+%s}_{-%s}$" %(fmt %data_pm[0][ix,iy], fmt %data_pm[1][ix,iy])

                # Determine if greater/less than signs are needed
                if cmax is not None:
                    if data[ix, iy] > cmax:
                        text = r"$>$"+fmt %cmax
                if cmin is not None:
                    if data[ix, iy] < cmin:
                        text = r"$<$"+fmt %cmin

            else:

                # This is not a number. Use nantext
                text = nantext


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

    # Set ylabel
    if ylabel is not None:
        fig.text(ylabel_spacing, 0.5, ylabel, ha = "left", va = "center",
            fontsize=mpl.rcParams['font.size'], zorder=10, rotation = 90,
            bbox=dict(boxstyle="square", fc="none", ec="none"))

    # Set xlabel
    if xlabel is not None:
        fig.text(0.5, xlabel_spacing, xlabel, ha = "center", va = "bottom",
                fontsize=mpl.rcParams['font.size'], zorder=10,
                bbox=dict(boxstyle="square", fc="none", ec="none"))

    # Save figure, optional
    if savename is not None:
        fig.savefig(savename, bbox_inches = "tight")

    return fig, ax

def ColorTableLinks(xlabels, ylabels, data, links, savetag = None,
                    labelfontsize = 18, labelrotation = 45, textsize = 18,
                    spacing = 0.025, colormap = "Blues",
                    fmt = "%.1f", title = None, cmin = None,
                    cmax = None, xlabel = None, ylabel = None,
                    xlabel_spacing = 0.00, ylabel_spacing = 0.00,
                    nancolor = (0.0, 0.0, 0.0), titlefontsize = 20):
    '''
    Creates a `matplotlib.pyplot` version of a simple 2D
    table, where the values in each cell are color coded
    for easy viewing.
    '''

    assert len(xlabels) == data.shape[0]
    assert len(ylabels) == data.shape[1]
    assert data.shape == links.shape

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
        ax[0, int(Nx/2)].set_title(title, fontsize = titlefontsize)

    # Adjust spacing
    plt.subplots_adjust(wspace=spacing, hspace=spacing)

    # Loop over grid cells
    for ix in range(Nx):
        for iy in range(Ny):

            # Remove all ticks
            ax[iy, ix].set_xticks([])
            ax[iy, ix].set_yticks([])

            # Set boxcolor by colormap
            boxcolor = smap.cmap(cnorm(data[ix, iy]))

            if np.isnan(data[ix, iy]):
                boxcolor = nancolor

            # Set the facecolor to boxcolor
            """
            ax[iy, ix].set_facecolor(boxcolor)
            """

            # Get RGB
            R = boxcolor[0] * 255
            G = boxcolor[1] * 255
            B = boxcolor[2] * 255

            # Calculate grey "brightness"
            grey = (R*0.299 + G*0.587 + B*0.114)

            # Set text color based on brightness
            if grey > 186:
                textcolor = "#000000"
            else:
                textcolor = "#ffffff"

            # Catch nans and infs
            if np.isfinite(data[ix, iy]):
                text = fmt %data[ix, iy]
            else:
                text = "%.2f" %data[ix, iy]

            # Determine if greater/less than signs are needed
            if cmax is not None:
                if data[ix, iy] > cmax:
                    text = r"$>$"+fmt %cmax
            if cmin is not None:
                if data[ix, iy] < cmin:
                    text = r"$<$"+fmt %cmin

            # Add text to plot
            """
            ax[iy, ix].text(0.5, 0.5, text, ha="center", va="center",
                            bbox=dict(boxstyle="square", fc="w", ec="w", alpha=0.0),
                            color = textcolor)
            """

            # Using massive scatter points to color axes because set_url
            # actually works for them (as opposed to axis.set_url)
            website = links[ix, iy]
            s = ax[iy, ix].scatter([0.5,2], [0.5,5], s = 100000, c = boxcolor)
            if website is not None:
                s.set_urls([website, website])
            ax[iy, ix].set_xlim(0.4, 0.6)
            ax[iy, ix].set_ylim(0.4, 0.6)
            # Add text to plot
            atext = ax[iy, ix].text(0.5, 0.5, text, ha="center", va="center",
                            bbox=dict(boxstyle="square", fc="w", ec="w", alpha=0.0),
                            color = textcolor, fontsize = textsize)
            if website is not None:
                atext.set_url(website)

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

    # Set ylabel
    if ylabel is not None:
        fig.text(ylabel_spacing, 0.5, ylabel, ha = "left", va = "center",
            fontsize=mpl.rcParams['font.size'], zorder=10, rotation = 90,
            bbox=dict(boxstyle="square", fc="none", ec="none"))

    # Set xlabel
    if xlabel is not None:
        fig.text(0.5, xlabel_spacing, xlabel, ha = "center", va = "bottom",
                fontsize=mpl.rcParams['font.size'], zorder=10,
                bbox=dict(boxstyle="square", fc="none", ec="none"))

    # Save figure, optional
    if savetag is not None:
        fig.canvas.print_figure(savetag + '.svg', bbox_inches = "tight")

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

def test_colortable_links():
    '''
    '''

    savetag = "../examples/colortablelinks1"

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
    links = []
    for ix in range(Nx):
        for iy in range(Ny):
            data[ix, iy] = data[ix, iy] * np.fabs(np.random.randn()) * 10.0
            links.append("https://www.google.com/search?q=%s+%s" %(xlabels[ix], ylabels[iy]))

    links = np.array(links).reshape([Nx, Ny])

    fig, ax = ColorTableLinks(xlabels, ylabels, data, links, savetag = savetag)

    return
