import sympy as sp
from sympy import pprint
from quantum_system import QuantumSystem
from potentials import *

sp.init_printing()

# Símbolos globales
x, p = sp.symbols("x p", real=True)

# Pequeña prueba para ver que todo se ejecute correctamente
well = InfiniteWell(x)
oscillator = HarmonicOscillator(x)

particle_well = QuantumSystem(x, well)
particle_oscillator = QuantumSystem(x, oscillator)

pprint("POZO DE POTENCIAL")
pprint("La ecuación a resolver es:")
pprint(particle_well.equation)
pprint("La solución es:")
pprint(particle_well.solve())
pprint("\n")