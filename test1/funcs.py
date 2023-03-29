import numpy as np
import matplotlib.pyplot as plt
hq20 = 0.0037
gamma = np.log(2.4)/10

def f(temp):
    return hq20*np.exp(gamma*(temp-20))

rnge = np.linspace(8,25,1000)
f_t = np.zeros_like(rnge)
for i in range(len(rnge)):
    f_t[i] = f(rnge[i])

plt.plot(rnge,f_t)
plt.show()