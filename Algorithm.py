import numpy as np

import AffineWarping as aw
import CoupledFiltering as cf


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
        m_range = np.reshape(np.fromstring(m_range_str, dtype=float, sep=' '), [2, 2])
        t_range = np.fromstring(t_range_str, dtype=float, sep=' ')
        self.pre_img = np.loadtxt(pre_path)
        self.post_img = np.loadtxt(post_path)
        self.m_start = np.array(-m_range) / 2
        self.m_end = np.array(m_range) / 2
        self.m_step = np.reshape(np.fromstring(m_step_str, dtype=float, sep=' '), [2, 2])
        self.t_start = np.array(-t_range) // 2
        self.t_end = np.array(t_range) // 2
        self.t_step = np.fromstring(t_step_str, dtype=float, sep=' ')
        self.psf = cf.psf()
        self.m_opt = np.empty(self.pre_img.shape)
        self.t_opt = np.empty(self.pre_img.shape)
        self.c_opt = np.full(self.pre_img.shape, -2)
        # self.c_total = np.empty(self.pre_img.shape)
        self.MIN_WINDOW_LENGTH = 2
        self.c_mean_pre = []
        self.c_mean = []
        self.c_mean_affine = []

        for (y, x) in np.ndindex(self.m_opt.shape):
            self.m_opt[y, x] = [[1, 0], [0, 1]]
        for (y, x) in np.ndindex(self.m_opt.shape):
            self.t_opt[y, x] = [[0, 0]]

    def window_correlation(self, X1, X2, start, length):
        X1 = X1[start[0]:start[0] + length, start[1]:start[1] + length]
        X2 = X2[start[0]:start[0] + length, start[1]:start[1] + length]
        sum_of_multiple = np.sum(X1 * X2)
        sqrt_of_multiple = np.sqrt(np.sum(np.square(X1)) * np.sum(np.square(X2)))
        return sum_of_multiple / sqrt_of_multiple

    def mean_correlation(self, scale, c):
        window_length = self.pre_img.shape[0] // pow(2, scale)
        total_correlation = 0
        number_windows = pow(4, scale)
        for y in range(0, self.pre_img.shape[0], window_length):
            for x in range(0, self.pre_img.shape[1], window_length):
                total_correlation += c[y, x]
        return total_correlation / number_windows

    def get_range(self, start, end, step, offset):
        """
        :param start: m_start or t_start
        :param end: m_end or t_end
        :param step: m_step or t_step
        :param offset:
        :return: a list of param will be used in searching for a window
        """
        output = []
        arr = start + offset
        lower_bound = start + offset
        upper_bound = end + offset
        lower_req = np.greater_equal(arr, lower_bound)
        upper_req = np.less_equal(arr, upper_bound)
        while lower_req.all() and upper_req.all():
            output.append(arr)
            arr += step
            lower_req = np.greater_equal(arr, lower_bound)
            upper_req = np.less_equal(arr, upper_bound)
        return output

    def store_opt_params(self, y, x, window_correlation, Mw, Tw):
        if window_correlation < self.c_opt[y, x]: return
        self.m_opt[y, x] = Mw
        self.t_opt[y, x] = Tw
        self.c_opt[y, x] = window_correlation

    def init_algo_param(self, scale, y, x):
        if scale == 1:
            m_scale = self.get_range(self.m_start, self.m_end, self.m_step, np.array([[1, 0], [0, 1]]))
            t_scale = self.get_range(self.t_start, self.t_end, self.t_step, np.array([0, 0]))
        else:
            m_scale = self.get_range(self.m_start, self.m_end, self.m_step, self.m_opt[y, x])
            t_scale = self.get_range(self.t_start, self.t_end, self.t_step, self.t_opt[y, x])
        return m_scale, t_scale

    def get_pre_correlation(self, window_length):
        c_pre = np.full(self.pre_img.shape, -2)
        for y in range(0, self.pre_img.shape[0], window_length):
            for x in range(0, self.pre_img.shape[1], window_length):
                c_pre[y, x] = self.window_correlation(self.pre_img, self.post_img, [y, x], self.pre_img.shape[0])
        return c_pre

    def run(self, scale):  # Algorithm 1 in p.440 is used
        window_length = self.pre_img.shape[0] // pow(2, scale)
        if window_length < self.MIN_WINDOW_LENGTH: return
        # or you can say: if scale > MAX_SCALE: return

        # y, x are the coordinates of the top left element of that window in the image
        c_affine = np.full(self.pre_img.shape, -2)
        for y in range(0, self.pre_img.shape[0], window_length):
            for x in range(0, self.pre_img.shape[1], window_length):
                # do affine warping and coupled filtering
                m_scale, t_scale = self.init_algo_param(scale, y, x)
                for Mw in m_scale:
                    processed_pre = cf.apply(self.pre_img, aw.affine_warping(self.psf, Mw, np.array([0, 0])))
                    for Tw in t_scale:
                        affine_post = aw.affine_warping(self.post_img, Mw, Tw)
                        processed_post = cf.apply(affine_post, self.psf)
                        temp_c_affine = self.window_correlation(self.pre_img, affine_post, [y, x], self.pre_img.shape[0])
                        if c_affine[y, x] < temp_c_affine:
                            c_affine[y, x] = temp_c_affine
                        window_correlation = self.window_correlation(processed_pre, processed_post, [y, x], window_length)
                        self.store_opt_params(y, x, window_correlation, Mw, Tw)

        self.c_mean_pre.append(self.mean_correlation(scale, self.get_pre_correlation(window_length)))
        self.c_mean_affine.append(self.mean_correlation(scale, c_affine))
        self.c_mean.append(self.mean_correlation(scale, self.c_opt))
        self.run(scale + 1)

    # ---------------- ALGORITHM 2

    def run_algo2(self, scale):  # Algorithm 2 in p.440 is used
        window_length = self.pre_img.shape[0] // pow(2, scale)
        if window_length < self.MIN_WINDOW_LENGTH: return
        # or you can say: if scale > MAX_SCALE: return

        # do affine warping and coupled filtering
        c_affine = np.empty(self.pre_img.shape)
        m_scale, t_scale = self.init_algo_param(scale, y, x)
        for Mw in m_scale:
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
        self.run(scale + 1)
