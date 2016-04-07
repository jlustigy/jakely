import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

from jakely import colorize

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
    PC_plot_lims = [(np.floor(np.min(PCs[:,i])), np.ceil(np.max(PCs[:,i]))) for i in range(N)]
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
