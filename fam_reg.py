#!/usr/bin/python3.2
# -*- coding: utf-8 -*-
'''
Created on 24 окт. 2013 г.

@author: Alexandr
'''

from PyQt4 import QtGui, QtCore

class Fam(QtGui.QLabel):
    '''
    classdocs
    '''


    def __init__(self, cl = "yellow", tx = "text", wt = 10, fn = '', parent=None):
        '''
        Constructor
        '''
        QtGui.QWidget.__init__(self, parent)
        #self.resize(600,50)
        self.tx = tx
 
        self.setStyleSheet("QLabel{background-color: black; color: " + cl + "; }")
        self.setAutoFillBackground(True)
        self.wt = wt  #жирность шрифта
   
        sp = QtGui.QSizePolicy.Ignored
        self.setSizePolicy(sp,sp)
        if fn == '':
            self.fn = QtGui.QFont()
        else:
            self.fn = QtGui.QFont(fn)
        self.align = 0                  #0-центр
                                        #1-левый край
                                        #2-правый край

    def setViewStyle(self, s):
        if s == 0:
            self.setStyleSheet("QLabel{background-color: black; color: white; }")
        elif s == 1:
            self.setStyleSheet("QLabel{background-color: black; color: red; }")
        else:
            self.setStyleSheet("QLabel{background-color: black; color: blue; }")

    def text(self, t):    
         self.tx = t
         self.repaint()
         self.emit(QtCore.SIGNAL("sigText(QString)"), t)

    def getText(self):
        return self.tx
        
    def paintEvent(self,e):
        self.fn.setPixelSize(self.height() / 0.9)
        self.fn.setWeight(self.wt) #63
        self.setFont(self.fn)
        
        pn = QtGui.QPainter()
        pn.begin(self)

        p=QtGui.QFontMetrics(self.font())
        
        if p.width(self.tx) >= self.width():
            pn.drawText(0, self.height() * 0.9, self.tx)
        else:
            if self.align == 0:
                pn.drawText((self.width() - p.width(self.tx)) / 2, self.height() * 0.9, self.tx)
            elif self.align == 1:
                pn.drawText(0, self.height() * 0.9, self.tx)
            elif self.align == 2:
               pn.drawText(self.width() - p.width(self.tx), self.height() * 0.9, self.tx)
        if self.align == 0 or self.align == 1 or p.width(self.tx) >= self.width():       
            gr = QtGui.QLinearGradient(self.width() * 0.85, 0, self.width(), 0)
            gr.setColorAt(0, QtGui.QColor(0,0,0,0))
            gr.setColorAt(1, QtGui.QColor(0,0,0,255))
            pn.setBrush(gr)
        
        pn.setPen(QtCore.Qt.NoPen)
        pn.drawRect(0, 0, self.width(), self.height())
        
        pn.end()
        
        
        
if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    fm = Fam()
    fm.resize(200,200)
    fm.show()
    
    sys.exit(app.exec_())
