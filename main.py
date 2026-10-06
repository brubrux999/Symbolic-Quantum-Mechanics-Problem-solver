import sympy as sp

sp.init_printing()

x, p = sp.symbols("x p", real=True)
m, L = sp.symbols("m L", positive=True)

# Con esta clase padre determinamos la estructura de todos los potenciales
class Potential:

    def potential(self, x):
        pass

    def boundary_points(self):
        pass

class InfiniteWell(Potential):

    def __init__(self, L):
        self._L = L
        self._V = sp.Piecewise(
            (0, (x > -self._L) & (x < self._L)), # 0 entre -L y L
            (sp.oo, True)                        # infinito para el resto
        )

    @property
    def width(self):
        return self._L

    @property
    def potential(self):
        return self._V

    @property
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

    h_bar = sp.Symbol(r"hbar", positive=True)

    def __init__(self, mass, potential):
        self._mass = mass
        self._potential = potential

    def solve(self):
        V = self._potential.potential
        boundaries = self._potential.boundary_points
        sp.pretty_print(V)
        sp.pretty_print(boundaries)
        ...

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
Well = InfiniteWell(L)
system = QuantumSystem(m, Well)
system.solve()