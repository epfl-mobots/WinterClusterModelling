class SimParam:
    def __init__(self,**kwargs):
        self.dims_draw = [800,800]
        self.dims_b = [50,50]
        self.dims_temp = [100,100] #twice as big as dims_b (twice finer grid)
        self.tau = 8