import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

class WaveFunction():

    def __init__(self, x, expr):
        # Variable simbólica de la que depende
        self._x = x
        # Expresión simbólica a manejar
        self._expr = expr
        ...

    def Fourier_transform(self, variable):
        ...

    def probability_density(self):
        ...

    def expectation_value(self, variable):
        ...
    
    def variance(self):
        ...

    def plot(self):
        f = sp.lambdify(x, self._expr, "numpy")
        t = np.linspace(0, 2*np.pi, 100)
        plt.plot(t, f(t))
        plt.grid()
        plt.show()
        ...