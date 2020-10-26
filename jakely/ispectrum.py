from __future__ import (division as _, print_function as _,
                absolute_import as _, unicode_literals as _)

from colorpy import colormodels, ciexyz
from .plot import set_figure_colors
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import gridspec
import os

__all__ = ["irgb_string_from_spectrum", "make_color_swatch", "plot_response",
           "rgb_from_wavelength", "plot_spectrum"]

def irgb_string_from_spectrum(wl, spectrum):
    """
    Calculates the irgb color given a wavelengh [nm] vs intensity [W/m*m/um]
    spectrum in the visible.
    """
    # Filter possible nans
    ifin = np.isfinite(spectrum)
    wl = wl[ifin]
    spectrum = spectrum[ifin]
    # Run through ColorPy
    spec = np.vstack([wl, spectrum]).T
    rgb_eye = colormodels.irgb_string_from_rgb (
        colormodels.rgb_from_xyz (ciexyz.xyz_from_spectrum (spec)))
    return rgb_eye

def make_color_swatch(**kwargs):
    """
    Generates a little rectangular swatch of the color given. Note that this
    function accepts only keyword arguments for the Rectangle object.

    Ex:
        swatch = make_color_swatch(color="orange")
    """
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    rect = plt.Rectangle((0.0, 0.0), 1, 1, **kwargs)
    ax.add_patch(rect)
    plt.axis('off')
    return fig

def plot_response(ax=None, wlmin=350, wlmax=750, **kwargs):
    """
    Adds human eye response curves to an axis.
    """
    relpath = "../colorvision/eye_response_functions/ciexyz31_1.csv"
    fn = os.path.join(os.path.dirname(__file__), relpath)
    data = np.genfromtxt(fn, delimiter=',')
    wl = data[:,0]
    mask = (wl >= wlmin) & (wl <= wlmax)
    wl = wl[mask]
    x = data[mask,1]
    y = data[mask,2]
    z = data[mask,3]

    yscale = 1.0

    # Create new axis if not specified, otherwise add twinx to current figure
    if ax is None:
        fig = plt.figure(figsize=(12,8))
        gs = gridspec.GridSpec(1,1)
        ax = plt.subplot(gs[0])
    else:
        ax = ax.twinx()
        ax.set_ylim([0.0,10.0])
        ax.axes.get_yaxis().set_visible(False)

    # Plot response functions
    ax.plot(wl,x, color='white', label=r'x', alpha=1, lw=2.0)
    ax.plot(wl,y, color='white', label=r'y', alpha=1, lw=2.0)
    ax.plot(wl,z, color='white', label=r'z', alpha=1, lw=2.0)


def rgb_from_wavelength(wl):
    """
    Get rgb colors for each wavelength [nm]
    """
    num_wl = len(wl)
    rgb_colors = np.empty ((num_wl, 3))
    for i in range (0, num_wl):
        wl_nm = wl[i]
        xyz = ciexyz.xyz_from_wavelength (wl_nm)
        rgb_colors [i] = colormodels.rgb_from_xyz (xyz)
    # scale to make brightest rgb value = 1.0
    rgb_max = np.max (rgb_colors)
    scaling = 1.0 / rgb_max
    rgb_colors *= scaling
    return rgb_colors

def plot_spectrum(wl, spectrum,
                  wlmin=350, wlmax=750,
                  stellar_spec=None,
                  show_cie=False,
                  xtitle="Wavelength [nm]",
                  ytitle="Intensity",
                  title="",
                  **kwargs):
    """
    Plots intensity [W/m*m/um] vs wavelength [nm] across the visible, shading the
    background above the curve the color the human eye would perceive, and the
    entire visible spectrum below the curve. Returns Figure object for saving
    and further artistry.


    Parameters
    ----------
    wl : array
        Wavelength grid [nm]
    spectrum : array
        Intensity spectrum [W / m^2 / um]
    wlmin : float
        Minimum wavelength plotted [nm]
    wlmax : float
        Maximum wavelength plotted [nm]
    show_cie : bool
        Adds overplotted CIE eye sensitivity curves for reference
    xtitle : str
        x-axis label
    ytitle : str
        y-axis label
    title : str
        Plot title

    Returns
    -------
    matplotlib.figure.Figure
    """

    if np.min(wl) > wlmin: wlmin = np.min(wl)
    if np.max(wl) < wlmax: wlmax = np.max(wl)

    # Mask wl region
    mask = (wl >= wlmin) & (wl <= wlmax)
    wl = wl[mask]
    spectrum = spectrum[mask]

    # Filter possible nans
    ifin = np.isfinite(spectrum)
    wl = wl[ifin]
    spectrum = spectrum[ifin]

    # Read-in solar spectrum
    if stellar_spec is None:
        pass
    elif stellar_spec == "Sun":
        data = np.genfromtxt("spectra/earth_quadrature_radiance_refl.dat", skip_header=8)
        wl_solar = data[:,0] * 1000.0 # Convert microns to nm
        F_solar = data[:,2]
        # Interpolate sun to CMF
        F_solar = np.interp(wl, wl_solar, F_solar)
        # Multiply Albedo and Flux
        spectrum = spectrum * F_solar
    else:
        print("Given stellar_spec is not included.")

    # Convert Flux to photon counts
    umnm = 1e-3
    hc    = 1.986446e-25  # h*c (kg*m**3/s**2)
    #spectrum = spectrum * umnm * wl / hc

    # Plot spectrum
    fig = plt.figure(figsize=(12,8))
    gs = gridspec.GridSpec(1,1)
    ax1 = plt.subplot(gs[0])
    ax1.set_xlim([wlmin, wlmax])

    num_wl = len(wl)

    #
    rgb_colors = rgb_from_wavelength(wl)

    #
    spec = np.vstack([wl, spectrum]).T
    rgb_eye = colormodels.irgb_string_from_rgb (
        colormodels.rgb_from_xyz (ciexyz.xyz_from_spectrum (spec)))

    # draw color patches (thin vertical lines matching the spectrum curve) in color
    for i in range (0, num_wl-1):    # skipping the last one here to stay in range
        x0 = wl [i]
        x1 = wl [i+1]
        y0 = spectrum [i]
        y1 = spectrum [i+1]
        poly_x = [x0,  x1,  x1, x0]
        poly_y = [0.0, 0.0, y1, y0]
        color_string = colormodels.irgb_string_from_rgb (rgb_colors[i])
        ax1.fill (poly_x, poly_y, color_string, edgecolor=color_string)

    # plot intensity as a curve
    ax1.plot (
        wl, spectrum,
        color='k', linewidth=1.0, antialiased=True)

    # plot CIE response curves
    if show_cie:
        plot_response(ax=ax1, wlmin=wlmin, wlmax=wlmax)

    ax1.set_xlabel(xtitle)
    ax1.set_ylabel(ytitle)
    ax1.set_title(title)
    ax1.set_xlim([wlmin, wlmax])

    # Set plot background color to derived rgb color
    #set_figure_colors(fig, foreground="white", background="black")
    ax1.patch.set_facecolor(rgb_eye)

    return fig
