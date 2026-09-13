from extra.Xrunner_OOP import Xruner
from parsec_gen import parsec
import numpy as np
from scipy.optimize import minimize

def optimize_nga(x0, func, Cl_des, ncx, AOA, Re, ite, pan):
    
    new_func = lambda h: func(h, Cl_des, ncx, AOA, Re, ite, pan)
    
    minval = minimize(new_func, x0, method='Nelder-Mead')
    x_min = minval.x
    
    for i, n in enumerate(x_min, start=1):
        print(f"x{i}_min = {n}")

    print(f"f_val_min = {minval.fun}")

def func_CL(x0, Cl_des, ncx, AOA, Re, ite, pan):
    
    coords, _, _, _ = parsec(x0, ncx)
    np.savetxt("holaputa_opti.txt", coords, fmt='%.6e')
    
    try:
        ecsfoil = Xruner(airfoil=[f"holaputa_opti.txt", f'foil_opt'], 
                     Re=Re, ite=ite, pan=pan, verbose=False)
        data = ecsfoil.run_alpha(AOA=AOA, filename=f"alpha{AOA}_opt.txt")
        return (data["Cl"][-1] - Cl_des)**2
    except:
        return 1e6

if __name__ == "__main__":
    
    x0=np.array([ # NACA-0012 representative
	# # Both---------------------------------	
	0.01550,
	# # UP---------------------------------	
	0.0000,
	0.29663,
	0.06002,
	0.00000,
	-0.45150,
	# # LOW---------------------------------	
	0.29663,
	-0.06002,
	0.0000,
	0.45150,
	0.0000,
	0.01550
	])

    Cl_des = 0.4
    Re = 1e6
    ite = 200
    pan = 160
    AOA = 1
    
    ncx = 60
    
    hola = optimize_nga(x0, func_CL, Cl_des, ncx, AOA, Re, ite, pan)