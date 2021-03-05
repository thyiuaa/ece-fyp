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
        self.m_range = np.reshape(np.fromstring(m_range_str, dtype=float, sep=' '), [2, 2])
        self.t_range = np.fromstring(t_range_str, dtype=float, sep=' ')
        self.m_start = np.array(-self.m_range) / 2
        self.m_end = np.array(self.m_range) / 2
        self.m_step = np.reshape(np.fromstring(m_step_str, dtype=float, sep=' '), [2, 2])
        self.t_start = np.array(-self.t_range) // 2
        self.t_end = np.array(self.t_range) // 2
        self.t_step = np.fromstring(t_step_str, dtype=float, sep=' ')
        # window specification
        self.num_win = [3, 4]
        self.win_sep = [64, 256]  # https://puu.sh/HkCG0/25fc8419b2.png
        self.windows = np.empty(self.num_win)
        self.WIN_WIDTH = 37
        self.WIN_HEIGHT = 25
        self.MIN_WIN_VERTICAL_SEPARATION = 1
        self.MIN_WIN_HORIZONTAL_SEPARATION = 4
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
                        myy = 2-mxx  # myy = 2-(exx+1) = 1-exx = 1+eyy (equation 22)
                        output.append(np.array([[mxx, mxy], [myx, myy]]))
        else:
            for tx in range(lower_bound[0], upper_bound[0] + self.t_step[0], self.t_step[0]):
                for ty in range(lower_bound[1], upper_bound[1] + self.t_step[1], self.t_step[1]):
                    output.append(np.array([tx, ty]))
        return output

    def store_opt_params(self, win_y, win_x, window_correlation, Mw, Tw):
        if window_correlation < self.windows[win_y, win_x].get_opt_c(): return
        self.windows[win_y, win_x].set_opt_m(Mw)
        self.windows[win_y, win_x].set_opt_t(Tw)
        self.windows[win_y, win_x].set_opt_c(window_correlation)

    def init_windows(self):
        start_pos = [-5, -11]
        for y in range(0, self.num_win[1]):
            for x in range(0, self.num_win[0]):
                self.windows[y, x] = win.Window(start_pos[0] * y, start_pos[1] * x)

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

    def reduce_range(self):
        self.m_start /= 2
        self.m_end /= 2
        self.t_start //= 2
        self.t_end //= 2

    def slice_image(self, pre_img, post_img, window):
        window_pos = [max(0, i) for i in window.get_coordinates()]  # map negative coordinate to 0
        sliced_pre = pre_img[window_pos[0]: window_pos[0] + self.WIN_HEIGHT, window_pos[1]: window_pos[1] + self.WIN_WIDTH]
        sliced_post = post_img[window_pos[0]: window_pos[0] + self.WIN_HEIGHT, window_pos[1]: window_pos[1] + self.WIN_WIDTH]
        return [sliced_pre, sliced_post]

    def correlation(self, image1, image2):
        sum_of_multiple = np.sum(image1 * image2)
        sqrt_of_multiple = np.sqrt(np.sum(np.square(image1)) * np.sum(np.square(image2)))
        return sum_of_multiple / sqrt_of_multiple

    def reset(self):
        self.num_win = [3, 4]
        self.win_sep = [64, 256]
        self.windows = np.empty(self.num_win)
        self.m_start = np.array(-self.m_range) / 2
        self.m_end = np.array(self.m_range) / 2
        self.t_start = np.array(-self.t_range) // 2
        self.t_end = np.array(self.t_range) // 2
        self.c_mean = []

    def run(self, algorithm):  # Algorithm 1 in p.440 is used
        scale = 0
        # for algo 2 use
        Mw = self.search_space('M', self.m_start, self.m_end, self.m_step, np.array([[1, 0], [0, 1]]))
        Tw = self.search_space('T', self.t_start, self.t_end, self.t_step, np.array([0, 0]))

        while self.win_sep[0] // 2 >= self.MIN_WIN_VERTICAL_SEPARATION and self.win_sep[1] // 2 >= self.MIN_WIN_HORIZONTAL_SEPARATION:
            if scale == 0:
                self.init_windows()
                range_start = 0  # process every windows
                range_step = 1
            else:
                self.update_windows()
                self.interpolate()
                range_start = 1  # process only new windows
                range_step = 2

            if algorithm == 1:
                for y in range(range_start, self.num_win[0], range_step):
                    for x in range(range_start, self.num_win[1], range_step):
                        Mw = self.search_space('M', self.m_start, self.m_end, self.m_step, self.windows[y, x].get_intp_m())
                        Tw = self.search_space('T', self.t_start, self.t_end, self.t_step, self.windows[y, x].get_intp_t())
                        sliced_pre, sliced_post = self.slice_image(self.pre_img, self.post_img, self.windows[y, x])
                        for M in Mw:
                            processed_pre = cf.apply(sliced_pre, aw.affine_warping(self.psf, M, np.array([0, 0])))
                            for T in Tw:
                                processed_post = cf.apply(aw.affine_warping(sliced_post, M, T), self.psf)
                                window_correlation = self.correlation(processed_pre, processed_post)
                                self.store_opt_params(y, x, window_correlation, M, T)
            elif algorithm == 2:
                for M in Mw:
                    processed_pre = cf.apply(self.pre_img, aw.affine_warping(self.psf, M, np.array([0, 0])))
                    for T in Tw:
                        processed_post = cf.apply(aw.affine_warping(self.post_img, M, T), self.psf)
                        for y in range(range_start, self.num_win[0], range_step):
                            for x in range(range_start, self.num_win[1], range_step):
                                sliced_pre, sliced_post = self.slice_image(processed_pre, processed_post, self.windows[y, x])
                                window_correlation = self.correlation(sliced_pre, sliced_post)
                                self.store_opt_params(y, x, window_correlation, M, T)

            self.reduce_range()
            scale += 1

        return
