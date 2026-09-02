import subprocess
import numpy as np
import plots

class Xruner:
    def __init__(self, naca=None, airfoil=None, Re=None, mach=None, pan=200, ite=400, verbose=True):
        self.naca = naca
        self.airfoil = airfoil
        self.Re = Re
        self.pan = pan
        self.ite = ite
        self.mach = mach
        self.verbose = verbose
        
        self._visc = f"VISC {self.Re}" if self.Re is not None else f"VISC {1}\nVISC"
        self._mach = f"MACH {self.mach}" if self.mach is not None else f"MACH {0}"
        self._foil = f"LOAD {self.airfoil}" if self.airfoil is not None else f"NACA {self.naca}"
        self._pacc = lambda file: f"PACC\n{file}\n"
        self._dump = lambda dump: f"DUMP {dump}\n" if dump is not None else ""

    def _base_run(self, sim, filename, dumpfile=None):
        if self.naca is None and self.airfoil is None:
            raise ValueError("You must add either NACA code or an Airfoil.dat file")
        
        script = f"""{self._foil}
    PANE
    PPAR
    N {self.pan}\n\n
    PANE
    OPER
    ITER {self.ite}
    {self._visc}
    {self._mach}
    {self._pacc(filename)}
    {sim}
    {self._dump(dumpfile)}
    QUIT
    """
        execute = subprocess.run(["xfoil.exe"], input=script, text=True, capture_output=True)
        if self.verbose:
            print(execute.stdout)
        print("\nLISTOOOOOOOOOO")
        return script, execute.stdout

    def run_alpha(self, AOA, filename, dumpfile=None, airfoil_plot=False):
        self._base_run(f"ALFA {AOA}", filename, dumpfile)
        data = [self.save_polar(filename)]
        if bool(dumpfile):
            dumps = self.save_dump(dumpfile)
            data.append(dumps)
            if airfoil_plot:
                plots.plot_airfoil(dumps, dumps["x"], dumps["y"], "Airfoil")
        return data
    
    def run_aseq(self, aseq, filename, plot_data=[]):
        aseq_sim = f"ASEQ {aseq[0]} {aseq[1]} {aseq[2]}"
        self._base_run(aseq_sim, filename, dumpfile=None)
        if bool(plot_data):
            polars = self.save_polar(filename)
            for var in plot_data:
                plots.plot_polar_pro(polars, polars[var[0]], polars[var[1]], f"{var[0]} vs {var[1]}")
        return self.save_polar(filename)
    
    def run_mesh_conv(self, AOA, pan_range, filename, plot_data=None):
        sim = ""
        pan = np.array(range(pan_range[0], pan_range[1]+pan_range[2], pan_range[2]))
        for p in pan:
            sim += f"""
            PPAR
            N {p}\n\n
            OPER
            ALFA {AOA}
            """
        self._base_run(sim, filename, None)
        
        if bool(plot_data):
            polars = self.save_polar(filename)
            polars["Panels"] = pan
            val = polars[plot_data]
            res = np.zeros(len(val))
            for i in range(1, len(val)):
                res[i] = np.abs((val[i]-val[i-1])/val[i-1]) * 100
            polars["Error"] = res
            plots.plot_polar_pro(polars, polars["Panels"], polars[plot_data], f"Mesh Convergence Study - Panels vs {plot_data}")
            plots.plot_polar_pro(polars, polars["Panels"], polars["Error"], f"Mesh Convergence Study - Panels vs Relative Error [%]")
        return self.save_polar(filename)
    
    #def _conv_panels(self, output):
    #    conv = []
    #    pan = None
#
    #    for l in output.splitlines():
    #        if "Number of panel nodes" in l:
    #            pan = int(l.split()[-1])
    #            
    #        if "Point added to stored polar" in l:
    #            conv.append(pan)
    #            
    #    return np.array(conv)

    def save_polar(self, filename):
        polars = np.loadtxt(filename, skiprows=12, ndmin=2)
        data = {
            "alpha": polars[:,0],
            "CL": polars[:,1],
            "CD": polars[:,2],
            "L/D": polars[:,1] / polars[:,2],
            "CDp": polars[:,3],
            "CM": polars[:,4],
            "Top_Xtr": polars[:,5],
            "Bot_Xtr": polars[:,6]}
        return data
    
    def save_dump(self, dumpfile):
        dumps = np.loadtxt(dumpfile, skiprows=1)
        data = {
            "s": dumps[:,0],
            "x": dumps[:,1],
            "y": dumps[:,2],
            "Ue/Vinf": dumps[:,3],
            "Dstar": dumps[:,4],
            "Theta": dumps[:,5],
            "Cf": dumps[:,6],
            "H": dumps[:,7],
            "Cp": 1 - dumps[:,3]**2}
        return data