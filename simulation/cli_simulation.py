import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)

import Core as c
import os

pre_img_path = "./2-D_Simulation_Data/rf_2media_0percent_FieldII.dat"
post_img_path = "./2-D_Simulation_Data/rf_2media_5percent_FieldII.dat"
m_range = "0.15 0.05 0.05 0.15"
m_step = "0.006 0.006 0.006 0.006"
t_range = "10 3"
t_step = "1 1"
core = c.Core(pre_img_path, post_img_path, m_range, m_step, t_range, t_step)
core.start_algo()

if (not os.path.exists("result")):
    os.mkdir("result")
filename = "result/correlation_result.dat"
core.save_correlation(filename)
filename = "result/axial_strain_result.dat"
core.save_axial_strain(filename)
filename = "result/lateral_strain_result.dat"
core.save_lateral_strain(filename)
filename = "result/axial_shear_result.dat"
core.save_axial_shear(filename)
filename = "result/lateral_shear_result.dat"
core.save_lateral_shear(filename)
filename = "result/axial_translation_result.dat"
core.save_axial_translation(filename)
filename = "result/lateral_translation_result.dat"
core.save_lateral_translation(filename)