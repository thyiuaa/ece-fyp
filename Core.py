import numpy as np
import os

import Algorithm as algo


class Core:
    def __init__(self, pre_path, post_path, m_range_str, m_step_str, t_range_str, t_step_str):
        self.algo = algo.Algorithm(pre_path, post_path, m_range_str, m_step_str, t_range_str, t_step_str)

    def start_algo(self, algorithm, is_parallel, threads):
        print(f"Starting Algorithm {algorithm}...")
        return self.algo.run(algorithm, is_parallel, threads)

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

    def get_intp_mxx(self):
        output = np.empty(self.algo.windows.shape)
        for y in range(0, output.shape[0]):
            for x in range(0, output.shape[1]):
                output[y, x] = self.algo.windows[y, x].intp_m[0, 0]
        return output

    def get_intp_mxy(self):
        output = np.empty(self.algo.windows.shape)
        for y in range(0, output.shape[0]):
            for x in range(0, output.shape[1]):
                output[y, x] = self.algo.windows[y, x].intp_m[0, 1]
        return output

    def get_intp_myx(self):
        output = np.empty(self.algo.windows.shape)
        for y in range(0, output.shape[0]):
            for x in range(0, output.shape[1]):
                output[y, x] = self.algo.windows[y, x].intp_m[1, 0]
        return output

    def get_intp_myy(self):
        output = np.empty(self.algo.windows.shape)
        for y in range(0, output.shape[0]):
            for x in range(0, output.shape[1]):
                output[y, x] = self.algo.windows[y, x].intp_m[1, 1]
        return output

    def get_intp_tx(self):
        output = np.empty(self.algo.windows.shape)
        for y in range(0, output.shape[0]):
            for x in range(0, output.shape[1]):
                output[y, x] = self.algo.windows[y, x].intp_t[0]
        return output

    def get_intp_ty(self):
        output = np.empty(self.algo.windows.shape)
        for y in range(0, output.shape[0]):
            for x in range(0, output.shape[1]):
                output[y, x] = self.algo.windows[y, x].intp_t[1]
        return output

    def dump_windows_data(self, i):
        if not os.path.exists("result"):
            os.mkdir("result")

        if i == 0:
            filename = "result/correlation_result.dat"
            np.savetxt(filename, self.get_correlation(), '%.4e', '\t', '\n')
        elif i == 1:
            filename = "result/axial_strain_result.dat"
            np.savetxt(filename, self.get_axial_strain(), '%.4e', '\t', '\n')
        elif i == 2:
            filename = "result/lateral_strain_result.dat"
            np.savetxt(filename, self.get_lateral_strain(), '%.4e', '\t', '\n')
        elif i == 3:
            filename = "result/axial_shear_result.dat"
            np.savetxt(filename, self.get_axial_shear(), '%.4e', '\t', '\n')
        elif i == 4:
            filename = "result/lateral_shear_result.dat"
            np.savetxt(filename, self.get_lateral_shear(), '%.4e', '\t', '\n')
        elif i == 5:
            filename = "result/axial_translation_result.dat"
            np.savetxt(filename, self.get_axial_translation(), '%.4e', '\t', '\n')
        elif i == 6:
            filename = "result/lateral_translation_result.dat"
            np.savetxt(filename, self.get_lateral_translation(), '%.4e', '\t', '\n')
        elif i == 7:
            filename = "result/intp_mxx_result.dat"
            np.savetxt(filename, self.get_intp_mxx(), '%.4e', '\t', '\n')
        elif i == 8:
            filename = "result/intp_mxy_result.dat"
            np.savetxt(filename, self.get_intp_mxy(), '%.4e', '\t', '\n')
        elif i == 9:
            filename = "result/intp_myx_result.dat"
            np.savetxt(filename, self.get_intp_myx(), '%.4e', '\t', '\n')
        elif i == 10:
            filename = "result/intp_myy_result.dat"
            np.savetxt(filename, self.get_intp_myy(), '%.4e', '\t', '\n')
        elif i == 11:
            filename = "result/intp_tx_result.dat"
            np.savetxt(filename, self.get_intp_tx(), '%.4e', '\t', '\n')
        elif i == 12:
            filename = "result/intp_ty_result.dat"
            np.savetxt(filename, self.get_intp_ty(), '%.4e', '\t', '\n')
