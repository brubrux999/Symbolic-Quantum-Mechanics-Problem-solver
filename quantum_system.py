import sympy as sp
import math_tools as mt

class QuantumSystem():

    def __init__(self, x, potential):
        # Recibe el potencial y la variable a la que depende
        self._x = x
        self._potential = potential
        self._L = sp.Symbol("L", positive=True) # Debería estar como propiedad del potencial

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

        # MÉTODO PARA RESOLVER EL POZO DE POTENCIAL INFINITO (V = 0)

        general_sol = sp.dsolve(self._equation, self._psi(self._x)).rhs

        # Simplificamos el argumento de las funciones trigonométricas mediante k
        k = sp.Symbol('k', positive=True)
        k_expr = sp.sqrt(2 * self._m * self._E) / self._hbar
        general_sol = mt.Simplify.apply(
            general_sol, k_expr, k
        )

        # Extraemos las constantes
        constants = mt.FilterSymbols.apply(
            general_sol, excluded_symbols=[k, self._x], cte=True
        )
        general_sol = mt.FilterSymbols.apply(
            general_sol, excluded_symbols=[k, self._x]
        )

        # Aplicamos condiciones de frontera
        conditions = mt.BoundaryConditions.apply(
            general_sol, self._x, 0, 0, self._L, 0
        )

        # Creamos y resolvemos el sistema lineal con las condiciones y constantes
        matrix = mt.Matrix.apply(
            mode="build", conditions=conditions, constants=constants
        )
        k_values = mt.Matrix.apply(
            mode="solve", matrix=matrix, variable=k, N=50, 
        )

        # Obtenemos los estados y energías
        E_n = mt.EigenSystem.apply(
            mode="energy",
            symbol=k,
            symbol_expr=k_expr,
            energy_symbol=self._E,
            k_values=k_values
        )

        psi_n = mt.EigenSystem.apply(
            mode="states",
            expr=general_sol,
            symbol=k,
            constants=constants,
            conditions=conditions,
            k_values=k_values
        )

        return E_n, psi_n

    def wave_function(self):
        ...