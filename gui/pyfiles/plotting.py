import random

from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100, labels=None, counts=None):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.ax = None

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot(labels, counts)

    def plot(self, labels, counts):
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title('Clasificaciones')
        self.draw()

    def do_update(self, labels, counts):
        self.ax.set_xticklabels(labels)
        x = np.arange(len(labels))  # the label locations
        self.ax.set_xticks(x)
        width = 0.7
        rects1 = self.ax.bar(x, counts, width)
        self.ax.legend()
        self.draw()

