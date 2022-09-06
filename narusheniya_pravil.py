#*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
import time

class Blinks(QtCore.QObject):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        self.current_state = False;

    def process(self):
        while True:
            time_ms = QtCore.QTime.currentTime().msec()
            if time_ms > 0 and time_ms < 19 and not self.current_state:
                self.emit(QtCore.SIGNAL("blink_turn(bool)"), True)
                self.current_state = True
            elif time_ms > 500 and time_ms < 519 and self.current_state:
                self.emit(QtCore.SIGNAL("blink_turn(bool)"), False)
                self.current_state = False
            QtCore.QThread.msleep(10)
                
class NP(QtGui.QLabel):
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
        self.style_red    = "QLabel{background-color: red; border-radius: 30px; border-color:white; border-width: 2px; border-style: solid; color: black}"
        self.style_yellow = "QLabel{background-color: yellow; border-radius: 30px; border-color:white; border-width: 2px; border-style: solid; color: black}"
        self.style_green  = "QLabel{background-color: green; border-radius: 30px; border-color:white; border-width: 2px; border-style: solid; color: black }"
        self.setStyleSheet(self.style)
        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.thread = QtCore.QThread()
        self.blinks = Blinks()
        self.blinks.moveToThread(self.thread)

        QtCore.QObject.connect(self.blinks, QtCore.SIGNAL("blink_turn(bool)"), self.prg)
        QtCore.QObject.connect(self.thread, QtCore.SIGNAL("started()"), self.blinks.process)

        self.thread.start()

    def prg(self, b):
        if self.bl == "П2":
            if b:
                self.setStyleSheet(self.style)
            else:
                self.setStyleSheet(self.style_red)
    '''  
    def set_red(self):
        if self.bl == 'П2':
            self.setStyleSheet(self.style_red)

    def set_black(self):
        if self.bl == 'П2':
            self.setStyleSheet(self.style)
    '''  
    def plus(self):
        if self.bl == '':
            self.bl = 'ЗП'
            self.setText(self.bl)
            self.setStyleSheet(self.style_green)
        elif self.bl == 'ЗП':
            self.bl = 'П1'
            self.setText(self.bl)
            self.setStyleSheet(self.style_yellow)
        elif self.bl == 'П1':
            self.bl = 'П2'
            self.setText(self.bl)
            self.setStyleSheet(self.style_red)
       
    def minus(self):
        if self.bl=='П2':
            self.bl = 'П1'
            self.setText(self.bl)
            self.setStyleSheet(self.style_yellow)
        elif self.bl == 'П1':
            self.bl = 'ЗП'
            self.setText(self.bl)
            self.setStyleSheet(self.style_green)
        elif self.bl == 'ЗП':
            self.bl = ''
            self.setText(self.bl)
            self.setStyleSheet(self.style)    
        
    def sbros(self):
        self.bl = ''
        self.setText(self.bl)
        self.setStyleSheet(self.style)
        
    def setValue(self, bl):
        self.bl = bl
        if self.bl == 'П2':
            self.setText(self.bl)
            self.setStyleSheet(self.style_red)
        elif self.bl=='П1':
            self.setText(self.bl)
            self.setStyleSheet(self.style_yellow)
        elif self.bl == 'ЗП':
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
        self.emit(QtCore.SIGNAL("change_np"), self.bl)
    '''       
    def resizeEvent(self, e):
        fnt = QtGui.QFont()
        fnt.setWeight(50)
        fnt.setPixelSize(self.height() * 0.75)
        self.setFont(fnt)   
        
 
if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    bl = NP()
    bl.resize(100,20)
    bl.show()
    
    sys.exit(app.exec_())        
