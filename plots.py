import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from scipy.interpolate import CubicSpline
import numpy as np


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
    
def N_name(data, N):
    for n, i in enumerate(data.values()):
        if (i==N).all():
            return list(data.keys())[n]    

def opt_point(ax, data, X, Y, lab, col, maxi):
    index = lambda n: np.argmax(n) if maxi else np.argmin(n)
    X_name = N_name(data, X)
    
    ax.axvline(x=X[index(Y)], linestyle="dotted", color=col, alpha=0.85, label=f"{X_name} = {X[index(Y)]}")
    ax.axhline(y=Y[index(Y)], linestyle="dotted", color=col, alpha=0.85, label=f"{lab} = {Y[index(Y)]:.4f}")
    ax.scatter(X[index(Y)], Y[index(Y)], color='r', zorder=10)
    ax.legend()
    
def cubic_interp(X, Y, n=10):
    spline = CubicSpline(X, Y)
    X_new = np.linspace(X[0], X[-1], n*len(X))
    Y_new = spline(X_new)
    return X_new, Y_new


def plot_polar_pro(data, X, Y, title, minorticks=True):
    plt_style(15, "Garamond")
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    #X_new, Y_new = cubic_interp(X, Y)
    
    ax.plot(X, Y, color="#6a408d")
    #ax.plot(X_new, Y_new, color="#6a408d")
    
    X_name = N_name(data, X)
    Y_name = N_name(data, Y)
    
    ax.set_title(title)
    ax.set_xlabel(X_name)
    ax.set_ylabel(Y_name)
    
    if X_name != 'Panels':
        if Y_name == "L/D":
            opt_point(ax, data, X, Y, "L/D Max", "#9671bd", maxi=True)
            
        elif Y_name == "CL":
            opt_point(ax, data, X, Y, "CL Max", "#9671bd", maxi=True)
            
        elif Y_name == "CD":
            opt_point(ax, data, X, Y, "CD Min", "#9671bd", maxi=False)
            
    
    ax.grid(True, linestyle='-', linewidth=0.75, alpha=0.25)
    if minorticks:
        ax.minorticks_on()
        ax.grid(True, which='minor', linestyle='-', linewidth=0.25, alpha=0.15)
    ax.set_axisbelow(True)

    plt.show()
    
def plot_airfoil(data, X, Y, title):
    plt_style(15, "Garamond")
    
    fig, ax = plt.subplots()
    
    new_X = [X[n] for n in range(0, len(X), 5)]
    new_Y = [Y[n] for n in range(0, len(Y), 5)]
    
    X_name = N_name(data, X)
    Y_name = N_name(data, Y)
    
    ax.plot(X, Y, color="#6a408d")
    ax.scatter(new_X, new_Y, s=10, color='red', zorder=10)
    
    ax.set_title(title)
    ax.set_xlabel(X_name)
    ax.set_ylabel(Y_name)
    ax.set_aspect('equal')
    ax.grid(True, which='major', linestyle='-', linewidth=0.75, alpha=0.25)

    ax.minorticks_on()
    ax.grid(True, which='minor', linestyle='-', linewidth=0.25, alpha=0.15)
    ax.set_axisbelow(True)
    
    yavg = (min(Y) + max(Y))/2
    ax.set_ylim(yavg - (max(Y)-min(Y))*1.2, yavg + (max(Y)-min(Y))*1.2)

    plt.show()