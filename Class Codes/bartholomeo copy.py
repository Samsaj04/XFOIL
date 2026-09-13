import subprocess
import numpy as np

def run_xfoil(naca, ite, Re, pan_seq, filename, aoa):
    script = f"""
    NACA {naca}
    PPAR
    N {pan_seq[0]}\n\n
    OPER
    ITER {ite}
    visc {Re}
    PACC
    {filename}\n
    ALFA {aoa}"""
    
    for i in range(pan_seq[0]+pan_seq[2], pan_seq[1], pan_seq[2]):
        script += f"""\n
        PPAR
        N {i}\n\n     
        OPER
        ALFA {aoa}"""
        
    script += """\n
    QUIT"""
 
    execute = subprocess.run(["xfoil"], input=script, text=True, capture_output=True)
    print(execute.stdout)

#====================================================

naca = "2412"
Re = 1e6
alpha = 5
ite = 400

panels = [30, 400, 30]

simu = run_xfoil(naca=naca, Re=Re, pan_seq=panels, ite=ite, filename=f"panels.txt", aoa=alpha)


