import numpy as np
import tqdm
from joblib import Parallel, delayed

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
        self.m_start = (np.array(self.m_range) / 2) * -1
        self.m_end = np.array(self.m_range) / 2
        self.m_step = np.reshape(np.fromstring(m_step_str, dtype=float, sep=' '), [2, 2])
        self.t_start = (np.array(self.t_range) // 2) * -1
        self.t_end = np.array(self.t_range) // 2
        self.t_step = np.fromstring(t_step_str, dtype=float, sep=' ')
        # window specification
        self.num_win = np.array([4, 3])
        self.win_sep = np.array([256, 64])  # https://puu.sh/HkCG0/25fc8419b2.png
        self.windows = np.empty(self.num_win, dtype=win.Window)
        self.WIN_WIDTH = 25
        self.WIN_HEIGHT = 37
        self.MIN_WIN_VERTICAL_SEPARATION = 4
        self.MIN_WIN_HORIZONTAL_SEPARATION = 1
        # PSF
        self.psf = cf.psf()

    def search_space(self, param_type, start, end, step, offset):
        # print("Getting search space for %s..." % param_type)
        output = []
        temp = start + offset
        lower_bound = temp - ((temp / step) % 1) * step  # round down to nearest multiple of step
        temp = end + offset
        upper_bound = temp + (1 - (temp / step) % 1) * step  # round up to nearest multiple of step
        counter = 0
        if param_type == 'M':
            mxx = lower_bound[0, 0]
            while mxx < upper_bound[0, 0]:
                mxy = lower_bound[0, 1]
                while mxy < upper_bound[0, 1]:
                    myx = lower_bound[1, 0]
                    while myx < upper_bound[1, 0]:
                        myy = -mxx + 2  # myy = 2-(exx+1) = 1-exx = 1+eyy (equation 22)
                        output.append(np.array([[mxx, mxy], [myx, myy]]))
                        counter += 1
                        myx += self.m_step[1, 0]
                    mxy += self.m_step[0, 1]
                mxx += self.m_step[0, 0]
        else:
            tx = lower_bound[0]
            while tx < upper_bound[0]:
                ty = lower_bound[1]
                while ty < upper_bound[1]:
                    output.append(np.array([tx, ty]))
                    ty += self.t_step[1]
                tx += self.t_step[0]
        return output

    def init_windows(self):
        start_pos = [116 - self.WIN_HEIGHT // 2, 36 - self.WIN_WIDTH // 2]
        for y in range(0, self.num_win[0]):
            for x in range(0, self.num_win[1]):
                self.windows[y, x] = win.Window(start_pos[0] + (self.win_sep[0] * y), start_pos[1] + (self.win_sep[1] * x))

    def update_windows(self):
        # enlarge windows
        old_num_win = self.num_win
        self.num_win = self.num_win * 2 - 1
        self.win_sep //= 2
        new_windows = np.empty(self.num_win, dtype=win.Window)
        new_windows[0: old_num_win[0], 0: old_num_win[1]] = self.windows
        # reposition inside windows
        for y in range(old_num_win[0] - 1, -1, -1):
            for x in range(old_num_win[1] - 1, -1, -1):
                new_windows[y * 2, x * 2] = self.windows[y, x]
        self.windows = new_windows

    def interpolate(self):
        for (y, x) in np.ndindex(self.windows.shape):
            y_t = y % 2
            x_t = x % 2
            if y_t == 0 and x_t == 1:
                y_pos = self.windows[y, x - 1].y
                x_pos = self.windows[y, x - 1].x + self.win_sep[1]
                intp_m = (self.windows[y, x - 1].opt_m + self.windows[y, x + 1].opt_m) / 2
                intp_t = (self.windows[y, x - 1].opt_t + self.windows[y, x + 1].opt_t) / 2
            elif y_t == 1 and x_t == 0:
                y_pos = self.windows[y - 1, x].y + self.win_sep[0]
                x_pos = self.windows[y - 1, x].x
                intp_m = (self.windows[y - 1, x].opt_m + self.windows[y + 1, x].opt_m) / 2
                intp_t = (self.windows[y - 1, x].opt_t + self.windows[y + 1, x].opt_t) / 2
            elif y_t == 1 and x_t == 1:
                y_pos = self.windows[y - 1, x - 1].y + self.win_sep[0]
                x_pos = self.windows[y - 1, x - 1].x + self.win_sep[1]
                intp_m = (self.windows[y - 1, x - 1].opt_m + self.windows[y - 1, x + 1].opt_m + self.windows[y + 1, x - 1].opt_m + self.windows[y + 1, x + 1].opt_m) / 4
                intp_t = (self.windows[y - 1, x - 1].opt_t + self.windows[y - 1, x + 1].opt_t + self.windows[y + 1, x - 1].opt_t + self.windows[y + 1, x + 1].opt_t) / 4
            else:
                continue
            self.windows[y, x] = win.Window(y_pos, x_pos, intp_m, intp_t)  # will only create interpolate result

    def slice_image(self, pre_img, post_img, window):
        # print("Slicing images...")
        window_pos = [max(0, i) for i in [window.y, window.x]]  # map negative coordinate to 0
        sliced_pre = pre_img[window_pos[0]: window_pos[0] + self.WIN_HEIGHT, window_pos[1]: window_pos[1] + self.WIN_WIDTH]
        sliced_post = post_img[window_pos[0]: window_pos[0] + self.WIN_HEIGHT, window_pos[1]: window_pos[1] + self.WIN_WIDTH]
        return [sliced_pre, sliced_post]

    def windows_id(self, scale):
        output = []
        if scale == 0:
            for y in range(0, self.num_win[0]):
                for x in range(0, self.num_win[1]):
                    output.append([y, x])
        else:
            for y in range(0, self.num_win[0]):
                for x in range(0, self.num_win[1]):
                    if y % 2 != 0 or x % 2 != 0:
                        output.append([y, x])
        return output

    def total_parameter(self, y, x):
        temp = self.m_start + self.windows[y, x].opt_m
        lower_bound = temp - ((temp / self.m_step) % 1) * self.m_step  # round down to nearest multiple of step
        temp = self.m_end + self.windows[y, x].opt_m
        upper_bound = temp + (1 - (temp / self.m_step) % 1) * self.m_step  # round up to nearest multiple of step
        temp = (upper_bound - lower_bound) / self.m_step
        temp[1, 1] = 1
        total_m = np.round(np.prod(temp))

        temp = self.t_start + self.windows[y, x].opt_t
        lower_bound = temp - ((temp / self.t_step) % 1) * self.t_step  # round down to nearest multiple of step
        temp = self.t_end + self.windows[y, x].opt_t
        upper_bound = temp + (1 - (temp / self.t_step) % 1) * self.t_step  # round up to nearest multiple of step
        total_t = np.prod((upper_bound - lower_bound) / self.t_step)
        return total_m * total_t

    def correlation(self, image1, image2):
        shape = np.minimum(image1.shape, image2.shape)
        sum_of_multiple = np.sum(image1[0:shape[0], 0:shape[1]] * image2[0:shape[0], 0:shape[1]])
        sqrt_of_multiple = np.sqrt(np.sum(np.sum(np.square(image1)[0:shape[0], 0:shape[1]])) * np.sum(np.sum(np.square(image2)[0:shape[0], 0:shape[1]])))
        return sum_of_multiple / sqrt_of_multiple

    def store_opt_params(self, win_y, win_x, window_correlation, M, T):
        if window_correlation > self.windows[win_y, win_x].opt_c:
            self.windows[win_y, win_x].opt_m = M
            self.windows[win_y, win_x].opt_t = T
            self.windows[win_y, win_x].opt_c = window_correlation

    def reduce_range(self):
        self.m_start /= 2
        self.m_end /= 2
        self.t_start //= 2
        self.t_end //= 2

    def reset(self):
        self.num_win = [4, 3]
        self.win_sep = [256, 64]
        self.windows = np.empty(self.num_win)
        self.m_start = np.array(-self.m_range) / 2
        self.m_end = np.array(self.m_range) / 2
        self.t_start = np.array(-self.t_range) // 2
        self.t_end = np.array(self.t_range) // 2

    def algo1_non_parallel(self, scale, progress_bar):
        for y in range(0, self.num_win[0]):
            for x in range(0, self.num_win[1]):
                if scale != 0 and y % 2 == 0 and x % 2 == 0: continue
                Mw = self.search_space('M', self.m_start, self.m_end, self.m_step, self.windows[y, x].intp_m)
                Tw = self.search_space('T', self.t_start, self.t_end, self.t_step, self.windows[y, x].intp_t)
                sliced_pre, sliced_post = self.slice_image(self.pre_img, self.post_img, self.windows[y, x])
                for M in Mw:
                    processed_pre = cf.apply(sliced_pre, aw.affine_warping(self.psf, M, np.array([0, 0])))
                    for T in Tw:
                        processed_post = cf.apply(aw.affine_warping(sliced_post, M, T), self.psf)
                        window_correlation = self.correlation(processed_pre, processed_post)
                        self.store_opt_params(y, x, window_correlation, M, T)
                        progress_bar.update(1)

    def algo1_parallel_core(self, scale, y, x):
        if scale != 0 and y % 2 == 0 and x % 2 == 0: return
        opt_m = np.array([[-100, -100], [-100, -100]])
        opt_t = np.array([-100, -100])
        opt_c = -2
        Mw = self.search_space('M', self.m_start, self.m_end, self.m_step, self.windows[y, x].intp_m)
        Tw = self.search_space('T', self.t_start, self.t_end, self.t_step, self.windows[y, x].intp_t)
        sliced_pre, sliced_post = self.slice_image(self.pre_img, self.post_img, self.windows[y, x])
        for M in Mw:
            processed_pre = cf.apply(sliced_pre, aw.affine_warping(self.psf, M, np.array([0, 0])))
            for T in Tw:
                processed_post = cf.apply(aw.affine_warping(sliced_post, M, T), self.psf)
                window_correlation = self.correlation(processed_pre, processed_post)
                if window_correlation > self.windows[y, x].opt_c:
                    opt_m = M
                    opt_t = T
                    opt_c = window_correlation
        return [y, x, opt_c, opt_m, opt_t]

    def algo1_parallel(self, scale, valid_windows, threads):
        print(f"Scale {scale}")
        print(f"Total tasks: {len(valid_windows)} windows.")
        results = Parallel(n_jobs=threads, backend="loky", verbose=100, max_nbytes=None, mmap_mode='w+')(
            delayed(self.algo1_parallel_core)(scale, y, x) for [y, x] in valid_windows
        )
        for data in results:
            self.store_opt_params(data[0], data[1], data[2], data[3], data[4])
        print("\n")

    def algo2_non_parallel(self, scale, Mw, Tw, progress_bar):
        for M in Mw:
            processed_pre = cf.apply(self.pre_img, aw.affine_warping(self.psf, M, np.array([0, 0])))
            for T in Tw:
                processed_post = cf.apply(aw.affine_warping(self.post_img, M, T), self.psf)
                for y in range(0, self.num_win[0]):
                    for x in range(0, self.num_win[1]):
                        if scale != 0 and y % 2 == 0 and x % 2 == 0: continue
                        sliced_pre, sliced_post = self.slice_image(processed_pre, processed_post, self.windows[y, x])
                        window_correlation = self.correlation(sliced_pre, sliced_post)
                        self.store_opt_params(y, x, window_correlation, M, T)
                        progress_bar.update(1)

    def algo2_parallel_core(self, scale, Mw, Tw, y, x):
        opt_m = np.array([[-100, -100], [-100, -100]])
        opt_t = np.array([-100, -100])
        opt_c = -2
        for M in Mw:
            processed_pre = cf.apply(self.pre_img, aw.affine_warping(self.psf, M, np.array([0, 0])))
            for T in Tw:
                processed_post = cf.apply(aw.affine_warping(self.post_img, M, T), self.psf)
                if scale != 0 and y % 2 == 0 and x % 2 == 0: return
                sliced_pre, sliced_post = self.slice_image(processed_pre, processed_post, self.windows[y, x])
                window_correlation = self.correlation(sliced_pre, sliced_post)
                if window_correlation > self.windows[y, x].opt_c:
                    opt_m = M
                    opt_t = T
                    opt_c = window_correlation
        return [y, x, opt_c, opt_m, opt_t]

    def algo2_parallel(self, scale, valid_windows, threads, Mw, Tw):
        print(f"Scale {scale}")
        print(f"Total tasks: {len(valid_windows)} windows ({len(Mw)} * {len(Tw)} parameters each).")
        results = Parallel(n_jobs=threads, backend="loky", verbose=100, max_nbytes=None, mmap_mode='w+')(
            delayed(self.algo2_parallel)(scale, Mw, Tw, y, x) for [y, x] in valid_windows
        )
        for data in results:
            self.store_opt_params(data[0], data[1], data[2], data[3], data[4])
        print("\n")

    def run(self, algorithm, is_parallel, threads):
        scale = 0
        # sets of parameters for algo 2 to use
        Mw = self.search_space('M', self.m_start, self.m_end, self.m_step, np.array([[1, 0], [0, 1]]))
        Tw = self.search_space('T', self.t_start, self.t_end, self.t_step, np.array([0, 0]))

        while self.win_sep[0] > self.MIN_WIN_VERTICAL_SEPARATION and self.win_sep[1] > self.MIN_WIN_HORIZONTAL_SEPARATION:
            if scale > 1: break
            if scale == 0:
                self.init_windows()
            else:
                self.update_windows()
                self.interpolate()
            valid_windows = self.windows_id(scale)

            # setting up progress bar for non parallel processing
            if not is_parallel:
                total_param = 0
                for [y, x] in valid_windows:
                    total_param += self.total_parameter(y, x)
                print(f"Estimated progress:")
                progress_bar = tqdm.tqdm(total=int(total_param), desc=f"Scale {scale}")

            # run algorithm
            if algorithm == 1:
                if is_parallel:
                    self.algo1_parallel(scale, valid_windows, threads)
                else:
                    self.algo1_non_parallel(scale, progress_bar)
            elif algorithm == 2:
                if is_parallel:
                    self.algo2_parallel(scale, valid_windows, threads, Mw, Tw)
                else:
                    self.algo2_non_parallel(scale, Mw, Tw, progress_bar)
            else:
                print("Invalid algorithm ID")
                return False

            # proceed to next scale
            self.reduce_range()
            scale += 1

        return True
