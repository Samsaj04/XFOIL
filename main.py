from Xrunner_no_pandas import Xruner

airfoil = "airfoils\\SSC-A09.txt"
naca_code = "4412"
Rey = 2.5e6

alpha = 3
AOA_seq = [-5, 18, 1]

panels = [100, 494, 20]

plot_datas = [("alpha","CL"), ("alpha","CD"), ("alpha","L/D"), ("alpha","CM"), ("CD","CL")]
plot_conv = "CL"

puta = Xruner(naca=naca_code, Re=2.5e6, pan=400, verbose=False)

#juanito.run_alpha(AOA = alpha,
#                  filename = 'hola.txt',
#                  dumpfile = "juanitodump.txt",
#                  airfoil_plot = True)

puta.run_aseq(aseq = AOA_seq, 
                 filename= "seq_alphas.txt", 
                 plot_data = plot_datas)

#juanito.run_mesh_conv(AOA = alpha,
#                      pan_range = panels,
#                      filename = "mesh_conv.txt",
#                      plot_data = plot_conv)