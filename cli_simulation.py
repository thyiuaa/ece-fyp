import Core as c
core = c.Core("./2-D_Simulation_Data/rf_2media_0percent_FieldII.dat", "./2-D_Simulation_Data/rf_2media_5percent_FieldII.dat", "0.2 0.1 0.1 0.2", "0.002 0.002 0.002 0.002", "30 6", "1 1")
core.start_algo()