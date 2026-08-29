import matplotlib.pyplot as plt
import pandas as pd

def plt_style(font_size, font):
    plt.style.use("seaborn-v0_8-paper")
    plt.rcParams.update({        
        "font.family": font,
        "font.size": font_size,
        "axes.titlesize": font_size*1.7,
        "axes.labelsize": font_size*1.2,
        "xtick.labelsize": font_size,
        "ytick.labelsize": font_size,
        "legend.fontsize": font_size,
        "figure.titlesize": font_size})
    
def plot_zoom(zoom, X, Y):
    
    xmin = min(X)
    xmax = max(X)
    xavg = (xmin + xmax)/2
    xran = xmax - xmin
    
    ymin = min(Y)
    ymax = max(Y)
    yavg = (ymin + ymax)/2
    yran = ymax - ymin
    
    plot_range =  max([xran, yran]) + zoom
    plt.set_xlim(xavg - plot_range/2, xavg + plot_range/2)
    plt.set_ylim(yavg - plot_range/2, yavg + plot_range/2)
    
def plot_polar(X, Y, title, zoom=0):
    plt.plot(X, Y)
    plt.title(title)
    plt.xlabel(X.name)
    plt.ylabel(Y.name)
    
    if zoom != 0:
        plot_zoom(zoom, X, Y)

    plt.grid(True)
    plt.show()
    
def plot_polar_pro(X, Y, title, minorticks=True, zoom=0):
    plt_style(15, "Garamond")
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    ax.plot(X, Y, color="#6a408d")
    
    ax.set_title(title)
    ax.set_xlabel(X.name)
    ax.set_ylabel(Y.name)
    
    if Y.name == "L/D":
        opt_point(ax, X, Y, "L/D Max", "#9671bd", maxi=True)
        
    elif Y.name == "CL":
        opt_point(ax, X, Y, "CL Max", "#9671bd", maxi=True)
        
    elif Y.name == "CD":
        opt_point(ax, X, Y, "CD Min", "#9671bd", maxi=False)
    
    #ax.set_aspect('equal', adjustable='datalim')
    ax.grid(True, which='major', linestyle='-', linewidth=0.75, alpha=0.25)
    if minorticks:
        ax.minorticks_on()
        ax.grid(True, which='minor', linestyle='-', linewidth=0.25, alpha=0.15)
    ax.set_axisbelow(True)
    
    if zoom != 0:
        plot_zoom(zoom, X, Y)

    plt.show()
    
def opt_point(ax, X, Y, lab, col, maxi):
    index = lambda n: n.idxmax() if maxi else n.idxmin()
    
    ax.axvline(x=X[index(Y)], linestyle="dotted", color=col, alpha=0.85, label=f"{X.name} = {X[index(Y)]}")
    ax.axhline(y=Y[index(Y)], linestyle="dotted", color=col, alpha=0.85, label=f"{lab} = {Y[index(Y)]:.4f}")
    ax.scatter(X[index(Y)], Y[index(Y)], color='r', zorder=10)
    ax.legend()