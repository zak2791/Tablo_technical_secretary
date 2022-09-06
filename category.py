#!C:\Python34\python
# -*- coding: utf-8 -*-
'''
Created on 22 окт. 2013 г.

@author: Alexandr
'''
from PyQt4 import QtGui, QtCore

class Category(QtGui.QLabel):
    '''
    classdocs
    '''
    def __init__(self, style = "style_category.qss", parent=None):
        '''
        Constructor
        '''
        QtGui.QWidget.__init__(self, parent)
   
        #self.setAutoFillBackground(True)
        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        sp = QtGui.QSizePolicy.Ignored
        self.setSizePolicy(sp,sp)

        self.fnt = QtGui.QFont()
  
    def resizeEvent(self,e):
        self.fnt.setPixelSize(self.height() * 0.8)
        self.setFont(self.fnt)
        self.setText(self.text())

    def setData(self, s):
        self.setText(s)
        self.emit(QtCore.SIGNAL("sigText(QString)"), s)
      
if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    cat = Category()
    cat.resize(100,200)

    cat.show()
    cat.setText('+85')


    sys.exit(app.exec_())
        
