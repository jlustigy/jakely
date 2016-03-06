# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 13:31:55 2016

@author: jlustigy
"""

import numpy as np
from jakely import colorize
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import gridspec

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
    #print 'r =', rad

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
            print "Error: No points found in hexbin"
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
        print "Error: Either pass all axes or none"
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