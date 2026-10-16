import sympy as sp
from sympy import pprint
import matplotlib.pyplot as plt
import numpy as np

class WaveFunction():

    # Constantes de clase
    _x, _p = sp.symbols("x p", real=True)
    _hbar = sp.Symbol(r"hbar", positive=True)

    def __init__(self, variable, expr, dominio=(-sp.oo, sp.oo)):
        # Variable simbólica de la que depende
        self._variable = variable

        # Límites donde existe la función
        self._dominio = dominio

        # Expresión simbólica normalizada a manejar
        self._expr = self.normalize(expr)

    @property
    def expression(self):
        return self._expr

    def normalize(self, expr):
        a, b = self._dominio
        psi = self._expr

        I = sp.integrate(expr**2, (self._variable, a, b))
        N = 1 / sp.sqrt(I)
        return sp.simplify(N * psi)

    def probability_density(self):
        density = sp.conjugate(self._expr) * self._expr
        return density.simplify()

    def Fourier_transform(self, inverse=False):
        C = 1 / sp.sqrt(2 * sp.pi * hbar)

        # Falta implementar mejora para asegurar que se recba la variable esperada
        if inverse:
            # La función de entrada depende de p
            kernel = sp.exp(sp.I * self._p * self._x / self._hbar)
            psi = C * sp.integrate(
                self._expr * kernel,
                (x, -sp.oo, sp.oo)
            )
            return WaveFunction(self._x, psi.simplify())
        else:
            # La función de entrada depende de x
            kernel = sp.exp(-sp.I * self._p * self._x / self._hbar)
            phi = C * sp.integrate(
                self._expr * kernel,
                (x, -sp.oo, sp.oo)
            )
            return WaveFunction(self._p, phi.simplify())

    def expected_value(self, variable):
        a, b = self._dominio
        value = sp.integrate(
            sp.conjugate(self._expr) * variable * self._expr, (self._variable, a, b)
        ) # Se espera que se introduzca una variable correspondiente al dominio de la función
        return value.simplify()
    
    def variance(self):
        value_1 = self.expected_value(self._variable)**2
        value_2 = self.expected_value(self._variable**2)
        var = value_2 - value_1
        return var.simplify()

    # Muestra una igualdad entre la expresión y su valor matemático
    def show(self, expresion, value, evaluate=False):
        pprint(sp.Eq(expresion, value, evaluate=evaluate))

    def plot(self):
        f = sp.lambdify(x, self._expr, "numpy")
        t = np.linspace(0, 2*np.pi, 100)
        plt.plot(t, f(t))
        plt.grid()
        plt.show()
        ...