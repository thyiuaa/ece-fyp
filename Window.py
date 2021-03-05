import numpy as np


class Window:
    def __init__(self, y, x, intp_m=np.array([[1, 0], [0, 1]]), intp_t=np.array([0, 0]), opt_m=np.array([[1, 0], [0, 1]]), opt_t=np.array([0, 0]), opt_c=-2):
        self.y = y
        self.x = x
        self.intp_m = intp_m
        self.intp_t = intp_t
        self.opt_m = opt_m
        self.opt_t = opt_t
        self.opt_c = opt_c

    def get_coordinates(self):
        return [self.y, self.x]

    def get_opt_m(self):
        return self.opt_m

    def get_opt_t(self):
        return self.opt_t

    def get_opt_c(self):
        return self.opt_c

    def get_intp_m(self):
        return self.intp_m

    def get_intp_t(self):
        return self.intp_t

    def set_coordinates(self, y, x):
        self.y = y
        self.x = x

    def set_opt_m(self, opt_m):
        self.opt_m = opt_m

    def set_opt_t(self, opt_t):
        self.opt_t = opt_t

    def set_opt_c(self, opt_c):
        self.opt_c = opt_c

    def set_intp_m(self, intp_m):
        self.intp_m = intp_m

    def set_intp_t(self, intp_t):
        self.intp_t = intp_t
