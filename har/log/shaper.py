import numpy as np


class LogShaper:
    def __init__(self, data):
        self.data = data

    def sliding_window(self, window_size, step_size):
        n = self.data.shape[0]
        return np.hstack(self.data[i:(1 + n + i - window_size):step_size] for i in range(0, window_size))

    def split(self, indices):
        return np.hsplit(self.data, indices)
