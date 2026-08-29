import subprocess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Xruner:
    def __init__(self, naca=None, airfoil=None, Re=None, pan=200, ite=400):
        self.naca = naca
        self.airfoil = airfoil
        self.Re = Re
        self.pan = pan
        self.ite = ite
        
        self._visc = f"VISC {self.Re}" if self.Re is not None else f"VISC {1}\nVISC"
        self._foil = f"LOAD {self.airfoil}\nPANE" if self.airfoil is not None else f"NACA {self.naca}"
        self._pacc = lambda file, dump: f"PACC\n{file}\n" if dump is None else f"PACC\n{file}\n{dump}"

    def _base_run(self, sim, filename, dumpfile=None):
        if self.naca is None and self.airfoil is None:
            raise ValueError("You must add either NACA code or an Airfoil.dat file")
        
        script = f"""{self._foil}
    PPAR
    N {self.pan}\n\n
    OPER
    ITER {self.ite}
    {self._visc}
    {self._pacc(filename, dumpfile)}
    {sim}\n
    QUIT
    """
        execute = subprocess.run(["xfoil.exe"], input=script, text=True, capture_output=True)
        print(execute.stdout)
        print("\nLISTOOOOOOOOOO")
        return script

    def run_alpha(self, AOA, filename, dumpfile=None, save_polar=False):
        alfa_sim = f"ALFA {AOA}"
        script = self._base_run(alfa_sim, filename, dumpfile)
        
        if not save_polar:
            pass
        else:
            self.save_polar_csv(filename)
        return script
    
    def run_aseq(self, aseq, filename, dumpfile=None, save_polar=False):
        aseq_sim = f"ASEQ {aseq[0]} {aseq[1]} {aseq[2]}"
        script = self._base_run(aseq_sim, filename, dumpfile)
        
        if not save_polar:
            pass
        else:
            self.save_polar_csv(filename)
        return script
    
    def run_mesh_conv(self, AOA, pan_range, filename, dumpfile=None, save_polar=False, plot=False):
        sim = ""
        pan = range(pan_range[0], pan_range[1], pan_range[2])
        for p in pan:
            sim += f"""
            PPAR
            N {p}\n\n
            OPER
            ALFA {AOA}
            """
        self.pan = pan_range[0]
        script = self._base_run(sim, filename, dumpfile)
        
        if not save_polar:
            pass
        else:
            polars_csv = self.save_polar_csv(filename)
            df = pd.read_csv(polars_csv)
            df.insert(0, "panels", 0)
            idx = 0
            for p in pan:
                df.loc[idx, "panels"] = p
                idx += 1
            df.to_csv(polars_csv, index=False)
            
            if plot:
                df = pd.read_csv(polars_csv)
                plt.plot(df["panels"], df["CL"])
                plt.grid(True)
                plt.show()
                plt.plot(df["panels"], df["CD"])
                plt.grid(True)
                plt.show()    
        return script

    def save_polar_csv(self, filename):
        polars = np.loadtxt(filename, skiprows=12)
        cols = ["alpha", "CL", "CD", "CDp", "CM", "Top_Xtr", "Bot_Xtr"]
        df = pd.DataFrame(polars, columns=cols)
        polars_csv = filename.replace(".txt", ".csv")
        df.to_csv(polars_csv, index=False)
        df = pd.read_csv(polars_csv)
        df["L/D"] = df["CL"]/df["CD"]
        df.to_csv(polars_csv, index=False)
        return polars_csv

#====================================================

airfoil = "airfoils\\NACA4415.txt"
naca_code = "2412"
Rey = 1e6
alpha = 3
ite = 400
filename = "juanito.txt"
dump = "puta.txt"

aseq = [-2, 15, 1]
panels = [30, 400, 50]

juanito = Xruner(naca=naca_code, Re=Rey)
#juanito.run_alpha(alpha, filename, save_polar=True)
#juanito.run_aseq(aseq=aseq, filename=filename, save_polar=True)
juanito.run_mesh_conv(AOA=alpha, pan_range=panels, filename=filename, save_polar=True, plot=True)


