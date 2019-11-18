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
