import numpy as np
import os

import Algorithm as algo


class Core:
    def __init__(self, pre_path, post_path, m_range_str, m_step_str, t_range_str, t_step_str):
        self.algo = algo.Algorithm(pre_path, post_path, m_range_str, m_step_str, t_range_str, t_step_str)

    def start_algo(self, algorithm, is_parallel, threads):
        print(f"Starting Algorithm {algorithm}...")
        self.algo.run(algorithm, is_parallel, threads)

    def get_correlation(self):
        output = np.empty(self.algo.windows.shape)
        for y in range(0, output.shape[0]):
            for x in range(0, output.shape[1]):
                output[y, x] = self.algo.windows[y, x].opt_c
        return output

    def get_axial_strain(self):  # mxx-1
        output = np.empty(self.algo.windows.shape)
        for y in range(0, output.shape[0]):
            for x in range(0, output.shape[1]):
                output[y, x] = self.algo.windows[y, x].opt_m[0, 0] - 1
        return output

    def get_lateral_strain(self):  # myy-1
        output = np.empty(self.algo.windows.shape)
        for y in range(0, output.shape[0]):
            for x in range(0, output.shape[1]):
                output[y, x] = self.algo.windows[y, x].opt_m[1, 1] - 1
        return output

    def get_axial_shear(self):  # mxy
        output = np.empty(self.algo.windows.shape)
        for y in range(0, output.shape[0]):
            for x in range(0, output.shape[1]):
                output[y, x] = 1 + self.algo.windows[y, x].opt_m[0, 1]
        return output

    def get_lateral_shear(self):  # myx
        output = np.empty(self.algo.windows.shape)
        for y in range(0, output.shape[0]):
            for x in range(0, output.shape[1]):
                output[y, x] = 1 + self.algo.windows[y, x].opt_m[1, 0]
        return output

    def get_axial_translation(self):
        output = np.empty(self.algo.windows.shape)
        for y in range(0, output.shape[0]):
            for x in range(0, output.shape[1]):
                output[y, x] = 1 + self.algo.windows[y, x].opt_t[1]
        return output

    def get_lateral_translation(self):
        output = np.empty(self.algo.windows.shape)
        for y in range(0, output.shape[0]):
            for x in range(0, output.shape[1]):
                output[y, x] = 1 + self.algo.windows[y, x].opt_t[0]
        return output

    def dump_windows_data(self):
        if not os.path.exists("result"):
            os.mkdir("result")
        filename = "result/correlation_result.dat"
        np.savetxt(filename, self.get_correlation(), '%.4e', '\t', '\n')
        filename = "result/axial_strain_result.dat"
        np.savetxt(filename, self.get_axial_strain(), '%.4e', '\t', '\n')
        filename = "result/lateral_strain_result.dat"
        np.savetxt(filename, self.get_lateral_strain(), '%.4e', '\t', '\n')
        filename = "result/axial_shear_result.dat"
        np.savetxt(filename, self.get_axial_shear(), '%.4e', '\t', '\n')
        filename = "result/lateral_shear_result.dat"
        np.savetxt(filename, self.get_lateral_shear(), '%.4e', '\t', '\n')
        filename = "result/axial_translation_result.dat"
        np.savetxt(filename, self.get_axial_translation(), '%.4e', '\t', '\n')
        filename = "result/lateral_translation_result.dat"
        np.savetxt(filename, self.get_lateral_translation(), '%.4e', '\t', '\n')
