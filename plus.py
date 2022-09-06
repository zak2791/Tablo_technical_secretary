
from PyQt4 import QtGui, QtCore

class plus(QtGui.QLabel):
    '''
    classdocs
    '''


    def __init__(self, col="yellow", parent=None):
        '''
        Constructor
        '''
        QtGui.QWidget.__init__(self, parent)
        self.setColor(col)
        #palW =  self.palette()
        #fnt = QtGui.QFont()
        #fnt.setPixelSize(self.height()*0.3)
        
        #self.setText("+")
        
        #palW.setColor(QtGui.QPalette.WindowText, QtGui.QColor(col))
        #self.setPalette(palW)
        #self.setFont(fnt)
        #self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.parent = parent
        
    def resizeEvent(self, e):
        fnt = QtGui.QFont()
        fnt.setWeight(50)
        fnt.setPixelSize(self.height() / 1.8)   #*2)
        self.setFont(fnt)
        #self.setText('+')

    def setColor(self, col):
        palW =  self.palette()
        palW.setColor(QtGui.QPalette.WindowText, QtGui.QColor(col))
        self.setPalette(palW)
        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


    def getText(self):
        return self.text()

    def setData(self, s):
        self.setText(s)
        self.emit(QtCore.SIGNAL("textChange(QString)"), self.text())

    
    '''   
    def change(self):
        if self.text == '+':
            pass    #self.text = ''
        else:
            pass    #self.text = '+'
    '''
