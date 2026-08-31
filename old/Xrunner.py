import subprocess
import numpy as np
import pandas as pd
import plots

class Xruner:
    def __init__(self, naca=None, airfoil=None, Re=None, pan=200, ite=400):
        self.naca = naca
        self.airfoil = airfoil
        self.Re = Re
        self.pan = pan
        self.ite = ite
        
        self._visc = f"VISC {self.Re}" if self.Re is not None else f"VISC {1}\nVISC"
        self._foil = f"LOAD {self.airfoil}\nPANE" if self.airfoil is not None else f"NACA {self.naca}"
        self._pacc = lambda file: f"PACC\n{file}\n"
        self._dump = lambda dump: f"DUMP {dump}\n" if dump is not None else ""

    def _base_run(self, sim, filename, dumpfile=None):
        if self.naca is None and self.airfoil is None:
            raise ValueError("You must add either NACA code or an Airfoil.dat file")
        
        script = f"""{self._foil}
    PPAR
    N {self.pan}\n\n
    OPER
    ITER {self.ite}
    {self._visc}
    {self._pacc(filename)}
    {sim}
    {self._dump(dumpfile)}
    QUIT
    """
        execute = subprocess.run(["xfoil.exe"], input=script, text=True, capture_output=True)
        print(execute.stdout)
        print("\nLISTOOOOOOOOOO")
        return script

    def run_alpha(self, AOA, filename, dumpfile=None, save_polar=False, save_dump=False):
        script = self._base_run(f"ALFA {AOA}", filename, dumpfile)
        if save_polar:
            self.save_polar_csv(filename)
        if save_dump:
            self.save_dump_csv(dumpfile)
        return script
    
    def run_aseq(self, aseq, filename, save_polar=False, plot_data=[]):
        aseq_sim = f"ASEQ {aseq[0]} {aseq[1]} {aseq[2]}"
        script = self._base_run(aseq_sim, filename, dumpfile=None)
        if save_polar:
            polars_csv = self.save_polar_csv(filename)
            if bool(plot_data):
                df = pd.read_csv(polars_csv)
                for var in plot_data:
                    plots.plot_polar_pro(df[var[0]], df[var[1]], f"{var[0]} vs {var[1]}")
        return script
    
    def run_mesh_conv(self, AOA, pan_range, filename, dumpfile=None, save_polar=False, plot_data=[]):
        sim = ""
        pan = range(pan_range[0], pan_range[1], pan_range[2])
        for p in pan:
            sim += f"""
            PPAR
            N {p}\n\n
            OPER
            ALFA {AOA}
            """
        script = self._base_run(sim, filename, dumpfile)
        
        if save_polar:
            polars_csv = self.save_polar_csv(filename)
            df = pd.read_csv(polars_csv)
            df.insert(0, "Panels", 0)
            idx = 0
            for p in pan:
                df.loc[idx, "Panels"] = p
                idx += 1
            df.to_csv(polars_csv, index=False)
            
            if bool(plot_data):
                df = pd.read_csv(polars_csv)
                for var in plot_data:
                    plots.plot_polar_pro(df["Panels"], df[var], f"Mesh Convergence Study - Panels vs {var}")
        return script

    def save_polar_csv(self, filename):
        polars = np.loadtxt(filename, skiprows=12, ndmin=2)
        cols = ["alpha", "CL", "CD", "CDp", "CM", "Top_Xtr", "Bot_Xtr"]
        df = pd.DataFrame(polars, columns=cols)
        df["L/D"] = df["CL"]/df["CD"]
        polars_csv = filename.replace(".txt", ".csv")
        df.to_csv(polars_csv, index=False)
        return polars_csv
    
    def save_dump_csv(self, dumpfile):
        dumps = np.loadtxt(dumpfile, skiprows=1)
        cols = ["s", "x", "y", "Ue/Vinf", "Dstar", "Theta", "Cf", "H"]
        df = pd.DataFrame(dumps, columns=cols)
        df["Cp"] = 1 - df["Ue/Vinf"]**2
        dump_csv = dumpfile.replace(".txt", '.csv')
        df.to_csv(dump_csv, index=False)
        return dump_csv

#====================================================

airfoil = "airfoils\\NACA4415.txt"
naca_code = "2412"
Rey = 1e6

alpha = 3
aseq = [-2, 15, 0.5]

Panels = [100, 500, 10]

plot_datas = [("alpha","CL"), ("alpha","CD"), ("alpha","L/D"), ("alpha","CM")]
plot_conv = ["CL", "CD", "CM", "L/D"]

juanito = Xruner(naca=naca_code, Re=Rey, pan=150)


juanito.run_alpha(alpha,filename='hola.txt', dumpfile="juanitodump.txt", save_dump=True)
#juanito.run_aseq(aseq=aseq, filename="seq_alphas.txt", save_polar=True, plot_data=[])
#juanito.run_mesh_conv(AOA=alpha, pan_range=Panels, filename="mesh_conv.txt", save_polar=True, plot_data=plot_conv)


