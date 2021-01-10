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

    def __init__(self, pre_path, post_path, m_range, m_step, t_range, t_step):
        self.pre_img = np.loadtxt(pre_path)
        self.post_img = np.loadtxt(post_path)
        self.m_start = np.array(-m_range) / 2
        self.m_end = np.array(m_range) / 2
        self.m_step = np.array(m_step)
        self.t_start = np.array(-t_range) // 2
        self.t_end = np.array(t_range) // 2
        self.t_step = np.array(t_step)
        self.psf = cf.psf()
        self.m_opt = np.empty(self.pre_img.shape)
        self.t_opt = np.empty(self.pre_img.shape)
        self.c_opt = np.full(self.pre_img.shape, -2)
        self.MIN_WINDOW_LENGTH = 2

        for (y, x) in np.ndindex(self.m_opt.shape):
            self.m_opt[y, x] = [[1, 0], [0, 1]]
        for (y, x) in np.ndindex(self.m_opt.shape):
            self.t_opt[y, x] = [[0, 0]]

    def window_correlation(self, X1, X2, start, length):
        X1 = X1[start[0]:start[0] + length, start[1] + length]
        X2 = X2[start[0]:start[0] + length, start[1] + length]
        sum_of_multiple = np.sum(X1 * X2)
        sqrt_of_multiple = np.sqrt(np.sum(np.square(X1)) * np.sum(np.square(X2)))
        return sum_of_multiple / sqrt_of_multiple

    def get_range(self, start, end, step, offset):
        """
        :param start: m_start or t_start
        :param end: m_end or t_end
        :param step: m_step or t_step
        :param offset:
        :return: a list of param to test for
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
        if window_correlation < self.c_opt[y, x]:
            return
        self.m_opt[y, x] = Mw
        self.t_opt[y, x] = Tw
        self.c_opt[y, x] = window_correlation

    def run(self, scale):
        window_length = self.pre_img.shape[0] / pow(2, scale)
        if window_length < self.MIN_WINDOW_LENGTH:
            return

        # initialization
        # TODO:: offset should be optimal solution from previous scale for scale != 1
        if scale == 1:
            m_scale = self.get_range(self.m_start, self.m_end, self.m_step, np.array([[1, 0], [0, 1]]))
            t_scale = self.get_range(self.t_start, self.t_end, self.t_step, np.array([0, 0]))
        else:
            m_scale = self.get_range(self.m_start, self.m_end, self.m_step, [[1, 0], [0, 1]])
            t_scale = self.get_range(self.t_start, self.t_end, self.t_step, [[1, 0], [0, 1]])

        # do affine warping and coupled filtering
        # TODO:: study how to loop through all Mw and Tw
        for Mw in m_scale:
            processed_pre = cf.apply(self.pre_img, aw.affine_warping(self.psf, Mw, np.array([0, 0])))
            for Tw in t_scale:
                processed_post = cf.apply(aw.affine_warping(self.post_img, Mw, Tw), self.psf)
                # calculate window correlation
                for y in range(0, window_length, self.pre_img.shape[0]):
                    for x in range(0, window_length, self.pre_img.shape[1]):
                        window_correlation = self.window_correlation(processed_pre, processed_post, [y, x],
                                                                     window_length)
                        self.store_opt_params(y, x, window_correlation, Mw, Tw)

        self.run(scale+1)
