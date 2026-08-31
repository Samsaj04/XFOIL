from Xrunner_no_pandas import Xruner

airfoil = "airfoils\\NACA4415.txt"
naca_code = "2412"
Rey = 1e6

alpha = 6
AOA_seq = [-2, 17, 0.1]

panels = [100, 500, 20]

plot_datas = [("alpha","CL"), ("alpha","CD"), ("alpha","L/D"), ("alpha","CM")]
plot_conv = ["CL", "CD", "CM", "L/D"]

juanito = Xruner(naca=naca_code, Re=Rey)

juanito.run_alpha(AOA = alpha,
                  filename = 'hola.txt',
                  dumpfile = "juanitodump.txt",
                  airfoil_plot = True)

#juanito.run_aseq(aseq = AOA_seq, 
#                 filename= "seq_alphas.txt", 
#                 plot_data = plot_datas)
#
#juanito.run_mesh_conv(AOA = alpha,
#                      pan_range = panels,
#                      filename = "mesh_conv.txt",
#                      plot_data = plot_conv)

