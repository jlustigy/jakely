from __future__ import (division as _, print_function as _,
                absolute_import as _, unicode_literals as _)
                
import os, sys
import numpy as np
import scipy as sp
import scipy.optimize
import matplotlib as mpl
from matplotlib import gridspec
import matplotlib.colors as colors
import matplotlib.cm as cmx
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
from matplotlib import gridspec, rc, ticker

__all__ = ["PCA_corner", "ColorTable", "test_colortable", "ColorTableLinks",
           "plot_hexbin_dots", "add_hexbin_points", "colorize",
           "set_foregroundcolor", "set_backgroundcolor", "set_figure_colors",
           "determine_contrasting_color"]

def PCA_corner(x, y, lowdim, color=None, N=None, size=5, xlabel="", ylabel="", hcolor="black"):
    """Plot all the extracted PCA dimensionality reduced projections against one
    another, as well as a scatter plot with user specified physical axes. The color
    of each point is consistent across all subplots.

    Parameters
    ----------
    x : array
        X-values for 'physical' plot
    y : array
        Y-values for 'physical' plot (same length as x)
    lowdim : 2D array
        PCA reduced dimensionality projections, with shape MxN where M is the number
        of samples (same length as x) and N is the number of principle components
        e.g. lowdim = pca.transform(data);
    color : array (optional)
        Color values for each sample (same length as x)
    N : int (optional)
        Number of PCs to plot against each other
    size : float or int (optional)
        Marker size for scatter points
    xlabel : str (optional)
        Label for x-axis on 'physical' plot
    ylabel : str (optional)
        Label for y-axis on 'physical' plot
    hcolor : str
        Color of line of histograms

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure which can be saved, etc
    """

    if N is None:
        N = len(lowdim[0,:])
    elif N > len(lowdim[0,:]):
        N = len(lowdim[0,:])
        print("Error: User specified N > len(lowdim[0,:]). Setting N = len(lowdim[0,:])")
    else:
        pass

    PCs = np.copy(lowdim)

    if color is None:
        print("Error: No colors provided. Setting colors to y")
        c,scalarMap,cNorm = colorize(y, cmap="viridis")
    else:
        c = color


    # Set Params
    PC_labels = ['PC'+str(i+1) for i in range(N)]
    PC_plot_lims = [(np.min(PCs[:,i]), np.max(PCs[:,i])) for i in range(N)]
    figlen = (N+1)*2
    subN = int(np.floor(N/2.0))

    # Set gridspace index tuning params
    if np.mod(N,2) != 0:
        val1 = 0
        val2 = 1
    else:
        val1 = 0
        val2 = 0

    # Use matrix for plot gridspace logic
    matrix = np.diag([True for i in range(N)])

    # Create figure
    fig = plt.figure(figsize=(figlen,figlen))
    gs = gridspec.GridSpec(N,N)

    # Create Physical plot in upper right pos
    # Note different treatment if odd vs even N
    if np.mod(N,2) == 0:
        ax0 = plt.subplot(gs[:subN+val1,subN+val2:])
        ax0.xaxis.set_label_position('top')
        ax0.yaxis.set_label_position('right')
        ax0.xaxis.set_ticks_position('top')
        ax0.yaxis.set_ticks_position('right')
        plt.setp(ax0.get_xticklabels(), fontsize=14, rotation=45)
        plt.setp(ax0.get_yticklabels(), fontsize=14, rotation=45)
        ax0.scatter(x, y, c=c, s=size, lw=0)
        ax0.set_xlabel(xlabel)
        ax0.set_ylabel(ylabel, rotation=270, labelpad=25)
    else:
        ax0 = plt.subplot(gs[:subN+val1,subN+val2:])
        plt.setp(ax0.get_xticklabels(), fontsize=14, rotation=45)
        plt.setp(ax0.get_yticklabels(), fontsize=14, rotation=45)
        ax0.scatter(x, y, c=c, s=size, lw=0)
        ax0.set_xlabel(xlabel)
        ax0.set_ylabel(ylabel)

    # Loop over y
    for i in range(N):
        # Set on for left of diagonal
        on = True
        # Loop over x
        for j in range(N):
            if matrix[i,j]:
                # Diagonal: Histograms
                ax = plt.subplot(gs[i,j])
                ax.hist(PCs[:,j], normed=True, histtype='step', color=hcolor, lw=1.0)
                ax.set_xlim(PC_plot_lims[j])
                plt.setp(ax.get_xticklabels(), fontsize=14, rotation=45)
                plt.setp(ax.get_yticklabels(), fontsize=14, rotation=45)
                if (i != N-1) and (j != N-1):
                    ax.set_xticklabels([])
                else:
                    ax.set_xlabel(PC_labels[-1])
                ax.set_yticklabels([])
                # Flip the switch
                if on:
                    on = False
                else:
                    on = True
            elif on:
                # Left of diagonal: Scatter plots
                ax = plt.subplot(gs[i,j])
                xx = PCs[:,j]
                yy = PCs[:,i]
                ax.scatter(xx, yy, c=c, s=size, lw=0)
                ax.set_xlim(PC_plot_lims[j])
                ax.set_ylim(PC_plot_lims[i])
                plt.setp(ax.get_xticklabels(), fontsize=14, rotation=45)
                plt.setp(ax.get_yticklabels(), fontsize=14, rotation=45)
                if i != N-1:
                    ax.set_xticklabels([])
                    pass
                else:
                    ax.set_xlabel(PC_labels[j])
                if j != 0:
                    ax.set_yticklabels([])
                else:
                    ax.set_ylabel(PC_labels[i])
            else:
                # Right of diagonal: Do nothing.
                pass
    return fig

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
        ax[-1,ix].set_xticklabels([xlabels[ix]], rotation = labelrotation,
                                  fontsize = labelfontsize, ha = "right")

    # Loop over y
    for iy in range(Ny):
        # Set tick to be in middle
        ax[iy,0].set_yticks([0.5])
        # Set tick label by user provided
        ax[iy,0].set_yticklabels([ylabels[iy]], rotation = labelrotation,
                                 fontsize = labelfontsize, ha = "right")

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

