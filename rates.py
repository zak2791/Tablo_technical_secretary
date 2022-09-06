#!E:\Python34\pythonw
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

class Name(QtGui.QGraphicsItem):
    def __init__(self, parent=None):
        QtGui.QGraphicsItem.__init__(self, parent)

        self.Name = ""
        self.status = 0    #если 0: текст, 1: обведенный текст, 2: перечеркнутый текст
        self.w = 0
        self.h = 0
        self.f = QtGui.QFont()

    def setName(self, name):
        self.Name = name
        print(self.Name)

    def setStatus(self, status):
        self.status = status
        print("status = ", status)
        self.update()

    def boundingRect(self):
        penWidth = 1.0
        return QtCore.QRectF(-self.w / 2 - penWidth / 2, -self.h / 2 - penWidth / 2,
                             self.w + penWidth, self.h + penWidth)

    def paint(self, p, opt, wid):
        p.setFont(self.f)
        p.fillRect(-self.w / 2, -self.h / 2, self.w, self.h, QtGui.QColor("white"))
        '''
        try:
            n = self.Name.split(":")
            name = n[1] + " (" + n[0] + ")"
        except:
            name = self.Name
        '''   
        p.drawText(-self.w / 2 + 10, -self.h / 2, int(self.w) - 10, int(self.h),
                   QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, self.Name)
        #p.drawLine(0, self.h / 4, self.h / 4, self.h / 4)
        if self.status == 1:
            p.drawEllipse(-self.w / 2 + 10, -self.h / 2 + 10, self.w - 20, self.h - 20)
        elif self.status == 2:
            p.drawLine(-self.w / 2 + 10, -self.h / 2 + 10, self.w / 2 - 10, self.h / 2 - 10)
            p.drawLine(self.w / 2 - 10, -self.h / 2 + 10, -self.w / 2 + 10, self.h / 2 - 10)

    def setSize(self, w, h):
        self.w = w
        self.h = h
        self.f.setPixelSize(self.h / 5)
        
class Rate(QtGui.QGraphicsItem):
    def __init__(self, rate, parter=False,      #если True: нарисовать кружок
                             strike = False,    #если True: не выделять при наведении мыши
                             value = 0,
                             parent=None):
        QtGui.QGraphicsItem.__init__(self, parent)
        self.w = 0
        self.h = 0
        self.f = QtGui.QFont()
        self.rate = rate
        self.parter = parter
        self.setAcceptHoverEvents(True)
        self.color = QtGui.QColor("white")
        self.strikethrough = False          #если True: отобразить зачеркнутым
        self.flagNoStrikethrough = strike
        self.value = value

    def getValue(self):
        return self.value

    def boundingRect(self):
        penWidth = 1.0
        return QtCore.QRectF(-self.w / 2 - penWidth / 2, -self.h / 2 - penWidth / 2,
                             self.w + penWidth, self.h + penWidth)

    def paint(self, p, opt, wid):
        p.setFont(self.f)
        p.fillRect(-self.w / 2, -self.h / 2, self.w, self.h, self.color)
        if self.parter:
            p.drawEllipse(-self.h / 2, -self.h / 2, self.h, self.h)
        
        p.drawText(-self.w / 2, -self.h / 2, int(self.w), int(self.h), QtCore.Qt.AlignCenter, self.rate)
        if self.strikethrough:
            p.drawLine(-self.w / 2, -self.h / 2, self.w / 2, self.h / 2)
            p.drawLine(self.w / 2, -self.h / 2, -self.w / 2, self.h / 2)

    def setSize(self, w, h):
        self.w = w
        self.h = h
        self.f.setPixelSize(self.h)
    
    def sceneEvent(self, e):
        if not self.flagNoStrikethrough:
            penWidth = 1
            if e.type() == QtCore.QEvent.GraphicsSceneHoverEnter:
                self.color = QtGui.QColor("gray")
                self.update(QtCore.QRectF(-self.w / 2 - penWidth / 2, -self.h / 2 - penWidth / 2,
                                 self.w + penWidth, self.h + penWidth))
            if e.type() == QtCore.QEvent.GraphicsSceneHoverLeave:
                self.color = QtGui.QColor("white")
                self.update(QtCore.QRectF(-self.w / 2 - penWidth / 2, -self.h / 2 - penWidth / 2,
                                 self.w + penWidth, self.h + penWidth))
        return True
 
