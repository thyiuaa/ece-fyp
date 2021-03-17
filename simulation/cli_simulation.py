import inspect
import os
import sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)

from joblib import Parallel, delayed
import Core as c

pre_img_path = "./2-D_Simulation_Data/rf_2media_0percent_FieldII.dat"
post_img_path = "./2-D_Simulation_Data/rf_2media_5percent_FieldII.dat"

ENV = "sim3"
if ENV == "sim1":
    m_range = "0.2 0.1 0.1 0.2"
    m_step = "0.002 0.002 0.002 0.002"
    t_range = "30 6"
    t_step = "1 1"
elif ENV == "sim2":
    m_range = "0.15 0.1 0.1 0.15"
    m_step = "0.015 0.001 0.01 0.015"
    t_range = "22 4"
    t_step = "1 1"
elif ENV == "sim3":
    m_range = "0.18 0.1 0.1 0.18"
    m_step = "0.006 0.005 0.05 0.006"
    t_range = "18 60"
    t_step = "1 1"
else:
    m_range = "0.1 0.1 0.1 0.1"
    m_step = "0.05 0.05 0.05 0.05"
    t_range = "6 2"
    t_step = "1 1"

core = c.Core(pre_img_path, post_img_path, m_range, m_step, t_range, t_step)

algorithm = 1
is_parallel = True
total_cpu_ratio = 0.7
threads = int(os.cpu_count() * total_cpu_ratio)
max_scale = 6

if __name__ == "__main__":
    success = core.start_algo(algorithm, is_parallel, threads, max_scale)

    if success:
        print("Simulation complete!")
        print("====================================\n")
        print(f"Saving result to files...")
        print(f"Total tasks: 13 files")
        Parallel(n_jobs=threads, backend="loky", verbose=100, max_nbytes=None, mmap_mode='w+')(
            delayed(core.dump_windows_data)(i) for i in range(13)
        )
    else:
        print("Simulation failed!")
