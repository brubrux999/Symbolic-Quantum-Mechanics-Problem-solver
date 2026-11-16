from abc import ABC, abstractmethod
from sympy import S, solveset, simplify
from sympy import (
    MatrixBase,
    Expr,
    Symbol
)

class MathTools(ABC):

    @staticmethod
    @abstractmethod
    def apply(expr: Expr, **kwargs):
        pass

class Simplify(MathTools):

    @staticmethod
    def apply(expr: Expr, old: Expr | Symbol, new):
        return expr.subs(old, new)

class FilterSymbols(MathTools):

    @staticmethod
    def extract_symbols(expr: Expr):
        return expr.free_symbols

    @staticmethod
    def exclude_constants(expr: Expr, excluded_symbols: list):
        return list(
            sorted(expr.free_symbols - set(excluded_symbols), key=str)
        )

    @staticmethod
    def substitute_constants(expr: Expr, excluded_symbols: list, cte: bool=False):
        original_constants = FilterSymbols.exclude_constants
        C1 = sp.Symbol(original_constants[0].name, real=True, nonzero=True)
        C2 = sp.Symbol(original_constants[1].name, real=True)
        constants = sorted([C1, C2], key=str)

        if cte:
            return constants

        return expr.subs({
            original_constants[0]: constants[0],
            original_constants[1]: constants[1]
        })

    @staticmethod
    def apply(expr: Expr, mode="substitute", **kwargs):
        
        operations = {
            "extract": FilterSymbols.extract_symbols,
            "exclude": FilterSymbols.exclude_constants,
            "substitute": FilterSymbols.substitute_constants
        }

        if mode not in operations:
            raise ValueError(f"Unknown mode: {mode}")

        return operations[mode](expr, **kwargs)

class BoundaryConditions(MathTools):

    @staticmethod
    def apply(expr: Expr, var: Symbol, arg1, imag1, arg2, imag2):
        return [
            sp.Eq(expr.subs(var, arg1), imag1, evaluate=False),
            sp.Eq(expr.subs(var, arg2), imag2, evaluate=False)
        ]

class Matrix(MathTools):

    @staticmethod
    def build_matrix(conditions: list, constants: list):
        return sp.Matrix(
            [
                [
                    sp.diff(condition.lhs, constant) for constant in constants
                ] for condition in conditions
            ]
        )

    @staticmethod
    def nontrivial_solutions(matrix: MatrixBase, variable: Symbol, N: int=100, dom=S.Reals):
        # Obtenemos una solución tipo ImageSet
        k_sol = simplify(
            solveset(
                matrix.det(),
                variable,
                domain=dom
            )
        )

        # Extraemos los N valores de k del ImageSet
        k_values = set()
        for branch in sol_k.args:
            j = branch.lamda.variables[0]
            for i in range(-N, N+1):
                value = sp.simplify(branch.lamda.expr.subs(j, i))
                if value.is_positive:
                    k_values.add(value)

        order = lambda v: float(v.subs({s: 1 for s in v.free_symbols}))
        return sorted(k_values, key=order)[:N]