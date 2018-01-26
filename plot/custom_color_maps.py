from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as colors

__all__ = ["create_linear_colormap"]

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
