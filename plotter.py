import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

class Plotter:

    def __init__(
        self,
        physical_parameters: dict,
        nrows=0, ncols=0, figsize=(10,6),
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

    def configure_axis(self, ax, title: str, xlabel: str, ylabel: str):
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(self.grid)
        ax.legend(self.legend)

class WaveFunctionPlotter(Plotter):

    def __init__(self, color="blue", **kwargs):
        super().__init__(**kwargs)
        self.color = color

    def plot(self, x, y):
        
        # Creamos la figura y los ejes
        self.create_figure()

        # Graficamos las funciones
        self.ax.plot(x, y, color=self.color)

        # Configuramos la visualización
        self.configure_axis(self.ax, "Quantum state i", "Position", "Energy")

        # Mostramos o guardamos la figura
        plt.show()

class ProbabilityDensityPlotter(Plotter):

    def plot(self):
        ...