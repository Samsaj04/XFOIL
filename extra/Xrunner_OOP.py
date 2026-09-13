from subprocess import run
import numpy as np
import extra.xfoil_plots as xfoil_plots

# ---------------------- XFOIL RUNNER ----------------------------
class Xruner:
    def __init__(self, naca=None, airfoil=None, Re=None, mach=None, pan=250, ite=400, verbose=True):
        
        self.naca = naca        # 4 Digits Naca Code
        self.airfoil = airfoil  # list, Path to 'txt' or 'dat' airfoil coordinates file and airfoil name
        
        self.Re = Re            # Reynolds Number
        self.mach = mach        # Mach Number
        
        self.pan = pan          # Number of panels
        self.ite = ite          # Number of Iterations
        
        self.verbose = verbose  # Output Xfoil analysis info
            
        self._visc = f"VISC {self.Re}" if self.Re is not None else f"VISC {1}\nVISC" # Add viscosity regime
        self._mach = f"MACH {self.mach}" if self.mach is not None else f"MACH {0}"   # Add mach regime
        
        # Load airfoil with coordinates file or generate NACA airfoil ------------------
        self._foil = f"LOAD {self.airfoil[0]}\n{self.airfoil[1]}" if self.airfoil is not None else f"NACA {self.naca}"
        
        # Generate Dump file ------------------
        self._dump = lambda dump: f"DUMP {dump}\n" if dump is not None else ""

    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------
    
    # Define base Xfoil Analysis - Takes 'sim' as any simulation ---------------
    def _base_run(self, sim, filename, dumpfile=None, timeout=None):
        
        if self.naca is None and self.airfoil is None:
            raise ValueError("You must add either NACA code or an Airfoil.dat file")
        
        # Generate Xfoil Commands ---------------
        script = f"""{self._foil}
        PANE
        PPAR
        N {self.pan}\n\n
        PANE
        OPER
        ITER {self.ite}
        {self._visc}
        {self._mach}
        PACC\n{filename}\n
        {sim}
        {self._dump(dumpfile)}
        QUIT
        """
        
        # Execute Xfoil script with a given timeout ---------------
        execute = run(["xfoil.exe"], input=script, text=True, capture_output=True, timeout=timeout)
        
        # Display Xfoil output ---------------
        if self.verbose:
            print(execute.stdout)

        print("LISTOOOOOOOOOO")
        return script, execute.stdout # Return Xfoil script and Xfoil output

    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------
    
    # Run Alpha Analysis ---------------
    def run_alpha(self, AOA, filename, dumpfile=None, airfoil_plot=False, timeout=None):
        
        self._base_run(f"ALFA {AOA}", filename, dumpfile, timeout)
        polars = self.save_polar(filename, bool(self.Re)) # Save Polar data
        
        if bool(dumpfile):
            dumps = self.save_dump(dumpfile) # Save Dumpfile data
            if airfoil_plot:
                xfoil_plots.plot_airfoil(dumps, dumps["x"], dumps["y"], "Airfoil")
                
            return polars, dumps
        return polars

    # Run Alpha Sequence Analysis ---------------
    def run_aseq(self, aseq, filename, plot_data=[], timeout=None):
        
        aseq_sim = f"ASEQ {aseq[0]} {aseq[1]} {aseq[2]}"
        self._base_run(aseq_sim, filename, timeout)
        polars = self.save_polar(filename, bool(self.Re)) # Save Polar data
        
        if bool(plot_data): # Plot Data
            for var in plot_data:
                xfoil_plots.plot_polar_pro(polars, polars[var[0]], polars[var[1]], f"{var[0]} vs {var[1]}")
                
        return polars

    # Run Mesh Dependency Study ---------------
    def run_mesh_conv(self, AOA, pan_range, filename, plot_data=None, timeout=None):
        
        sim = ""
        pan = np.array(range(pan_range[0], pan_range[1]+pan_range[2], pan_range[2])) # Generate panel array

        for p in pan:
            sim += f"""
            PPAR
            N {p}\n\n
            OPER
            ALFA {AOA}
            """
        self._base_run(sim, filename, timeout)
        
        if bool(plot_data):
            polars = self.save_polar(filename)
            polars["Panels"] = pan
            xfoil_plots.plot_polar_pro(polars, polars["Panels"], polars[plot_data],
                                 f"Mesh Convergence Study - Panels vs {plot_data}")
            
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

    def save_polar(self, filename, visc):
        polars = np.loadtxt(filename, skiprows=12, ndmin=2)
        data = {
            "alpha": polars[:,0],
            "Cl": polars[:,1],
            "Cd": polars[:,2],
            "Cdp": polars[:,3],
            "Cm": polars[:,4],
            "Top_Xtr": polars[:,5],
            "Bot_Xtr": polars[:,6]}
        if visc:
            data["L/D"] = polars[:,1] / polars[:,2]
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
    
