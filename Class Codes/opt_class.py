import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import minimize

def plot_func3d(X, Y, func):
    
    x0 = np.array([-1.5, 2.0])
    minval = minimize(func, x0, method='nelder-mead')
    
    x_min = minval.x[0]
    y_min = minval.x[1]
    f_valmin = minval.fun

    print(f"x_min = {x_min}")
    print(f"y_min = {y_min}")
    print(f"f_valmin = {f_valmin}")

    x,y = np.meshgrid(X, Y)
    f = func([x, y])
    
    fig = plt.figure(0)
    ax = plt.axes(projection='3d')
    
    ax.plot_surface(x, y, f, cmap=plt.cm.coolwarm, edgecolor='none', alpha=0.75)
    ax.contour(x, y, f, levels=100, zdir='z', cmap=plt.cm.coolwarm)
    ax.scatter(x_min, y_min, f_valmin, c='black', marker='o', s=50, 
               label=f"X = {x_min:.5}\nY = {y_min:.5}\nZ = {f_valmin:.5}")
    
    ax.set(xlabel='X', ylabel='Y', zlabel='Z')
    ax.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    
    f = lambda x: (1-x[0])**2 + (1-x[1])**2 + 0.5 * (2*x[1] - x[0]**2)**2
    X = np.linspace(-5, 5, 20)
    Y = X
    plot_func3d(X, Y, f)
