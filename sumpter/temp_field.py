import numpy as np

class TempField:
    def __init__(self, dims, temp_amb):
        self.field = temp_amb*np.ones(dims)
        self.dims = dims
        self.tempA = temp_amb

    def update(self,colony):
        return