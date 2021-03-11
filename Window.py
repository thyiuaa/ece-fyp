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
