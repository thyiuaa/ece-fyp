import numpy as np

import AffineWarping as aw
import CoupledFiltering as cf
import Window as win


class Algorithm:
    """
    pre_img: pre-compression image
    post_img: post-compression image
    m_start: lower bound of M
    m_end: upper bound of M
    m_step: step of M
    t_start: lower bound of T
    t_end: upper bound of T
    t_step: step of T
    psf: Point spread function, filter used in coupled filtering
    m_opt: the optimal value of M
    t_opt: the optimal value of T
    c_opt: the optimal value of correlation coefficient
    MIN_WINDOW_LENGTH: minimum window length that the algorithm will continue to process
    """

    def __init__(self, pre_path, post_path, m_range_str, m_step_str, t_range_str, t_step_str):
        # images
        self.pre_img = np.loadtxt(pre_path)
        self.post_img = np.loadtxt(post_path)
        # motion parameters
        m_range = np.reshape(np.fromstring(m_range_str, dtype=float, sep=' '), [2, 2])
        t_range = np.fromstring(t_range_str, dtype=float, sep=' ')
        self.m_start = np.array(-m_range) / 2
        self.m_end = np.array(m_range) / 2
        self.m_step = np.reshape(np.fromstring(m_step_str, dtype=float, sep=' '), [2, 2])
        self.t_start = np.array(-t_range) // 2
        self.t_end = np.array(t_range) // 2
        self.t_step = np.fromstring(t_step_str, dtype=float, sep=' ')
        # interpolation result
        self.M_intp = []
        self.T_intp = []
        self.C_intp = 0
        # window specification
        self.num_win = [3, 4]
        self.win_sep = [64, 256]  # https://puu.sh/HkCG0/25fc8419b2.png
        self.windows = np.array(self.num_win)
        self.WIN_LENGTH = 37
        self.WIN_HEIGHT = 25
        self.MIN_WIN_VERTICAL_SEPARATION = 1
        self.MIN_WIN_HORIZONTAL_SEPARATION = 4
        # correlation coefficient
        self.c_mean = []
        # PSF
        self.psf = cf.psf()

    def search_space(self, param_type, start, end, step, offset):
        output = []
        temp = start + offset
        lower_bound = temp - ((temp / step) % 1) * step  # round down to nearest multiple of step
        temp = end + offset
        upper_bound = temp + (1 - (temp / step) % 1) * step  # round up to nearest multiple of step
        if param_type == 'M':
            for mxx in range(lower_bound[0, 0], upper_bound[0, 0] + self.m_step[0, 0], self.m_step[0, 0]):
                for mxy in range(lower_bound[0, 1], upper_bound[0, 1] + self.m_step[0, 1], self.m_step[0, 1]):
                    for myx in range(lower_bound[1, 0], upper_bound[1, 0] + self.m_step[1, 0], self.m_step[1, 0]):
                        myy = -mxx  # equation 22
                        output.append(np.array([[mxx, mxy], [myx, myy]]))
        else:
            for tx in range(lower_bound[0], upper_bound[0] + self.t_step[0], self.t_step[0]):
                for ty in range(lower_bound[1], upper_bound[1] + self.t_step[1], self.t_step[1]):
                    output.append(np.array([tx, ty]))
        return output

    def init_window_search_space(self, m_intp, t_intp):
        m_scale = self.search_space('M', self.m_start, self.m_end, self.m_step, m_intp)
        t_scale = self.search_space('T', self.t_start, self.t_end, self.t_step, t_intp)
        return m_scale, t_scale

    def store_opt_params(self, win_y, win_x, window_correlation, Mw, Tw):
        if window_correlation < self.windows[win_y, win_x].get_opt_c(): return
        self.windows[win_y, win_x].set_opt_m(Mw)
        self.windows[win_y, win_x].set_opt_t(Tw)
        self.windows[win_y, win_x].set_opt_c(window_correlation)

    def update_windows(self):
        # enlarge windows
        old_num_win = self.num_win
        self.num_win = self.num_win * 2 - 1
        self.win_sep //= 2
        new_windows = np.empty(self.num_win)
        new_windows[0: old_num_win[0] - 1, 0: old_num_win[1] - 1] = self.windows
        self.windows = new_windows
        # reposition inside windows
        for y in range(old_num_win[0], 0, -1):
            for x in range(old_num_win[1], 0, -1):
                self.windows[y * 2, x * 2] = self.windows[y, x]

    def interpolate(self):
        for (y, x) in np.ndindex(self.windows.shape):
            y_t = y % 2
            x_t = x % 2
            if y_t == 0 and x_t == 1:
                y_pos = self.windows[y, x - 1].get_coordinates()[0]
                x_pos = self.windows[y, x - 1].get_coordinates()[1] + self.win_sep[1]
                intp_m = (self.windows[y, x - 1].get_opt_m() + self.windows[y, x + 1].get_opt_m()) / 2
                intp_t = (self.windows[y, x - 1].get_opt_t() + self.windows[y, x + 1].get_opt_t()) / 2
            elif y_t == 1 and x_t == 0:
                y_pos = self.windows[y - 1, x].get_coordinates()[0] + self.win_sep[0]
                x_pos = self.windows[y - 1, x].get_coordinates()[1]
                intp_m = (self.windows[y - 1, x].get_opt_m() + self.windows[y + 1, x].get_opt_m()) / 2
                intp_t = (self.windows[y - 1, x].get_opt_t() + self.windows[y + 1, x].get_opt_t()) / 2
            elif y_t == 1 and x_t == 1:
                y_pos = self.windows[y - 1, x - 1].get_coordinates()[0] + self.win_sep[0]
                x_pos = self.windows[y - 1, x - 1].get_coordinates()[1] + self.win_sep[1]
                intp_m = (self.windows[y - 1, x - 1].get_opt_m() + self.windows[y - 1, x + 1].get_opt_m() + self.windows[y + 1, x - 1].get_opt_m() + self.windows[y + 1, x + 1].get_opt_m()) / 4
                intp_t = (self.windows[y - 1, x - 1].get_opt_t() + self.windows[y - 1, x + 1].get_opt_t() + self.windows[y + 1, x - 1].get_opt_t() + self.windows[y + 1, x + 1].get_opt_t()) / 4
            else:
                continue
            self.windows[y, x] = win.Window(y_pos, x_pos, intp_m, intp_t)  # will only create interpolate result

    def window_correlation(self, image1, image2, start):
        image1 = image1[start[0]:start[0] + self.WIN_HEIGHT, start[1]:start[1] + self.WIN_LENGTH]
        image2 = image2[start[0]:start[0] + self.WIN_HEIGHT, start[1]:start[1] + self.WIN_LENGTH]
        sum_of_multiple = np.sum(image1 * image2)
        sqrt_of_multiple = np.sqrt(np.sum(np.square(image1)) * np.sum(np.square(image2)))
        return sum_of_multiple / sqrt_of_multiple

    def mean_correlation(self):
        total_correlation = 0
        for y in range(0, self.num_win[0]):
            for x in range(0, self.num_win[1]):
                total_correlation += self.windows[y, x].get_opt_c()
        return total_correlation / (self.num_win[0] * self.num_win[1])

    def get_pre_correlation(self):
        c_pre = np.full(self.pre_img.shape, -2)
        for y in range(0, self.num_win[0]):
            for x in range(0, self.num_win[1]):
                c_pre[y, x] = self.window_correlation(self.pre_img, self.post_img, self.windows[y, x].get_coordinates())
        return c_pre

    def run(self, scale):  # Algorithm 1 in p.440 is used
        if self.win_sep[0] // 2 < self.MIN_WIN_VERTICAL_SEPARATION: return
        if self.win_sep[1] // 2 < self.MIN_WIN_HORIZONTAL_SEPARATION: return

        if scale == 0:
            self.init_windows()  # TODO:: implement init_windows()
        else:
            self.update_windows()
            self.interpolate()

        for y in range(0, self.num_win[0]):
            for x in range(0, self.num_win[1]):
                m_scale, t_scale = self.init_window_search_space(self.windows[y, x].get_intp_m(), self.windows[y, x].get_intp_t())
                for Mw in m_scale:
                    processed_pre = cf.apply(self.pre_img, aw.affine_warping(self.psf, Mw, np.array([0, 0])))
                    for Tw in t_scale:
                        affine_post = aw.affine_warping(self.post_img, Mw, Tw)
                        processed_post = cf.apply(affine_post, self.psf)
                        window_correlation = self.window_correlation(processed_pre, processed_post, self.windows[y, x].get_coordinates())
                        self.store_opt_params(y, x, window_correlation, Mw, Tw)

        self.c_mean.append(self.mean_correlation())
        self.run(scale + 1)
