import subprocess
import numpy as np

#====================================================
    
def run_xfoil(naca, Re, ite, pan, filename, alpha):
    input_file = open("polars.in", 'w')
    input_file.write(f"NACA {naca}\n")
    input_file.write("PPAR\n")
    input_file.write(f"N {pan}\n\n\n")
    input_file.write("OPER\n")
    input_file.write(f"VISC {Re}\n")
    input_file.write(f"ITER {ite}\n")
    input_file.write("PACC\n")
    input_file.write(f"{filename}\n\n")
    input_file.write(f"ALFA {alpha}\n")
    input_file.write("\n")
    input_file.write("QUIT\n")
    input_file.close()

    subprocess.call("xfoil.exe < polars.in", shell=True)


naca = "2412"
Re = 1e6
alpha = 5
ite = 400

for panels in range(30, 400, 30):
    run_xfoil(naca=naca, Re=Re, ite=ite, pan=panels, filename="pedro.txt", alpha=alpha)
    
hola = np.loadtxt("pedro.txt", skiprows=12)