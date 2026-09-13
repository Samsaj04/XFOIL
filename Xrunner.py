import subprocess
import numpy as np
import extra.plots as plots
#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------

def base_run(sim, airfoil=None, naca=None, Re=None, mach=None, 
              iter=None, panels=None, filename=None, dumpfile=None, verbose=True):
    
    if naca is None and airfoil is None:
        raise ValueError("You must add either NACA code or an Airfoil.dat file")
    
    visc = f"VISC {Re}" if Re is not None else f"VISC {1}\nVISC"
    mach = f"MACH {mach}" if mach is not None else f"MACH {0}"
    foil = f"LOAD {airfoil[0]}\n{airfoil[1]}" if airfoil is not None else f"NACA {naca}"
    dump = lambda dump: f"DUMP {dump}\n" if dump is not None else ""
    
    script = f"""{foil}
PANE
PPAR
N {panels}\n\n
PANE
OPER
ITER {iter}
{visc}
{mach}
PACC\n{filename}\n"
{sim}
{dump(dumpfile)}
QUIT
"""
    execute = subprocess.run(["xfoil.exe"], input=script, text=True, capture_output=True)
    
    if verbose:
        print(execute.stdout)
    print("\nLISTOOOOOOOOOO")
    
    return script, execute.stdout

# Run-an-Alpha-Analysis -------------------------------------------
def run_alpha(AOA, airfoil=None, naca=None, Re=None, mach=None, 
              iter=None, panels=None, filename=None, dumpfile=None, 
              airfoil_plot=False, verbose=True):
    
    base_run(f"ALFA {AOA}", airfoil, naca, Re, mach, iter, panels, filename, dumpfile, verbose)
    if bool(dumpfile):
        if airfoil_plot:
            dumps = save_dump(dumpfile)
            plots.plot_airfoil(dumps, dumps["x"], dumps["y"], "Airfoil")
        return save_polar(filename), dumps
    return save_polar(filename)

# Run-an-Alpha-Sequence-Analysis -------------------------------------------
def run_aseq(aseq, airfoil=None, naca=None, Re=None, mach=None, iter=None, 
             panels=None, filename=None, dumpfile=None, plot_data=[], verbose=True):
    
    aseq_sim = f"ASEQ {aseq[0]} {aseq[1]} {aseq[2]}"
    base_run(aseq_sim, airfoil, naca, Re, mach, iter, panels, filename, dumpfile, verbose)
    if bool(plot_data):
        polars = save_polar(filename)
        for var in plot_data:
            plots.plot_polar_pro(polars, polars[var[0]], polars[var[1]], f"{var[0]} vs {var[1]}")
    return save_polar(filename)

# Run-a-Mesh-Dependency-Study -------------------------------------------
def run_mesh_conv(AOA, pan_range, airfoil=None, naca=None, Re=None, mach=None, iter=None, 
                  filename=None, dumpfile=None, plot_data=[], verbose=True):
    sim = ""
    pan = np.array(range(pan_range[0], pan_range[1]+pan_range[2], pan_range[2]))
    for p in pan:
        sim += f"""
        PPAR
        N {p}\n\n
        OPER
        ALFA {AOA}
        """
    base_run(sim, airfoil, naca, Re, mach, iter, pan_range[0], filename, dumpfile, verbose)
    
    if bool(plot_data):
        polars = save_polar(filename)
        plots.plot_polar_pro(polars, pan, polars[plot_data], f"Mesh Convergence Study - Panels vs {plot_data}")
    return save_polar(filename)

def save_polar(filename):
    polars = np.loadtxt(filename, skiprows=12, ndmin=2)
    return {
        "alpha": polars[:,0],
        "CL": polars[:,1],
        "CD": polars[:,2],
        "L/D": polars[:,1] / polars[:,2],
        "CDp": polars[:,3],
        "CM": polars[:,4],
        "Top_Xtr": polars[:,5],
        "Bot_Xtr": polars[:,6]}

def save_dump(dumpfile):
    dumps = np.loadtxt(dumpfile, skiprows=1)
    return {
        "s": dumps[:,0],
        "x": dumps[:,1],
        "y": dumps[:,2],
        "Ue/Vinf": dumps[:,3],
        "Dstar": dumps[:,4],
        "Theta": dumps[:,5],
        "Cf": dumps[:,6],
        "H": dumps[:,7],
        "Cp": 1 - dumps[:,3]**2}


def main():
    airfoil = ['', 'name']
    naca = "2412"
    Re = 1e6
    mach = 0


if __name__ == "__main__":
    main()