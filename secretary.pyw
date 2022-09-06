#!E:\Python34\pythonw
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore, uic

class Secretary(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi("WindowSecretary.ui", self)
        pal = self.palette()
        pal.setColor(QtGui.QPalette.Window, QtGui.QColor("white"))
        self.setPalette(pal)
        self.setAutoFillBackground(True)

     

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    secr = Secretary()
    #secr.resize(1000, 240)
    secr.show()
    sys.exit(app.exec_())