def create_linear_colormap(c1 = "white", c2 = "C4", c3 = None, N = 1000, cmap_name = "custom_cmap"):
    """
    Creates a colormap with a linear gradient between two user-specified colors

    Parameters
    ----------
    c1 : str
        Color of the smallest value
    c2 : str
        Color of the largest/middle value
    c3 : str
        Color of the largest value
    N : int
        Color resolution
    cmap_name : str
        Name of new colormap

    Returns
    -------
    cm : matplotlib.colors.LinearSegmentedColormap
        New colormap
    """

    # If a third color was not specified
    if c3 is None:

        # Create list with two end-member RGBA color tuples
        c = [colors.colorConverter.to_rgba(c1), colors.colorConverter.to_rgba(c2)]

    else:

        # Create list with two end-member RGBA color tuples
        c = [colors.colorConverter.to_rgba(c1), colors.colorConverter.to_rgba(c2), colors.colorConverter.to_rgba(c3)]

    # Create the colormap
    cm = LinearSegmentedColormap.from_list(cmap_name, c, N = N)

    return cm

def add_hexbin_points(ax,h,Nx,Ny,cval,ms=2., cmap='Greys'):

    padfrac = 4.0
    counts = h.get_array()
    verts = h.get_offsets()

    colors,scalarMap,cNorm = colorize(cval,cmap=cmap)
    N = len(cval)

    # Calculate distance between all verticies
    Nv = len(verts)
    x,y = verts[:,0],verts[:,1]
    dist = np.zeros([Nv,Nv])
    for i in range(Nv):
        for j in range(Nv):
            if i!=j:
                dist[i,j] = np.sqrt((x[i] - x[j])**2. + (y[i] - y[j])**2.)
            else:
                dist[i,j] = np.inf

    # Minimum distance / 2 = cell "radius"
    rad = (np.min(dist) / 2) + (np.min(dist) / padfrac)

    # Calculate the distance between each vertex and all scatter points
    dist2 = np.zeros([Nv,N])
    for i in range(Nv):
        for j in range(N):
            dist2[i,j] = np.sqrt((x[i] - Nx[j])**2. + (y[i] - Ny[j])**2.)

    # For each vertex, check which scatter points lie within a circle of radius rad
    ptcolor = np.ones([Nv,4])
    for i in range(Nv):
        # isolate points within radius
        tmask = dist2[i,:] < rad
        # if there are no points in radius (there should be points!)
        if np.sum(tmask) == 0:
            # Set color to red for error
            ptcolor[i,:] = [1.0,0.0,0.0,1.0]
            print("Error: No points found in hexbin")
        # otherwise set color to median value of points within radius
        else:
            ptcolor[i,:] = scalarMap.to_rgba(np.median(cval[tmask]))

    for offc in xrange(verts.shape[0]):
        binx,biny = verts[offc][0],verts[offc][1]
        if counts[offc]:
            ax.plot(binx,biny,'o',zorder=100, ms=ms, color=ptcolor[offc], markeredgecolor=ptcolor[offc])

