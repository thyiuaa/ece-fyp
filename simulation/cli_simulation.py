import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)

import Core as c
import os

pre_img_path = "./2-D_Simulation_Data/rf_2media_0percent_FieldII.dat"
post_img_path = "./2-D_Simulation_Data/rf_2media_5percent_FieldII.dat"
m_range = "0.15 0.05 0.05 0.15"
m_step = "0.05 0.05 0.05 0.05"
t_range = "4 2"
t_step = "1 1"
core = c.Core(pre_img_path, post_img_path, m_range, m_step, t_range, t_step)

algorithm = 1
is_parallel = True
threads = os.cpu_count()-5
core.start_algo(algorithm, is_parallel, threads)

core.dump_windows_data()
