#!C:\Python34\python
# -*- coding: utf-8 -*-
'''
Created on 22 окт. 2013 г.

@author: Alexandr
'''
from PyQt4 import QtGui, QtCore

class Ball(QtGui.QLabel):
    '''
    classdocs
    '''
    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtGui.QWidget.__init__(self, parent)
        
        self.bl = 0
        self.id = 0
        '''
        self.max_num = max_num
        if max_num < 10:
            self.diff_font = False
        else:
            self.diff_font = diff_font
        '''
        #self.setStyleSheet(open("./" + style, "r").read())
        #palW = self.palette()

        self.setStyleSheet('''QLabel{border-radius: 30px; border-width: 2px;
                              border-style: solid; border-color:white;
                              background-color: black; color: white;}''');
        
        self.setAutoFillBackground(True)
        
      
        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        sp = QtGui.QSizePolicy.Ignored
        self.setSizePolicy(sp,sp)
        
        self.fnt1 = QtGui.QFont()
        self.fnt2 = QtGui.QFont()

        #self.show()
        
    def plus(self):
        if self.bl < 99:
            self.bl += 1
            if self.bl == 10:
                self.setFont(self.fnt2)
            self.setText(str(self.bl))
            self.emit(QtCore.SIGNAL("ball(int)"), self.bl)
            
    def minus(self):
        if self.bl > 0:
            self.bl -= 1
            if self.bl == 9:
                self.setFont(self.fnt1)
            self.setText(str(self.bl))
            self.emit(QtCore.SIGNAL("ball(int)"), self.bl)
                
    def sbros(self):
        self.bl = 0
        self.setFont(self.fnt1)
        self.setBall(self.bl)
        #self.emit(QtCore.SIGNAL("ball(int)"), self.bl)
        
    '''
    def mousePressEvent(self, e): 
        if e.buttons() == QtCore.Qt.LeftButton:
            self.plus()
        elif e.buttons() == QtCore.Qt.RightButton:
            self.minus()
    '''
    def setBall(self, ball):
        if ball < 10:
            self.setFont(self.fnt1)
        else:
            self.setFont(self.fnt2)
        self.bl = ball
        self.setText(str(self.bl))
        self.emit(QtCore.SIGNAL("ball(int)"), self.bl)

    def setViewStyle(self, s, width):
        if s == 0:
            self.setStyleSheet("QLabel{border-radius: 30px; border-width: "
                               + str(width)
                               + "px; border-style: solid; border-color:white; background-color: black; color: white;}")
        elif s == 1:
            self.setStyleSheet("QLabel{border-radius: 30px; border-width: "
                                   + str(width)
                                   + "px; border-style: solid; border-color:white; background-color: black; color: red;}")
        elif s == 2:
            self.setStyleSheet("QLabel{border-radius: 30px; border-width: "
                               + str(width)
                               + "px; border-style: solid; border-color:white; background-color: black; color: blue;}")
        elif s == 3:
            self.setStyleSheet("QLabel{background-color: black; color: red; border-width: 0px; border-style: solid;}")
        elif s == 4:
            self.setStyleSheet("QLabel{background-color: black; color: blue; border-width: 0px; border-style: solid;}")
        
    def resizeEvent(self,e):
        self.fnt1.setWeight(50)
        self.fnt1.setPixelSize(self.height() * 2)
        fm = QtGui.QFontMetrics(self.fnt1)
        self.fnt2.setWeight(50)
        self.fnt2.setPixelSize(self.height() * 2)
        a = self.height() * 1.05
        st1 = '0'
        st2 = '00'
        while True:
            self.fnt1.setPixelSize(a)
            self.setFont(self.fnt1)
            fm = QtGui.QFontMetrics(self.fnt1)
            if fm.width(st1) < self.width():
                break
            if a > 20:
                a -= 20
            else:
                break
        a = self.height() * 1.05
        while True:
            self.fnt2.setPixelSize(a)
            self.setFont(self.fnt2);
            fm = QtGui.QFontMetrics(self.fnt2)
            if fm.width(st2) < self.width():
                break;
            if a > 20:
                a -= 20
            else:
                break
        if self.bl > 9:
            self.setFont(self.fnt2)
        else:
            self.setFont(self.fnt1)
        self.setText(str(self.bl))
      
if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    bl = Ball()
    bl.resize(100,20)

    bl.show()
    bl.setBall(5)


    sys.exit(app.exec_())
        
