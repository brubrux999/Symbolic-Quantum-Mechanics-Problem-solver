import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

class Plotter:

    def __init__(
        self,
        physical_parameters: dict,
        nrows=1, ncols=1, figsize=(10,6),
        grid=True, legend=True
    ):
        # Valores a sustituir como hbar, longitud del pozo, etc
        self.physical_parameters = physical_parameters

        # Numero de filas y columnas de la figura
        self.nrows = nrows
        self.ncols = ncols

        # Tamaño de la figura
        self.figsize = figsize

        # Otro parámetros
        self.grid = grid
        self.legend = legend

    def create_figure(self):
        self.fig, self.ax = plt.subplots(
            nrows=self.nrows,
            ncols=self.ncols,
            figsize=self.figsize
        )
        return self.fig, self.ax

    def configure_axis(self, ax, title: str, xlabel: str, ylabel: str):
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(self.grid)
        ax.legend(self.legend)

    def numerical_function(self, variable, expression):
        return sp.lambdify(
            variable,
            expression.subs(self.physical_parameters),
            "numpy"
        )

class WaveFunctionPlotter(Plotter):

    def __init__(self, xaxis, wavefunctions: list, color="blue", **kwargs):
        super().__init__(**kwargs)
        # Array de numpy para graficar en el eje x
        self.xaxis = xaxis
        
        # Lista con instancias WaveFunctions
        self.wavefunctions = wavefunctions

        # Parámetros para la visualización
        self.color = color

    def plot(self):
        # Creamos la figura y los ejes
        fig, ax = self.create_figure()

        # Hacemos numérica cada función y la graficamos
        for wf in self.wavefunctions:

            psi = self.numerical_function(
                wf.variable,
                wf.expression,
            )

            ax.plot(
                self.xaxis,
                psi(self.xaxis),
                color=self.color,
                label=fr"$\psi_{{{wf.n}}}(x)$"
            )

        # Configuramos la visualización
        self.configure_axis(self.ax, "Pozo de potencial infinito", "Position", "Energy")

        # Mostramos o guardamos la figura
        plt.show()

class ProbabilityDensityPlotter(Plotter):

    def plot(self):
        ...