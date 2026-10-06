import sympy as sp
from sympy import pprint

sp.init_printing()

# Símbolos globales
x, p = sp.symbols("x p", real=True)

# Con esta clase padre determinamos la estructura de todos los potenciales
class Potential:

    def expression(self):
        pass

    def equilibrium_points(self):
        pass

    def boundary_points(self):
        pass

class Constant(Potential):

    def __init__(self, V0):
        # Potencial V(x) = V0
        self._expr = sp.Integer(V0)

    @property
    def expression(self):
        return self._expr

    def equilibrium_points(self):
        return f"Equilibrio en todo el espacio ({-sp.oo}, {sp.oo})"

    def boundary_points(self):
        return (-sp.oo, sp.oo)

class HarmonicOscillator(Potential):
    
    def __init__(self, x):
        # Símbolo global insertado
        self._x = x
        # Símbolos particulares
        self._k = sp.Symbol("k", positive=True)

        # Potencial V(x) = 1/2 * k * x**2
        self._expr = sp.Rational(1,2) * self._k * self._x**2

    @property
    def expression(self):
        return self._expr

    def equilibrium_points(self):
        # dV/dx = 0
        return sp.solve(sp.diff(self._expr, self._x), self._x)

    def boundary_points(self):
        return (-sp.oo, sp.oo)

class InfiniteWell(Potential):

    def __init__(self, L):
        self._L = L
        self._V = sp.Piecewise(
            (0, (x > -self._L) & (x < self._L)), # 0 entre -L y L
            (sp.oo, True)                        # infinito para el resto
        )

    @property
    def L(self):
        return self._L

    @property
    def expression(self):
        return self._V

    def boundary_points(self):
        return (-self._L, self._L)

class PotentialBarrier(Potential):
    
    def __init__(self, V0, a):
        self._V0 = V0
        self._a = a
        self._V = sp.Piecewise(
            (0, x < 0),   # Región I (0 para x < 0)
            (V0, x <= a), # Región II (V0 entre 0 y a)
            (0, True)     # Región III (0 para x > a)
        )

    @property
    def width(self):
        return self._a
    
    @property
    def initial_potential(self):
        return self._V0

    @property
    def potential(self):
        return self._V

    @property
    def boundary_points(self):
        return (0, self._a)

class QuantumSystem():

    def __init__(self, x, potential):
        # Recibe el potencial y la variable a la que depende
        self._x = x
        self._potential = potential

        # Símbolos de la partícula
        self._m = sp.Symbol("m", positive=True)
        self._hbar = sp.Symbol(r"hbar", positive=True)
        self._E = sp.Symbol("E", real=True)

        # Función incógnita
        self._psi = sp.Symbol("psi")

        # Ecuación de Schrödinger independiente del tiempo
        V = self._potential.expression
        T = -(self._hbar**2 / (2 * self._m)) * sp.Derivative(self._psi, self._x, 2)
        H = T + V
        self._equation = sp.Eq(self._E * self._psi, H * self._psi, evaluate=False)

    def solve(self):
        return self._equation

    def wave_function(self):
        ...

    def energy_states(self):
        ...

    def probability_density(self):
        ...

    def expectation_value(self):
        ...

    def plot(self):
        ...

# Pequeña prueba para ver que todo se ejecute correctamente
zero_potential = Constant(0)
oscillator = HarmonicOscillator(x)
free_particle = QuantumSystem(x, zero_potential)
harmonic_oscillator = QuantumSystem(x, oscillator)

pprint("PARTICULA LIBRE")
pprint(zero_potential.equilibrium_points())
pprint("La ecuación a resolver es:")
pprint(free_particle.solve())

pprint("OSCILADOR ARMÓNICO")
pprint(oscillator.equilibrium_points())
pprint("La ecuación a resolver es:")
pprint(harmonic_oscillator.solve())