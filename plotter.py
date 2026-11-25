import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

class Plotter:

    def __init__(
        self,
        nrows=1, ncols=1, figsize=(6,6),
        grid=True, legend=True,
        colors=["#7961A8", "#5686B5", "#59A68D", "#D58C91"]
    ):
        # Numero de filas y columnas de la figura
        self.nrows = nrows
        self.ncols = ncols

        # Tamaño de la figura
        self.figsize = figsize

        # Otro parámetros
        self.grid = grid
        self.legend = legend
        self.colors = colors

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
        ax.grid(self.grid, alpha=0.2)
        if self.legend:
            ax.legend()

    def numerical_function(self, variable, expression, physical_parameters: dict):
        return sp.lambdify(
            variable,
            expression.subs(physical_parameters),
            "numpy"
        )

    def add_energy_levels(self, ax, y_e, i):
            ax.axhline(
                y_e,
                linestyle="--",
                color=self.get_color(i, self.colors),
                alpha=0.5
            )

    def get_color(self, i, colors: list):
        return colors[i % len(colors)]

class WaveFunctionPlotter(Plotter):

    def __init__(
        self,
        xaxis, wavefunctions: list, # instancias WaveFunctions
        physical_parameters: dict, # Símbolos a sustituir
        energy_scale=1.0, visual_scale=1.0, density_scale=1.0, # Escalas visuales
        **kwargs
    ):
        super().__init__(**kwargs)
        # Array de numpy para graficar en el eje x
        self.xaxis = xaxis
        
        self.wavefunctions = wavefunctions
        self.physical_parameters = physical_parameters

        # Parámetros para la visualización
        self.visual_scale = visual_scale
        self.density_scale = density_scale
        self.energy_scale = energy_scale

    def _plot(
        self,
        quantity: str, # wavefunction o density
        offset_energy=False,
        energy_parameters: dict = None, # Símbolos a sustituir
    ):

        fig, ax = self.create_figure()

        for i, wf in enumerate(self.wavefunctions):

            if quantity == "wavefunction":
                expr = wf.expression
                scale = self.visual_scale
                label = fr"$\psi_{{{wf.n}}}(x)$"

            elif quantity == "density":
                expr = wf.probability_density
                scale = self.density_scale
                label = fr"$|\psi_{{{wf.n}}}(x)|^2$"

            # Obtiene la función a graficar de acuerdo a los parámetros elegidos
            y, numerical_function, y_e = self._get_visual_scale(
                wf, expr, offset_energy, energy_parameters
            )

            # Graficamos
            ax.plot(
                self.xaxis,
                y,
                color=self.get_color(i, self.colors),
                label=label
            )

            # Lineas horizontales para el nivel de enegía
            #if offset_energy:
                #self.add_energy_levels(ax, y_e, i)

            # Sombrea el área bajo la curva
            self._add_density_shading(
                ax, self.xaxis, y, y_e, i
            )
        
        # Seleccionamos el título y labels correspondientes
        if quantity == "wavefunction":
            title = "Soluciones al Pozo de Potencial Infinito"
            if offset_energy:
                ylabel = r"$E$"
            else:
                ylabel = f"$\psi (x)$"

        elif quantity == "density":
            title = "Densidades de probabilidad del Pozo Infinito"
            if offset_energy:
                ylabel = r"$E$"
            else:
                ylabel = f"$|\psi (x)|^2$"

        # Configuramos los ejes con los parámetros seleccionados
        self.configure_axis(ax, title, "Posiciones" + f"$(x)$", ylabel)
        plt.show()

    def _get_visual_scale(self, wf, expr, offset_energy, energy_parameters=None):

        numerical_function = self.numerical_function(
            wf.variable,
            expr,
            self.physical_parameters
        )

        if offset_energy:
            energy = float(wf.E_n.subs(energy_parameters))
            energy_scale = self.energy_scale
        else:
            energy = 0

        return (
            self.visual_scale * numerical_function(self.xaxis)
            + self.energy_scale * energy,
            numerical_function,
            self.energy_scale * energy
        )

    def _add_density_shading(self, ax, xaxis, y1, y2, i):
            ax.fill_between(
                xaxis,
                y1, # Curva de la cual debajo sombrea
                y2, # Límite inferior del sombreado
                color=self.get_color(i, self.colors),
                alpha=0.3
            )

    def plot_wavefunctions(self):
        self._plot(
            quantity="wavefunction"
        )

    def plot_energystates(self, energy_parameters: dict):
        self._plot(
            quantity="wavefunction",
            offset_energy=True,
            energy_parameters=energy_parameters
        )

    def plot_probability_densities(self):
        self._plot(
            quantity="density"
        )

    def plot_energy_densities(self, energy_parameters):
        self._plot(
            quantity="density",
            offset_energy=True,
            energy_parameters=energy_parameters
        )