from Xrunner_OOP_V2 import Xruner
from extra.xfoil_plots import plot_polar_dump, plot_airfoil

airfoil = "holaputa_opti.txt"
Rey = 1e6

alpha = 1

#plot_polars = [("alpha","Cl"), ("alpha","Cd"), ("alpha","L/D"), ("alpha","Cm"), ("Cd","Cl")]
#plot_dump = [('x', 'Cp'), ('x', 'Ue/Vinf')]

puta = Xruner(naca='2412', Re=Rey, ite=200, pan=160, verbose=False)

#polars = puta.run_aseq(aseq=[-3, 12, 1], filename='hola.txt')
#plot_polar_dump(var=plot_polars, data=polars)
pol, dump = puta.run_alpha(AOA=alpha, filename='hola.txt', dumpfile='juanito.txt')
plot_polar_dump(var='dump', data=dump)