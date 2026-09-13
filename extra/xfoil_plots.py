import numpy as np
import matplotlib.pyplot as plt
#from scipy.interpolate import CubicSpline

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
    
#def cubic_interp(X, Y, n=10):
#    spline = CubicSpline(X, Y)
#    X_new = np.linspace(X[0], X[-1], n*len(X))
#    Y_new = spline(X_new)
#    return X_new, Y_new
    
#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------
        
def plot_airfoil(dump, N=5):
    plt_style(15, "Garamond")

    X = dump['x']
    Y = dump['y']

    new_X = [X[n] for n in range(0, len(X), N)]
    new_Y = [Y[n] for n in range(0, len(Y), N)]

    X_name = N_name(dump, X)
    Y_name = N_name(dump, Y)

    fig, ax = plt.subplots(figsize=(8, 2.5))

    ax.plot(X, Y, color="#6a408d")
    ax.scatter(new_X, new_Y, s=10, color='red', zorder=10)

    ax.minorticks_on()
    ax.grid(True, which='major', linestyle='-', linewidth=0.75, alpha=0.25)
    ax.grid(True, which='minor', linestyle='-', linewidth=0.25, alpha=0.15)

    ax.set(xlabel=X_name, ylabel=Y_name, aspect='equal', axisbelow=True)
    ax.set_title("Airfoil")

    yavg = (min(Y) + max(Y))/2
    ax.set_ylim(yavg - (max(Y)-min(Y))*1.2, yavg + (max(Y)-min(Y))*1.2)
    
    plt.show()
    
def plot_polar_dump(var, data):
    plt_style(15, "Garamond")

    if var == 'polar':
        var = [("alpha","Cl"), ("alpha","Cd"), ("alpha","L/D"), ("alpha","Cm"), ("Cd","Cl")]
    if var == 'dump':
        var = [('x', 'Cp'), ('x', 'Ue/Vinf'), ('x', 'Theta'), ('x', 'Cf'), ('x', 'H')]
    
    if any("x" in i for i in var):
        plot_airfoil(data)
    
    for n in var:
        
        fig, ax = plt.subplots(figsize=(8, 8))
        
        X = data[n[0]]
        Y = data[n[1]]
        
        X_name = N_name(data, X)
        Y_name = N_name(data, Y)
        
        if X_name == 'x':
            
            TE = np.argmin(np.abs(X[1:]-1))+1
            LE = np.argmin(X)
            
            foil = X[:TE+1]
            new_Y = Y[:TE+1]
            
            X_upper = foil[:LE+1]
            X_lower = foil[LE:]
            
            Y_upper = new_Y[:LE+1]
            Y_lower = new_Y[LE:]
            
            ax.plot(X_upper, Y_upper, color="#6a408d", label='Suction Side')
            ax.plot(X_lower, Y_lower, color="#05d2ed", label='Pressure Side')
            plt.gca().invert_yaxis() if Y_name == "Cp" else None
            
        else:
            ax.plot(X, Y, color="#6a408d")
    
        ax.set(xlabel=X_name, ylabel=Y_name, axisbelow=True)
        ax.set_title(f"{X_name} vs {Y_name}")
    
        if X_name != 'Panels':
            if Y_name == "L/D":
                opt_point(ax, data, X, Y, "L/D Max", "#9671bd", maxi=True)
                
            elif Y_name == "Cl":
                opt_point(ax, data, X, Y, "Cl Max", "#9671bd", maxi=True)
                
            elif Y_name == "Cd":
                opt_point(ax, data, X, Y, "Cd Min", "#9671bd", maxi=False)
            
        ax.minorticks_on()
        ax.grid(True, linestyle='-', linewidth=0.75, alpha=0.25)
        ax.grid(True, which='minor', linestyle='-', linewidth=0.25, alpha=0.15)
        
        plt.show()