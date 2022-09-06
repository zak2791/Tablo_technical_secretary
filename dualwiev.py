#!C:\Python34\pythonw
# -*- coding: utf-8 -*-
import sys
import os
import first, ball, fam_reg, plus
from PyQt4 import QtGui, QtCore

import narusheniya_pravil
import narusheniya_vihody
import category

class desktop(QtGui.QWidget):
    def __init__(self,  evl, evr, view, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.View = view
        
        self.minimum_height = 0
        self.percent_height = 0
        
        #self.setWindowState(QtCore.Qt.WindowFullScreen)
        self.setCursor(QtCore.Qt.BlankCursor)
        
        palW = self.palette()
        palW.setColor(QtGui.QPalette.Window,QtGui.QColor("black"))
        palW.setColor(QtGui.QPalette.WindowText, QtGui.QColor("yellow"))
        self.setPalette(palW)      
        
        self.evl = evl
        self.evr = evr
        
        
        #первое техн. для вывода в сеть
        #self.pl_l = ' '
        #self.pl_r = ' '
        ################################
       
        self.flag = QtGui.QPixmap()
        
        self.flag_blue = QtGui.QLabel(self)
        self.flag_blue.setScaledContents(True)

        self.flag_red = QtGui.QLabel(self)
        self.flag_red.setScaledContents(True)
        
        col_left = 'white'#'lightblue'#'steelblue'
        col_right = 'white'#'hotpink'
        
        #fnt = QtGui.QFont()

        desk = QtGui.QApplication.desktop()

        self.form_vis = 0                           #видимая форма

        self.ves = [' ','6','0','кг']
        
        
##################################################################################
       
        self.kat = category.Category()#QtGui.QLabel()
        
        self.fam_blue = fam_reg.Fam(col_left,'',63)
        self.reg_blue = fam_reg.Fam(col_left,'',10,'Lucida Console')
        
        self.fam_red = fam_reg.Fam(col_right,'',63)
        self.reg_red = fam_reg.Fam(col_right,'',10,'Lucida Console')

        self.plus_left = plus.plus(col_left)
               
        self.plus_right = plus.plus(col_right)
                
        self.ball_left = ball.Ball()
        self.ball_left.setFrameShape(QtGui.QFrame.Box)
        self.ball_left.id = 1   
        
        self.ball_right = ball.Ball()
        self.ball_right.setFrameShape(QtGui.QFrame.Box)
        self.ball_right.id = 0
        
        self.akt_left = ball.Ball()
        self.akt_left.setFrameShape(QtGui.QFrame.Box)
        self.akt_left.id = 3
        
        self.akt_right  = ball.Ball()
        self.akt_right.setFrameShape(QtGui.QFrame.Box)
        self.akt_right.id = 2

        self.NV_left = narusheniya_vihody.NV()
        self.NP_left = narusheniya_pravil.NP()

        self.NV_right = narusheniya_vihody.NV()
        self.NP_right = narusheniya_pravil.NP()
           
################################################################################        
        self.sek = first.DigitalClock(self.evl, self.evr, "chartreuse","green", 1.30, -1, False, False)
        
        self.sek_left = first.DigitalClock(self.evl, self.evr, 'lightblue',"blue", 0.20, 1, True, False)
        
        self.sek_right = first.DigitalClock(self.evl, self.evr, "salmon", "red", 0.20, 1, True, False)
        
        self.sek_left.setVisible(False)
        self.sek_right.setVisible(False)

        self.sek_left_TV = first.DigitalClock(self.evl, self.evr, "lightblue", 'blue', 2.00,1, True, False)
        
        self.sek_right_TV = first.DigitalClock(self.evl, self.evr, "salmon", 'red', 2.00,1, True, False)
        
        self.sek_left_TV.setVisible(False)
        self.sek_right_TV.setVisible(False)
################################################################################        
        self.grid = QtGui.QGridLayout()
  
        self.grid.addWidget(self.kat, 14, 28, 6, 14)##############

        self.grid.addWidget(self.fam_blue, 0, 0,  6, 34)
        self.grid.addWidget(self.fam_red,  0, 34, 6, 34)

        self.grid.addWidget(self.ball_left,  6, 0,  18, 24)
        self.grid.addWidget(self.ball_right, 6, 44, 18, 24) 
        
        self.grid.addWidget(self.akt_left,  24,  0, 13, 14)###############
        self.grid.addWidget(self.akt_right, 24, 54, 13, 14)
        
        self.grid.addWidget(self.plus_left,  6, 24, 8, 8)
        self.grid.addWidget(self.plus_right, 6, 36, 8, 8)
        #self.plus_left.setVisible(False)
        #self.plus_right.setVisible(False)
        
        self.grid.addWidget(self.sek_left,     9, 0,  12,  24)
        self.grid.addWidget(self.sek_right,    9, 44, 12,  24)

        self.grid.addWidget(self.sek_left_TV,  9, 0,  12,  24)
        self.grid.addWidget(self.sek_right_TV, 9, 44, 12,  24)
        
        self.grid.addWidget(self.flag_blue,    29, 14, 8,  10)
        self.grid.addWidget(self.flag_red,     29, 44, 8,  10)
        
        self.grid.addWidget(self.sek,          24, 24, 13, 20)

        
        self.grid.addWidget(self.NP_right,     24, 19,  5,  5)
        self.grid.addWidget(self.NP_left,      24, 44,  5,  5)
        
        self.grid.addWidget(self.NV_right,     24, 14,  5,  5)
        self.grid.addWidget(self.NV_left,      24, 49,  5,  5)

        self.grid.addWidget(self.reg_blue,      37, 0, 5 , 34)
        self.grid.addWidget(self.reg_red,     37, 34, 5, 34)
        
        self.setLayout(self.grid)
      
    def paintEvent(self,e):
        pn = QtGui.QPainter(self)
        #gr = QtGui.QLinearGradient(0,self.width(),self.width(),self.width())
        #gr.setColorAt(0.49,QtGui.QColor('blue'))###############
        #gr.setColorAt(0.51,QtGui.QColor('red'))####################
        #pn.setBrush(gr)
        pn.begin(self)
        pn.setPen(QtCore.Qt.NoPen)
        #print("self.View = ", self.View)
        if self.View == 0:
            pn.setBrush(QtCore.Qt.blue)
            pn.drawRect(0, 0, self.width() / 2, self.height())
            pn.setBrush(QtCore.Qt.red)
            pn.drawRect(self.width() / 2, 0, self.width() / 2, self.height())
        else:
            pn.setBrush(QtCore.Qt.black)
            pn.drawRect(0, 0, self.width(), self.height())

        pn.end()

    def showEvent(self, e):
        self.minimum_height = (self.height() - 12) / 42
        self.percent_height = (self.height() - 12) / 100
        self.grid.setRowMinimumHeight(0, self.minimum_height)
        self.grid.setRowMinimumHeight(1, self.minimum_height)
        self.grid.setRowMinimumHeight(2, self.minimum_height)
        self.grid.setRowMinimumHeight(3, self.minimum_height)
        self.grid.setRowMinimumHeight(4, self.minimum_height)
        self.grid.setRowMinimumHeight(5, self.minimum_height)
        self.grid.setRowMinimumHeight(37, self.minimum_height)
        self.grid.setRowMinimumHeight(38, self.minimum_height)
        self.grid.setRowMinimumHeight(39, self.minimum_height)
        self.grid.setRowMinimumHeight(40, self.minimum_height)
        self.grid.setRowMinimumHeight(41, self.minimum_height)
        
