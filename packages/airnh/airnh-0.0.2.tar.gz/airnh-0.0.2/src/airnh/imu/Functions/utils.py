import pandas as pd
import matplotlib.pyplot as plt
plt.style.use(['dark_background'])
import numpy as np
from ipywidgets import interactive, fixed, interact
np.set_printoptions(precision=3, suppress=True)
np.random.seed(123)
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

#from DataReader import *
# from DataReader_obf import *

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

def getArrow(fromXYZ=[0, 0, 0], toXYZ=[1, 1, 1], color='white'):
    return Arrow3D([fromXYZ[0], toXYZ[0]], [fromXYZ[1], toXYZ[1]], [fromXYZ[2], toXYZ[2]],
            mutation_scale=20, lw=2, arrowstyle="-|>", color=color)

def drawVerticalLine(start, end, at=0, color='balck'):
    N = 2
    x = np.ones((N,1))*at
    y = np.linspace(start, end, N)
    plt.plot(x, y, '-', color=color)
    
def drawHorizontalLine(start, end, at=0, color='balck'):
    N = 2
    y = np.ones((N,1))*at
    x = np.linspace(start, end, N)
    plt.plot(x, y, '-', color=color)
      
def drawXYCoord2D(start, end):
    plt.xlim(start, end)
    plt.ylim(start, end)
    drawVerticalLine(start, end, at=0, color='w')
    drawHorizontalLine(start, end, at=0, color='w')
    plt.minorticks_on()
    plt.grid(b=True, which='major', color='grey', linestyle='--')

def drawCircle2D(x, y, r):
    x = np.linspace(x-r, x+r, 100)
    y1 = np.sqrt(r-x**2)
    y2 = -np.sqrt(r-x**2)
    plt.plot(x, y1, 'w-')
    plt.plot(x, y2, 'w-')
    
def reset3DFigure(ax, xlabel='', ylabel='', zlabel=''):
    ax.clear()
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
        
def get3DFigure(title='', xlabel='', ylabel='', zlabel=''):
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, projection='3d')
    reset3DFigure(ax, xlabel, ylabel, zlabel)
    plt.title(title)    
    return fig, ax

def interactiveCrossProduct(foo):
    fig, ax = get3DFigure('Cross Product', 'X', 'Y', 'Z')
    def update(degree=-45):
        reset3DFigure(ax)
        ang = degree*np.pi/180
        p0 = np.array([1, 0, 0])
        p1 = np.array([np.cos(ang), -np.sin(ang), 0])
        p2 = foo(p0, p1)
        #p2 = np.cross(p0, p1)

        ax.add_artist(getArrow(np.zeros((3,)), p0, color='g'))
        ax.add_artist(getArrow(np.zeros((3,)), p1, color='b'))
        ax.add_artist(getArrow(np.zeros((3,)), p2, color='r'))
        fig.canvas.draw_idle()
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Cross Product')
        print(f"green:")

    interact(update, degree=(-90, 90, 0.1))
        
def plotXYZ(data, timeStamp=None, title=None, ylabel=None, xlabel=None, alone=True, style='-'):
    if alone:
        plt.figure()
    if title is not None:
        plt.title(title)
    
    toPlot = []
    for i in range(0, 3):
        toPlot.append([data[:, i]])
        if timeStamp is not None:
            if (i==0):
                plt.xlabel('Time, sec')
            toPlot[i].insert(0, timeStamp)
    plt.plot(*toPlot[0], 'g', linestyle=style, label='X')
    plt.plot(*toPlot[1], 'b', linestyle=style, label='Y')
    plt.plot(*toPlot[2], 'r', linestyle=style, label='Z')
    if ylabel is not None:
        plt.ylabel(ylabel)
    else:
        if xlabel is not None:
            plt.xlabel(xlabel)
    plt.legend()
    if alone:
        plt.show()
