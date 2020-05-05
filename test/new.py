from windrose import WindroseAxes
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from numpy.random import random
from numpy import arange

ws = random(500) * 6
wd = random(500) * 360


# A quick way to create new windrose axes...
def new_axes():
    fig = plt.figure(figsize=(8, 8), dpi=80, facecolor='w', edgecolor='w')
    rect = [0.1, 0.1, 0.8, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax


# ...and adjust the legend box
def set_legend(ax):
    l = ax.legend(shadow=True, bbox_to_anchor=[-0.1, 0], loc='lower left')
    plt.setp(l.get_texts(), fontsize=10)


ax = new_axes()
ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
set_legend(ax)
plt.show()