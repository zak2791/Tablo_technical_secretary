#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

class DigitalClock(QtGui.QLCDNumber):
    def __init__(self, evl, evr, col_start = "yellow",col_stop = "gold", tm = 0.10, drc = -1, bg = True, beep = True, parent=None):
        super(DigitalClock, self).__init__(parent)
        self.drc = drc
        self.setSegmentStyle(QtGui.QLCDNumber.Filled)
        self.setDigitCount(4)
        
        if bg:
            self.setStyleSheet("background-color: rgb(0,0,0,210);")
        #else:
            #self.setStyleSheet(open("./style_green.qss","r").read())
            #pass
        
        self.fl_val = 1
        self.fl_state = False
        self.beep = beep
        
        self.setFrameShape(True)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.tm = tm
        
        self.textTime = ''  #текст времени боя
        
        self.pal_start=QtGui.QPalette()
        self.pal_start.setColor(QtGui.QPalette.Window, QtGui.QColor("black"))
        self.pal_start.setColor(QtGui.QPalette.WindowText, QtGui.QColor(col_start))

        self.pal_stop=QtGui.QPalette()
        self.pal_stop.setColor(QtGui.QPalette.Window, QtGui.QColor("black"))
        self.pal_stop.setColor(QtGui.QPalette.WindowText, QtGui.QColor(col_stop))
    
        self.setPalette(self.pal_stop)
        self.setAutoFillBackground(True)

        self.clearTimer()
        
        self.setSegmentStyle(1)
        self.setFrameShape(QtGui.QFrame.Box)
        self.setLineWidth(2)
        self.ev_L = evl
        self.ev_R = evr
        self.pastTime = QtCore.QTime(0,0,0,0)    #прошедшее время боя
        
    def startstop(self):
        if self.timer.isActive():
            self.timer.stop()
            self.fl_state = False
            self.setPalette(self.pal_stop)
            self.emit(QtCore.SIGNAL("state"),0)
            if self.beep:
                QtGui.QApplication.beep()
        else:
            if self.fl_val != -1:   
                self.timer.start(1000)
                self.fl_state = True
                self.setPalette(self.pal_start)
                self.fl_val = 0
                if self.beep:
                    QtGui.QApplication.beep()
        self.emit(QtCore.SIGNAL("sec_sig(QString, QPalette)"), self.textTime, self.palette())
        self.emit(QtCore.SIGNAL("sec_visible(bool)"), self.isVisible())
                
    def clearTimer(self):
        if not self.timer.isActive():
            if self.drc == 1:
                self.time = QtCore.QTime(0,0,0,0)
            else:
                self.time = QtCore.QTime(0, int(self.tm), round((self.tm - int(self.tm))*100 - self.drc), 0)
            self.pastTime = QtCore.QTime(0,0,0,0)
            self.showTime()
            self.fl_val = 1
        self.pastTime = QtCore.QTime(0,0,0,0)
            
    def showTime(self):
        if not (self.timer.isActive() == False
                and self.drc == 1
                and self.time == QtCore.QTime(0,0,0,0)):
            self.time = self.time.addSecs(self.drc)
        self.textTime = self.time.toString('mm:ss')
        self.display(self.textTime)
        
        if (self.drc == -1 and self.textTime == "00:00") or (self.drc == 1 and self.textTime == "0" + str(self.tm)[0] + ":" + str(self.tm)[2] + "0"):
            self.timer.stop()
            self.setPalette(self.pal_stop)
            self.fl_state = False
            self.fl_val = -1
            self.sound()
        self.pastTime = self.pastTime.addSecs(1)
        ps = self.pastTime.toString("mm:ss")
        self.emit(QtCore.SIGNAL("past_time(QString)"), ps)
        self.emit(QtCore.SIGNAL("sec_sig(QString, QPalette)"), self.textTime, self.palette())

    def customEvent(self, e):
        if e.type() == self.ev_L:
            if self.fl_val != -1: 
                self.startstop()
        elif e.type() == self.ev_R:
            self.clearTimer()
            
    def sound(self):
        self.emit(QtCore.SIGNAL("sound"))

    def setTime(self, m, s1, s2):
        self.tm = m + s1 / 10.0 + s2 / 100.0
        self.clearTimer()

    def getLastTime(self):
        return self.time.toString("m:ss")
    
    def showLastTime(self, s):
        self.time.setHMS(0, int(s.split(":")[0]), int(s.split(":")[1]));
        t = self.time.toString("mm:ss");
        self.display(t);
        self.emit(QtCore.SIGNAL("sec_sig(QString, QPalette)"), t, self.palette())

    def doubleTime(self, t, p):
        self.display(t)
        self.setPalette(p)
        self.repaint()
        
    def sec_visible(self, b):
        self.emit(QtCore.SIGNAL("sec_visible(bool)"), b)

    def isActive(self):
        return self.timer.isActive()

    def getVisible(self):
        return self.isVisible()

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    clock = DigitalClock(0,0,"salmon","red",0.10,-1)#  orangered
    clock.setWindowTitle("Digital Clock")
    clock.resize(150, 60)
    clock.show()
    clock.startstop()
    sys.exit(app.exec_())

