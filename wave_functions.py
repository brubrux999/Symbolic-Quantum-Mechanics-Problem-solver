import sympy as sp
from sympy import pprint

class WaveFunction():

    def __init__(self, variable, expr, quantum_number, E_n, dominio=(-sp.oo, sp.oo)):
        # Variable simbólica de la que depende
        self._variable = variable

        # Número cuántico y nivel de energía
        self._n = quantum_number
        self._E = E_n

        # Límites donde existe la función
        self._dominio = dominio

        # Expresión simbólica normalizada a manejar
        self._expr = expr
        self._expr = self.normalize()

    @property
    def expression(self):
        return self._expr

    @property
    def n(self):
        return self._n

    @property
    def E_n(self):
        return self._E

    @property
    def variable(self):
        return self._variable

    @property
    def probability_density(self):
        return sp.simplify(sp.conjugate(self._expr) * self._expr)

    # Se normaliza al inicializar la clase, de este modo siempre se trabaja con
    # funciones normalizadas
    def normalize(self):
        a, b = self._dominio

        I = sp.integrate(self.probability_density, (self._variable, a, b))
        if I == 0:
            raise ValueError("La integral de probabilidad es cero")

        N = 1 / sp.sqrt(I)
        return sp.simplify(N * self._expr)

    # Devuelve otro objeto de la misma clase con una variable y expresión distintas
    # inverse=False: x -> p
    # inverse=True: p -> x
    def Fourier_transform(self, new_variable, hbar, inverse=False):
        a, b = self._dominio
        C = 1 / sp.sqrt(2 * sp.pi * hbar)

        # Falta implementar mejora para asegurar que se recba la variable esperada
        if inverse:
            # La función de entrada depende de p
            kernel = sp.exp(sp.I * self._variable * self.new_variable / hbar)
            psi = C * sp.integrate(
                self._expr * kernel,
                (self._variable, a, b)
            )
            return WaveFunction(new_variable, psi.simplify())
        else:
            # La función de entrada depende de x
            kernel = sp.exp(-sp.I * new_variable * self._variable / hbar)
            phi = C * sp.integrate(
                self._expr * kernel,
                (self._variable, a, b)
            )
            return WaveFunction(new_variable, phi.simplify())

    # Calcula el valor esperado del argumento 'variable'
    def expected_value(self, variable):
        a, b = self._dominio

        # Se espera que se introduzca una variable correspondiente al dominio de la función
        # como x, x**2, etc. en el caso de que dependa de x
        return sp.simplify(
            sp.integrate(
                sp.conjugate(self._expr) * variable * self._expr, (self._variable, a, b)
            )
        )
    
    def variance(self):
        value_1 = self.expected_value(self._variable)**2
        value_2 = self.expected_value(self._variable**2)
        return sp.simplify(value_2 - value_1)

    # Muestra una igualdad entre la expresión y su valor matemático
    def show(self, expresion, value, evaluate=False):
        # Se usa pprint de momento para la visualización en la terminal
        pprint(sp.Eq(expresion, value, evaluate=evaluate))