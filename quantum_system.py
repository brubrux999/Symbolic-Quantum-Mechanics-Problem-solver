import sympy as sp

class QuantumSystem():

    def __init__(self, x, potential):
        # Recibe el potencial y la variable a la que depende
        self._x = x
        self._potential = potential

        # Símbolos de la partícula
        self._m = sp.Symbol("m", positive=True)
        self._hbar = sp.Symbol(r"hbar", positive=True)
        self._E = sp.Symbol("E", positive=True)

        # Función incógnita
        self._psi = sp.Function("psi")

        # Ecuación de Schrödinger independiente del tiempo
        V = self._potential.expression
        T = -(self._hbar**2 / (2 * self._m)) * self._psi(self._x).diff(self._x, 2)
        H = T + V # Añadir para diferentes regiones de V
        self._equation = sp.Eq(self._E * self._psi(self._x), H)

    @property
    def equation(self):
        return self._equation

    def solve(self):
        # Resolvemos para la primera condición de frontera
        sol_1 = sp.dsolve(self._equation, self._psi(self._x), ics=dict([next(iter(self._potential.boundary_conditions(self._psi).items()))]))
        # Falta implementar solución para eigenvalores y eigenvectores
        sol_2 = ...
        return sol_1

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