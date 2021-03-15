import os, sys, inspect
import concurrent.futures as td
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)

import Core as c


pre_img_path = "./2-D_Simulation_Data/rf_2media_0percent_FieldII.dat"
post_img_path = "./2-D_Simulation_Data/rf_2media_5percent_FieldII.dat"

ENV = "home"
if ENV == "lab":
    m_range = "0.2 0.1 0.1 0.2"
    m_step = "0.002 0.002 0.002 0.002"
    t_range = "30 6"
    t_step = "1 1"
else :
    m_range = "0.15 0.05 0.05 0.15"
    m_step = "0.05 0.05 0.05 0.05"
    t_range = "6 2"
    t_step = "1 1"

core = c.Core(pre_img_path, post_img_path, m_range, m_step, t_range, t_step)

algorithm = 1
is_parallel = True
total_cpu_ratio = 0.7
threads = int(os.cpu_count() * total_cpu_ratio)
success = core.start_algo(algorithm, is_parallel, threads)

if success:
    with td.ThreadPoolExecutor(max_workers=threads) as executor:
        for i in range(12):
            executor.submit(core.dump_windows_data, i)

