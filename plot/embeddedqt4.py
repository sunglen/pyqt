#!/usr/bin/env python
# coding=utf-8
# matplotlib example modified by Glen
# see matplotlib/figure.py for Figure Class Usage
# see matplotlib/axes/_axes.py for axes usage
# and for basic knowledge, see:
# https://matplotlib.org/tutorials/index.html

import sys
import time

#from matplotlib.backends.qt_compat import QtCore, QtWidgets
from PyQt4 import QtCore, QtGui
import numpy as np
from matplotlib.backends.backend_qt4agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self._main = QtGui.QWidget()
        self.setCentralWidget(self._main)
        layout = QtGui.QVBoxLayout(self._main)
        
        self.fig1=Figure(figsize=(5, 3))
        self.axes1=self.fig1.add_subplot(111)
        static_canvas = FigureCanvas(self.fig1)
        layout.addWidget(static_canvas)
        
        self.addToolBar(NavigationToolbar(static_canvas, self))
        #the following is OK, but on bottom
        #self.addToolBar(QtCore.Qt.BottomToolBarArea, NavigationToolbar(static_canvas, self))

        self.fig2=Figure(figsize=(5, 3))
        #self.axes2=self.fig2.add_subplot(111)
        self.axes2 = self.fig2.add_axes([0,0,1,1])
        self.dynamic_canvas = FigureCanvas(self.fig2)
        layout.addWidget(self.dynamic_canvas)
        layout.addWidget(NavigationToolbar(self.dynamic_canvas, self))
        
        #the following is OK, but cannot use in a QtGui.QWidget
        #self.addToolBar(QtCore.Qt.BottomToolBarArea,
        #                NavigationToolbar(self.dynamic_canvas, self))
        
        #self._static_ax = static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self.axes1.plot(t, np.tan(t), ".")
        static_canvas.draw()
        
        #self._dynamic_ax = dynamic_canvas.figure.subplots()
        self._timer = self.dynamic_canvas.new_timer(
            100, [(self._update_canvas, (), {})])
        self._timer.start()
        
        
    def _update_canvas(self):
        #self.dynamic_canvas.clear()
        self.axes2.clear()
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self.axes2.plot(t, np.sin(t + time.time()))
        self.dynamic_canvas.draw()


if __name__ == "__main__":
    qapp = QtGui.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()