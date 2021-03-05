import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import numpy as np

def output_graph(): #TODO: add input parameters
    # make these smaller to increase the resolution
    # dx, dy = 0.05, 0.05

    # generate 2 2d grids for the x & y bounds
    # y, x = np.mgrid[slice(1, 5 + dy, dy), slice(1, 5 + dx, dx)]

    # z = np.sin(x)**10 + np.cos(10 + y*x) * np.cos(x)    

    # ** Displayed Data **
    #TODO: create a loop to find out the value of each window
    #TODO: store the values into the array
    correlation = [] -->c_opt
    axial_strains = [] -->mxx-1
    lateral_strains = [] -->myy-1
    axial_shears = [] -->mxy
    lateral_shears = [] -->myx

    # x and y are bounds, so z should be the value *inside* those bounds.
    # Therefore, remove the last value from the z array.
    #z = z[:-1, :-1]

    levels = MaxNLocator(nbins=15).tick_values(z.min(), z.max())

    # pick the desired colormap, sensible levels, and define a normalization
    # instance which takes data values and translates those into levels.
    cmap = plt.get_cmap('Spectral')
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

    # contours are *point* based plots, so convert our bound into point
    # centers
    fig, ax0 = plt.subplots()
    im = ax0.contourf( correlation, levels=levels, cmap=cmap) #add x, y if needed
    fig.colorbar(im, ax=ax0)
    ax0.set_title('Correlation Coefficient')

    fig1, ax1 = plt.subplots()
    im_1 = ax1.contourf( axial_strains, levels=levels, cmap=cmap)
    #im_1 = ax1.contourf(x[:-1, :-1] + dx/2., y[:-1, :-1] + dy/2., axial_strains, levels=levels, cmap=cmap)
    fig1.colorbar(im_1, ax=ax1)
    ax1.set_title('Axial Strains')

    fig2, ax2 = plt.subplots()
    im_2 = ax2.contourf( lateral_strains, levels=levels, cmap=cmap)
    fig2.colorbar(im_2, ax=ax2)
    ax1.set_title('Lateral Strains')

    fig3, ax3 = plt.subplots()
    im_3 = ax3.contourf( axial_shears, levels=levels, cmap=cmap)
    fig3.colorbar(im_3, ax=ax3)
    ax1.set_title('Axial Shears')

    fig4, (ax4) = plt.subplots()
    im_4 = ax4.contourf( lateral_shears, levels=levels, cmap=cmap)
    fig4.colorbar(im_4, ax=ax4)
    ax1.set_title('Lateral Shears')

    # adjust spacing between subplots so `ax1` title and `ax0` tick labels
    # don't overlap
    #fig.tight_layout()

    plt.show()