def plot_hexbin_dots(x,y,z,ax=None,cbar_ax1=None,cbar_ax2=None,cmap_bin='Spectral_r', cmap_dots='Greys',\
                     dotsize=4., label_hex='N per Hex', label_dots='Median Value per Hex',\
                     gridsize=25, cbar1_orientation='horizontal',\
                     cbar2_orientation='vertical'):

    # Create figure if axes not passed as kwargs
    if (ax==None) & (cbar_ax1==None) & (cbar_ax2==None):
        fig = plt.figure(figsize=(11,10))
        gs = gridspec.GridSpec(2,2, height_ratios=[.1,1], width_ratios=[1,.1])
        cbar_ax1 = plt.subplot(gs[0])
        cbar_ax1.set_xlabel(r"", labelpad=-100)
        cbar_ax2 = plt.subplot(gs[3])
        cbar_ax2.set_ylabel('', rotation=270, labelpad=25)
        ax = plt.subplot(gs[2])
        ret = True
    elif (ax==None) or (cbar_ax1==None) or (cbar_ax2==None):
        print("Error: Either pass all axes or none")
        return
    else:
        fig = ax.get_figure()
        ret = False
        pass


    alpha1 = 0.8

    # Set dot colors
    colors,scalarMap,cNorm = colorize(z,cmap=cmap_dots)

    # Create hexbins
    h0 = ax.hexbin(x,y, alpha=alpha1, cmap=cmap_bin,gridsize=gridsize, mincnt=1)

    # Add hexbin dots
    add_hexbin_points(ax, h0, x, y, z, ms=dotsize)

    # Set hexbin colorbar
    cb1 = fig.colorbar(h0, cax=cbar_ax1, orientation=cbar1_orientation)
    cb1.set_label(label_hex)
    # Set dot colorbar
    cb2 = mpl.colorbar.ColorbarBase(cbar_ax2, cmap=cmap_dots, norm=cNorm, orientation=cbar2_orientation)
    cb2.set_label(label_dots)

    # Return figure object if just created
    if ret:
        return fig
    else:
        return

def colorize(vector, cmap='plasma', vmin=None, vmax=None):
    """
    Convert a vector to RGBA colors.

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

    return vcolors, scalarmap, cNorm

def set_foregroundcolor(ax, color):
    """For the specified axes, sets the color of the frame,
    major ticks, tick labels, axis labels, title and legend.

    Originally written by jasonmc: https://gist.github.com/jasonmc/1160951

    Parameters
    ----------
    ax : matplotlib.pyplot axis object
        Figure axis
    color : str
        matplotlib acceptable color
    """
    for tl in ax.get_xticklines() + ax.get_yticklines():
         tl.set_color(color)
    for spine in ax.spines:
         ax.spines[spine].set_edgecolor(color)
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_color(color)
    for tick in ax.yaxis.get_major_ticks():
         tick.label1.set_color(color)
    ax.axes.xaxis.label.set_color(color)
    ax.axes.yaxis.label.set_color(color)
    ax.axes.xaxis.get_offset_text().set_color(color)
    ax.axes.yaxis.get_offset_text().set_color(color)
    ax.axes.title.set_color(color)
    lh = ax.get_legend()
    if lh != None:
        lh.get_title().set_color(color)
        lh.legendPatch.set_edgecolor('none')
        labels = lh.get_texts()
        for lab in labels:
            lab.set_color(color)
    for tl in ax.get_xticklabels():
        tl.set_color(color)
    for tl in ax.get_yticklabels():
        tl.set_color(color)


def set_backgroundcolor(ax, color):
    """Sets the background color of the current axes (and legend).
    Use 'None' (with quotes) for transparent. To get transparent
    background on saved figures, use:
    pp.savefig("fig1.svg", transparent=True)

    Originally written by jasonmc: https://gist.github.com/jasonmc/1160951

    Parameters
    ----------
    ax : matplotlib.pyplot axis object
        Figure axis
    color : str
        matplotlib acceptable color
    """
    ax.patch.set_facecolor(color)
    lh = ax.get_legend()
    if lh != None:
         lh.legendPatch.set_facecolor(color)

def set_figure_colors(fig, foreground="white", background="black"):
    """Sets the background, foreground, and facecolor of all axes
    belonging to figure

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure for which to change colors
    foreground : str
        color to set plot forground (axes lines, ticks, labels, etc)
    background : str
        color to set plot background and facecolor
        Can use 'None' for transparent.
    """
    for ax in fig.axes:
        set_foregroundcolor(ax, foreground)
        set_backgroundcolor(ax, background)

    fig.set_facecolor(background)

def determine_contrasting_color(color):
    """
    Given a color, determine whether black or white contrasts better with the
    color's grayscale value. This is useful for determining the color of text
    that should be used on top of a color.

    Parameters
    ----------
    color : list or tuple
        RGB color

    Returns
    -------
    textcolor : str
        A string hex color that is either black or white
    """

    # Get RGB
    R = color[0] * 255
    G = color[1] * 255
    B = color[2] * 255

    # Calculate grey "brightness"
    grey = (R*0.299 + G*0.587 + B*0.114)

    # Set text color based on brightness
    if grey > 186:
        textcolor = "#000000"
    else:
        textcolor = "#ffffff"

    return textcolor
