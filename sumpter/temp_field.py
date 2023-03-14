import numpy as np

class TempField:
    def __init__(self, param):
        self.dims = param["dims_temp"]
        self.tempA = param["tempA"]
        self.field = self.tempA*np.ones(self.dims)

    def update(self,colony):
        return