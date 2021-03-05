import numpy as np
import Algorithm as algo


def save_data_to_file(data, filename):
    output_file = open(filename, "w")
    for y in range(0, data.shape[1]):
        for x in range(0, data.shape[0]):
            output_file.write(str(data[y, x]))
            if x != data.shape[0] - 1:
                output_file.write("\t")
            else:
                output_file.write("\n")
    output_file.close()


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

    def get_axial_translation(self):
        output = np.empty(self.algo.windows.shape)
        for y in range(0, output.shape[1]):
            for x in range(0, output.shape[0]):
                output[y, x] = 1 + self.algo.windows[y, x].get_opt_t()[1]
        return output

    def get_lateral_translation(self):
        output = np.empty(self.algo.windows.shape)
        for y in range(0, output.shape[1]):
            for x in range(0, output.shape[0]):
                output[y, x] = 1 + self.algo.windows[y, x].get_opt_t()[0]
        return output

    def save_axial_strain(self):
        save_data_to_file(self.get_axial_strain(), "axial_strain.dat")

    def save_lateral_strain(self):
        save_data_to_file(self.get_lateral_strain(), "lateral_strain.dat")

    def save_axial_shear(self):
        save_data_to_file(self.get_axial_shear(), "axial_shear.dat")

    def save_lateral_shear(self):
        save_data_to_file(self.get_lateral_shear(), "lateral_shear.dat")

    def save_axial_translation(self):
        save_data_to_file(self.get_axial_translation(), "axial_translation.dat")

    def save_lateral_translation(self):
        save_data_to_file(self.get_lateral_translation(), "lateral_translation.dat")
