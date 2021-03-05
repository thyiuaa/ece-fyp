import numpy as np
import Algorithm as algo


class Core:
    def __init__(self, pre_path, post_path, m_range_str, m_step_str, t_range_str, t_step_str):
        self.algo = algo.Algorithm(pre_path, post_path, m_range_str, m_step_str, t_range_str, t_step_str)

    def start_algo(self):
        self.algo.run(0)

    def get_axial_strain(self):  # mxx-1
        output = np.empty(self.algo.windows.shape)
        for y in range(0, output.shape[1]):
            for x in range(0, output.shape[0]):
                output[y, x] = self.algo.windows[y, x].get_opt_m()[0, 0] - 1
        return output

    def get_lateral_strain(self):  # myy-1
        output = np.empty(self.algo.windows.shape)
        for y in range(0, output.shape[1]):
            for x in range(0, output.shape[0]):
                output[y, x] = self.algo.windows[y, x].get_opt_m()[1, 1] - 1
        return output

    def get_axial_shear(self):  # mxy
        output = np.empty(self.algo.windows.shape)
        for y in range(0, output.shape[1]):
            for x in range(0, output.shape[0]):
                output[y, x] = 1 + self.algo.windows[y, x].get_opt_m()[0, 1]
        return output

    def get_lateral_shear(self):  # myx
        output = np.empty(self.algo.windows.shape)
        for y in range(0, output.shape[1]):
            for x in range(0, output.shape[0]):
                output[y, x] = 1 + self.algo.windows[y, x].get_opt_m()[1, 0]
        return output

    def get_x_translate(self):
        output = np.empty(self.algo.windows.shape)
        for y in range(0, output.shape[1]):
            for x in range(0, output.shape[0]):
                output[y, x] = 1 + self.algo.windows[y, x].get_opt_t()[1]
        return output

    def get_y_translate(self):
        output = np.empty(self.algo.windows.shape)
        for y in range(0, output.shape[1]):
            for x in range(0, output.shape[0]):
                output[y, x] = 1 + self.algo.windows[y, x].get_opt_t()[0]
        return output
