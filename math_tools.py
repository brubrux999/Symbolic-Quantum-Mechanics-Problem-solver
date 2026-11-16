from abc import ABC, abstractmethod

class MathTools(ABC):

    @staticmethod
    @abstractmethod
    def apply(expr, **kwargs):
        pass

class Simplify(MathTools):

    @staticmethod
    def apply(expr, old, new):
        ...

class FilterSymbols(MathTools):

    @staticmethod
    def extract_symbols(expr):
        ...

    @staticmethod
    def exclude_constants(expr, excluded_symbols):
        ...

    @staticmethod
    def substitute_constants(expr, excluded_symbols):
        ...

    @staticmethod
    def apply(expr, mode, **kwargs):
        ...

def BoundaryConditions(MathTools):

    @staticmethod
    def apply(expr, var, arg1, imag1, arg2, imag2):
        ...

class Matrix(MathTools):

    @staticmethod
    def build_matrix(conditions, constants):
        ...

    @staticmethod
    def nontrivial_solution(matrix, variable):
        ...