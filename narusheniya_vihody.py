#!/usr/bin/python3.2
#*- coding: utf-8 -*-
'''
Created on 30 нояб. 2013 г.

@author: Alexandr
'''
from PyQt4 import QtGui, QtCore
class NV(QtGui.QLabel):
    '''
    classdocs
    '''


    def __init__(self, col="white", parent=None):
        '''
        Constructor
        '''
        QtGui.QWidget.__init__(self, parent)
        self.bl = ''
        self.id = 0
        
        self.style        = "QLabel{background-color: black; border-radius: 30px; border-color:white; border-width: 2px; border-style: solid; color: white}"
        self.style_yellow = "QLabel{background-color: yellow; border-radius: 30px; border-color:white; border-width: 2px; border-style: solid; color: black}"
        self.style_green  = "QLabel{background-color: green; border-radius: 30px; border-color:white; border-width: 2px; border-style: solid; color: black }"
        
        self.setStyleSheet(self.style)
        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    
    def plus(self):
        if self.bl == '':
            self.bl = 'ЗВ'
            self.setText(self.bl)
            self.setStyleSheet(self.style_green)
        elif self.bl == 'ЗВ':
            self.bl = 'В'
            self.setText(self.bl)
            self.setStyleSheet(self.style_yellow)
        
    def minus(self):
        if self.bl=='В':
            self.bl = 'ЗВ'
            self.setText(self.bl)
            self.setStyleSheet(self.style_green)
        elif self.bl == 'ЗВ':
            self.bl = ''
            self.setText(self.bl)
            self.setStyleSheet(self.style)
        
    def sbros(self):
        self.bl = ''
        self.setText(self.bl)
        self.setStyleSheet(self.style)

    def setValue(self, bl):
        self.bl = bl
        if self.bl=='В':
            self.setText(self.bl)
            self.setStyleSheet(self.style_yellow)
        elif self.bl == 'ЗВ':
            self.setText(self.bl)
            self.setStyleSheet(self.style_green)
        elif self.bl == '':
            self.setText(self.bl)
            self.setStyleSheet(self.style)      
    '''
    def mousePressEvent(self, e): 
        if e.buttons() == QtCore.Qt.LeftButton:
            self.plus()
        elif e.buttons() == QtCore.Qt.RightButton:
            self.minus()
        self.emit(QtCore.SIGNAL("change_nv"), self.bl)
    '''    
    def resizeEvent(self, e):
        fnt = QtGui.QFont()
        fnt.setWeight(50)
        fnt.setPixelSize(self.height() * 0.75)
        self.setFont(fnt)  
        
if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    bl = NV()
    bl.resize(100,20)
    bl.show()
    
    sys.exit(app.exec_())        
