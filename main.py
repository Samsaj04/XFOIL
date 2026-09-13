from Xrunner_OOP import Xruner

airfoil = "holaputa_opti.txt"
Rey = 1e6

alpha = 1

plot_datas = [("alpha","CL"), ("alpha","CD"), ("alpha","L/D"), ("alpha","CM"), ("CD","CL")]
plot_conv = "CL"

puta = Xruner(naca='2412', Re=Rey, ite=200, pan=160, verbose=True)
puta.run_alpha(AOA=alpha, filename='hola.txt', dumpfile='juan.txt', airfoil_plot=True)