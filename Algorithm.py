import numpy as np

import AffineWarping as aw
import CoupledFiltering as cf
import Window as win


class Algorithm:
    """
    pre_img: pre-compression image (2^n x 2^n array)
    post_img: post-compression image (2^n x 2^n array)
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
        self.win_sep = [0, 0]  # TODO :: enter correct value
        self.windows = np.array(self.num_win)
        self.WIN_LENGTH = 37
        self.WIN_HEIGHT = 25
        self.MIN_WIN_VERTICAL_SEPARATION = 1
        self.MIN_WIN_HORIZONTAL_SEPARATION = 4
        # correlation coefficient
        self.c_mean_pre = []
        self.c_mean = []
        self.c_mean_affine = []
        # PSF
        self.psf = cf.psf()

    def window_correlation(self, X1, X2, start):
        X1 = X1[start[0]:start[0] + self.WIN_HEIGHT, start[1]:start[1] + self.WIN_LENGTH]
        X2 = X2[start[0]:start[0] + self.WIN_HEIGHT, start[1]:start[1] + self.WIN_LENGTH]
        sum_of_multiple = np.sum(X1 * X2)
        sqrt_of_multiple = np.sqrt(np.sum(np.square(X1)) * np.sum(np.square(X2)))
        return sum_of_multiple / sqrt_of_multiple

    def mean_correlation(self):
        total_correlation = 0
        for y in range(0, self.num_win[0]):
            for x in range(0, self.num_win[1]):
                total_correlation += self.windows[y, x].get_opt_c()
        return total_correlation / (self.num_win[0] * self.num_win[1])

    def get_range(self, type, offset):
        """
        :param type: 'M' or 'T'
        :param offset: offset to both start and end
        :return: a list of param will be used in searching for a window
        """
        if type == 'M':
            start = self.m_start
            end = self.m_end
            step = self.m_step
        else:
            start = self.t_start
            end = self.t_end
            step = self.t_step
        output = []
        lower_bound = start + offset
        upper_bound = end + offset
        for mxx in range(lower_bound[0, 0], upper_bound[0, 0] + step[0, 0], step[0, 0]):
            for mxy in range(lower_bound[0, 1], upper_bound[0, 1] + step[0, 1], step[0, 1]):
                for myx in range(lower_bound[1, 0], upper_bound[1, 0] + step[1, 0], step[1, 0]):
                    myy = -mxx  # equation 22
                    output.append(np.array([[mxx, mxy], [myx, myy]]))
        return output

    def store_opt_params(self, win_y, win_x, window_correlation, Mw, Tw):
        if window_correlation < self.windows[win_y, win_x].get_opt_c(): return
        self.windows[win_y, win_x].set_opt_m(Mw)
        self.windows[win_y, win_x].set_opt_t(Tw)
        self.windows[win_y, win_x].set_opt_c(window_correlation)

    def init_algo_param(self, scale, m_intp, t_intp):
        if scale == 0:
            m_scale = self.get_range('M', np.array([[1, 0], [0, 1]]))
            t_scale = self.get_range('T', np.array([0, 0]))
        else:
            m_scale = self.get_range('M', m_intp)
            t_scale = self.get_range('T', t_intp)
        return m_scale, t_scale

    def get_pre_correlation(self):
        c_pre = np.full(self.pre_img.shape, -2)
        for y in range(0, self.num_win[0]):
            for x in range(0, self.num_win[1]):
                c_pre[y, x] = self.window_correlation(self.pre_img, self.post_img, self.windows[y, x].get_coordinates())
        return c_pre

    def update_windows(self):
        old_num_win = self.num_win
        self.num_win = self.num_win * 2 - 1
        self.win_sep //= 2
        self.windows = np.reshape(self.windows, self.num_win)
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
            self.windows[y, x] = win.Window(y_pos, x_pos, intp_m, intp_t)

    def run(self, scale):  # Algorithm 1 in p.440 is used
        if self.win_sep[0] // 2 < self.MIN_WIN_VERTICAL_SEPARATION: return
        if self.win_sep[1] // 2 < self.MIN_WIN_HORIZONTAL_SEPARATION: return
        if scale > 0:
            self.update_windows()
            self.interpolate()

        # y, x are the coordinates of the top left element of that window in the image
        # c_affine = np.full(self.pre_img.shape, -2)
        for y in range(0, self.num_win[0]):
            for x in range(0, self.num_win[1]):
                # do affine warping and coupled filtering
                m_scale, t_scale = self.init_algo_param(scale, self.windows[y, x].get_opt_m(), self.windows[y, x].get_opt_t())
                for Mw in m_scale:
                    processed_pre = cf.apply(self.pre_img, aw.affine_warping(self.psf, Mw, np.array([0, 0])))
                    for Tw in t_scale:
                        affine_post = aw.affine_warping(self.post_img, Mw, Tw)
                        processed_post = cf.apply(affine_post, self.psf)
                        # temp_c_affine = self.window_correlation(self.pre_img, affine_post, [y, x], self.pre_img.shape[0])
                        # if c_affine[y, x] < temp_c_affine:
                        #     c_affine[y, x] = temp_c_affine
                        window_correlation = self.window_correlation(processed_pre, processed_post, self.windows[y, x].get_coordinates())
                        self.store_opt_params(y, x, window_correlation, Mw, Tw)

        # self.c_mean_pre.append(self.mean_correlation(scale, self.get_pre_correlation(window_length)))
        # self.c_mean_affine.append(self.mean_correlation(scale, c_affine))
        self.c_mean.append(self.mean_correlation())
        self.run(scale + 1)

    # ---------------- ALGORITHM 2
    def run_algo2(self, scale):  # Algorithm 2 in p.441 is used
        window_length = self.pre_img.shape[0] // pow(2, scale)
        if window_length < self.MIN_WINDOW_LENGTH: return
        # or you can say: if scale > MAX_SCALE: return

        # do affine warping and coupled filtering
        c_affine = np.zeros(self.pre_img.shape)

        m_scale = t_scale = np.empty(self.pre_img.shape)
        for y in range(0, self.pre_img.shape[0], window_length):
            for x in range(0, self.pre_img.shape[1], window_length):
                m_scale[y, x], t_scale[y, x] = self.init_algo_param(scale, self.m_opt[y, x], self.t_opt[y, x])

        for y in range(0, self.pre_img.shape[0], window_length):
            for x in range(0, self.pre_img.shape[1], window_length):
                for Mw in m_scale[y, x]:
                    processed_pre = cf.apply(self.pre_img, aw.affine_warping(self.psf, Mw, np.array([0, 0])))
                    for Tw in t_scale:
                        affine_post = aw.affine_warping(self.post_img, Mw, Tw)
                        processed_post = cf.apply(affine_post, self.psf)
                        # y, x are the coordinates of the top left element of that window in the image
                        for y in range(0, self.pre_img.shape[0], window_length):
                            for x in range(0, self.pre_img.shape[1], window_length):
                                temp_c_affine = self.window_correlation(self.pre_img, affine_post, [y, x], self.pre_img.shape[0])
                                if c_affine[y, x] < temp_c_affine:
                                    c_affine[y, x] = temp_c_affine
                                window_correlation = self.window_correlation(processed_pre, processed_post, [y, x], window_length)
                                self.store_opt_params(y, x, window_correlation, Mw, Tw)

        self.c_mean_pre.append(self.mean_correlation(scale, self.get_pre_correlation(window_length)))
        self.c_mean_affine.append(self.mean_correlation(scale, c_affine))
        self.c_mean.append(self.mean_correlation(scale, self.c_opt))
        self.run_algo2(scale + 1)
