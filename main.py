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

    def __init__(self, x, L=None):
        self._x = x

        if L == None:
            self._L = sp.Symbol("L", positive=True)
        else:
            self._L = sp.Integer(L)

        # Solo nos interesa la solución dentro del pozo, donde V(x) = 0
        self._expr = sp.Integer(0)

    @property
    def width(self):
        return self._L

    @property
    def expression(self):
        return self._expr

    def equilibrium_points(self):
        return (
            f"Equilibrio indiferente en todo el intervalo ({-self._L}, {self._L}), "
            f"Equilibrio estable límite en los puntos {self.boundary_points()}"
        )

    def boundary_points(self):
        return (-self._L, self._L)

    def boundary_conditions(self, wave_function):
        return {
            wave_function.subs(self._x, 0): 0,      # psi(0) = 0
            wave_function.subs(self._x, self._L): 0 # psi(L) = 0
        }

class PotentialBarrier(Potential):
    
    def __init__(self, x, V0, a):
        self._x = x
        self._V0 = sp.Integer(V0)
        self._a = a

    @property
    def width(self):
        return self._a
    
    @property
    def V0(self):
        return self._V0

    @property
    def expression(self):
        # Buscamos resolver una EDO para cada región
        return {
            "Región I": 0,         # Región I (0 para x < 0)
            "Región II": self._V0, # Región II (V0 entre 0 y a)
            "Región III": 0        # Región III (0 para x > a)
        }

    def equilibrium_points(self):
        return (
            f"Equilibrio indiferente en los intervalos ({-sp.oo}, 0), (0, {self._a}) y ({self._a}, {sp.oo}), "
            f"Equilibrio inestable límite en los puntos {self.boundary_points()}"
        )

    def boundary_points(self):
        return (0, self._a)

    def boundary_conditions(self, wave_function_I, wave_function_II, wave_function_III):
        return {
            wave_functionI.subs(self._x, 0): wave_function_II.subs(self._x, 0),               # psi_I(0) = psi_II(0)
            wave_function_II.subs(self._x, self._a): wave_function_III.subs(self._x, self._a) # psi_II(a) = psi_III(a)
        }

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
        H = T + V # Añadir para diferentes regiones de V
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
pot_barr = PotentialBarrier(x, 10, 1)
well = InfiniteWell(x)

#particle_well = QuantumSystem(x, well)
#particle_barr = QuantumSystem(x, pot_barr)

pprint("POZO DE POTENCIAL")
pprint(well.equilibrium_points())
pprint("La ecuación a resolver es:")
#pprint(particle_well.solve())
pprint("\n")

pprint("BARRERA DE POTENCIAL")
pprint(pot_barr.equilibrium_points())
pprint("La ecuación a resolver es:")
#pprint(particle_barr.solve())

# Nos arroja error dado que V es un diccionario, y no esta definida T + V 