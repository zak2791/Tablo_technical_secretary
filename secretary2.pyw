#!E:\Python34\pythonw
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import rates, queuefight
import socket, sqlite3
currentX = 0

class TcpClient(QtCore.QObject):
    def __init__(self, data, addr, parent=None):
        QtCore.QObject.__init__(self, parent)
        #self.addr = "192.168.0.100"
        #self.port = 1111
        self.data = data
        self.addr = addr
        print("self.addr = ", self.addr)

    def run(self):
        sock = socket.socket()
        sock.settimeout(0.1)
        try:
            sock.connect(self.addr)
            sock.send(self.data)
        except:
            print("err socket")
        finally:
            sock.close()

class LeftRightPushButton(QtGui.QPushButton):
    def __init__(self, parent=None):
        QtGui.QPushButton.__init__(self, parent)

    def mouseReleaseEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.emit(QtCore.SIGNAL("left_right_clicked(bool, QString)"), False, self.objectName())
        elif e.button() == QtCore.Qt.RightButton:
            self.emit(QtCore.SIGNAL("left_right_clicked(bool, QString)"), True, self.objectName())

class MyGraphicsView(QtGui.QGraphicsView):
    def __init__(self, parent=None):
        QtGui.QGraphicsScene.__init__(self, parent)

    def mouseDoubleClickEvent(self, e):
        global currentX
        if e.button() == QtCore.Qt.RightButton:
            item = self.itemAt(e.pos().x(), e.pos().y())
            if item == None:
                return QtGui.QWidget.mouseDoubleClickEvent(self, e)
            posX = item.pos().x()
            itemW = item.w
            l = self.scene().items(posX, e.pos().y(), self.scene().width() - posX, e.pos().y() + 1.0, 1)
            dialog = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Первое техническое действие!", "Вы уверены?",
                                           buttons=QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            result = dialog.exec_()
            if result == QtGui.QMessageBox.Ok:
                item = rates.Rate("+")
                item.setSize(self.height()/4.0, self.height()/3)
                item.setPos(posX - itemW / 2 + item.w / 2, self.height()/2)
                self.scene().addItem(item)
                currentX += item.w
                for each in l:
                    each.setPos(each.pos().x() + item.w, each.pos().y())
                self.emit(QtCore.SIGNAL("shift(int, int)"), item.w, posX)
        if e.button() == QtCore.Qt.LeftButton:
            item = self.scene().itemAt(e.pos().x(), e.pos().y())
            if item == None or item.flagNoStrikethrough == True:
                return QtGui.QWidget.mouseDoubleClickEvent(self, e)
            dialog = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Зачеркивание!", "Вы уверены?",
                                       buttons=QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            result = dialog.exec_()
            if result == QtGui.QMessageBox.Ok:
                item.strikethrough = True
                penWidth = 1
                item.update(QtCore.QRectF(-item.w / 2 - penWidth / 2, -item.h / 2 - penWidth / 2,
                                 item.w + penWidth, item.h + penWidth))
                self.emit(QtCore.SIGNAL("strike(int, int)"), item.pos().x(), item.pos().y())
            return QtGui.QWidget.mouseDoubleClickEvent(self, e)
    
class Secretary(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.q = None

        self.address = None
        self.mat = None

        self.vin = 0            #0 - нет победителя, 1 - синий, 2 - красный

        pal = self.palette()
        pal.setColor(QtGui.QPalette.Window, QtGui.QColor("white"))
        self.setPalette(pal)
        self.setAutoFillBackground(True)

        self.currentX = 0
        self.lastItem = None
        self.pairedItem = None

        self.btnNk = LeftRightPushButton("Нк")
        self.btnNk.setObjectName("NK")
        self.btnNk.setMinimumSize(30, 30)
        self.btnNk.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnNk, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)
        
        self.btnV = LeftRightPushButton("V")
        self.btnV.setObjectName("V")
        self.btnV.setMinimumSize(30, 30)
        self.btnV.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnV, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)
        
        self.btnBP = LeftRightPushButton("БП")
        self.btnBP.setObjectName("BP")
        self.btnBP.setMinimumSize(30, 30)
        self.btnBP.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnBP, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)
        
        self.btnUd = LeftRightPushButton("Уд")
        self.btnUd.setObjectName("Ud")
        self.btnUd.setMinimumSize(30, 30)
        self.btnUd.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnUd, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)
        
        self.btnNkT = LeftRightPushButton("Нк-Т")
        self.btnNkT.setObjectName("NKT")
        self.btnNkT.setMinimumSize(30, 30)
        self.btnNkT.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnNkT, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)
        
        self.btnYP = LeftRightPushButton("ЯП")
        self.btnYP.setObjectName("YP")
        self.btnYP.setMinimumSize(30, 30)
        self.btnYP.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnYP, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)
        
        self.btnPT = LeftRightPushButton("+")
        self.btnPT.setObjectName("PLUS")
        self.btnPT.setMinimumSize(30, 30)
        self.btnPT.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnPT, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)
        
        self.btnOPB = LeftRightPushButton("ОПБ")
        self.btnOPB.setObjectName("OPB")
        self.btnOPB.setMinimumSize(30, 30)
        self.btnOPB.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnOPB, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)
        
        self.btnNPB = LeftRightPushButton("НПБ")
        self.btnNPB.setObjectName("NPB")
        self.btnNPB.setMinimumSize(30, 30)
        self.btnNPB.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnNPB, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)
        
        self.btnNkd = LeftRightPushButton("Нкд")
        self.btnNkd.setObjectName("Nkd")
        self.btnNkd.setMinimumSize(30, 30)
        self.btnNkd.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnNkd, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)
        
        self.btnTNk = LeftRightPushButton("ТНк")
        self.btnTNk.setObjectName("TNK")
        self.btnTNk.setMinimumSize(30, 30)
        self.btnTNk.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnTNk, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)
        
        self.btnAr = LeftRightPushButton("Ар")
        self.btnAr.setObjectName("AR")
        self.btnAr.setMinimumSize(30, 30)
        self.btnAr.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnAr, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)
        
        self.btnPs = LeftRightPushButton("Пс")
        self.btnPs.setObjectName("PS")
        self.btnPs.setMinimumSize(30, 30)
        self.btnPs.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnPs, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)
        
        self.btnBack = LeftRightPushButton("<-")
        self.btnNk.setObjectName("NK")
        self.btnBack.setMinimumSize(40, 40)
        self.btnBack.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnBack, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Back)
        
        self.btn2 = LeftRightPushButton("2")
        self.btn2.setObjectName("TWO")
        self.btn2.setMinimumSize(40, 40)
        self.btn2.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btn2, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)
        
        self.btn1 = LeftRightPushButton("1")
        self.btn1.setObjectName("btn1")
        self.btn1.setMinimumSize(40, 40)
        self.btn1.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btn1, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)
        
        self.btnA = LeftRightPushButton("A")
        self.btnA.setObjectName("A")
        self.btnA.setMinimumSize(40, 40)
        self.btnA.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnA, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)
        
        self.btn2P = LeftRightPushButton()
        self.btn2P.setObjectName("2P")
        self.btn2P.setIcon(QtGui.QIcon('A2.png'))
        self.btn2P.setMinimumSize(40, 40)
        self.btn2P.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btn2P, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)
        
        self.btn1P = LeftRightPushButton()
        self.btn1P.setObjectName("1P")
        self.btn1P.setIcon(QtGui.QIcon('A1.png'))
        self.btn1P.setMinimumSize(40, 40)
        self.btn1P.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btn1P, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)
        
        self.btnAP = LeftRightPushButton()
        self.btnAP.setObjectName("AP")
        self.btnAP.setIcon(QtGui.QIcon('AA.png'))
        self.btnAP.setMinimumSize(40, 40)
        self.btnAP.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnAP, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)
        
        self.btnZv = LeftRightPushButton("Зв")
        self.btnZv.setObjectName("ZV")
        self.btnZv.setMinimumSize(40, 40)
        self.btnZv.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnZv, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)
        
        self.btnVyh = LeftRightPushButton("В")
        self.btnVyh.setObjectName("VYH")
        self.btnVyh.setMinimumSize(40, 40)
        self.btnVyh.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnVyh, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)

        self.btnZp = LeftRightPushButton("Зп")
        self.btnZp.setObjectName("ZP")
        self.btnZp.setMinimumSize(40, 40)
        self.btnZp.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnZp, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)
        
        self.btnP1 = LeftRightPushButton("П1")
        self.btnP1.setObjectName("P1")
        self.btnP1.setMinimumSize(40, 40)
        self.btnP1.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnP1, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)
        
        self.btnP2 = LeftRightPushButton("П2")
        self.btnP2.setObjectName("P2")
        self.btnP2.setMinimumSize(40, 40)
        self.btnP2.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnP2, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)

        self.btnNy = LeftRightPushButton("н/я")
        self.btnNy.setObjectName("NY")
        self.btnNy.setMinimumSize(30, 30)
        self.btnNy.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnNy, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)

        self.btnDoc = LeftRightPushButton("сн.вр")
        self.btnDoc.setObjectName("DOCT")
        self.btnDoc.setMinimumSize(30, 30)
        self.btnDoc.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnDoc, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)

        self.btnVin = LeftRightPushButton("VIN")
        self.btnVin.setObjectName("VIN")
        self.btnVin.setMinimumSize(30, 30)
        self.btnVin.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnVin, QtCore.SIGNAL("left_right_clicked(bool, QString)"), self.Rate)
                
        #self.sportsmenRed = QtGui.QGrapicsView()
        #self.sportsmenRed.setStyleSheet("color:red; font-size: 14px; border-style:solid; border-right:none; border-width:1px; border-color:black")
        #self.sportsmenBlue = QtGui.QLabel("Петров Петр\nБрянск")
        #self.sportsmenBlue.setStyleSheet("color:blue; font-size: 14px; border-style:solid; border-top:none; border-right:none; border-width:1px; border-color:black")

        self.BallsRed = QtGui.QLabel("0")
        self.BallsRed.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.BallsRed.setStyleSheet("color:black; font-size: 20px; border-style:solid; border-left:none;"
                                    "border-width:1px; border-color:black")
        self.BallsBlue = QtGui.QLabel("0")
        self.BallsBlue.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.BallsBlue.setStyleSheet("color:black; font-size: 20px;border-style:solid; border-top:none;"
                                     "border-left:none; border-width:1px; border-color:black")

        self.AktRed = QtGui.QLabel("0")
        self.AktRed.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.AktRed.setStyleSheet("color:black; font-size: 16px; border-style:solid; border-top:none;"
                                  "border-left:none; border-width:1px; border-color:black")
        self.AktBlue = QtGui.QLabel("0")
        self.AktBlue.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.AktBlue.setStyleSheet("color:black; font-size: 16px; border-style:solid; border-top:none;"
                                   "border-left:none; border-width:1px; border-color:black")

        self.ResultRed = QtGui.QLabel("")
        self.ResultRed.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.ResultRed.setStyleSheet("color:black; font-size: 20px; border-style:solid;"
                                   "border-left:none; border-width:1px; border-color:black")
        self.ResultBlue = QtGui.QLabel("")
        self.ResultBlue.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.ResultBlue.setStyleSheet("color:black; font-size: 20px; border-style:solid; border-top:none;"
                                   "border-left:none; border-width:1px; border-color:black")

        lblRef  = QtGui.QLabel("Судьи")
        lblRef.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        lblRef.setStyleSheet("border-style:solid; border-left:none;"
                                   "border-bottom:none; border-width:1px; border-color:black")
        
        self.nameMain = QtGui.QLabel("рук. ковра")
        self.nameMain.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.nameMain.setStyleSheet("border-style:solid; border-left:none; border-top: none;"
                                   "border-bottom:none; border-width:1px; border-color:black")

        self.nameRef = QtGui.QLabel("рефери")
        self.nameRef.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.nameRef.setStyleSheet("border-style:solid; border-left:none; border-top: none;"
                                   "border-bottom:none; border-width:1px; border-color:black")

        self.nameSide = QtGui.QLabel("боковой")
        self.nameSide.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.nameSide.setStyleSheet("border-style:solid; border-left:none; border-top: none;"
                                   "border-bottom:none; border-width:1px; border-color:black")
        
        lblTime = QtGui.QLabel("Время")
        lblTime.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        lblTime.setStyleSheet("border-style:solid; border-left:none;"
                                   "border-bottom:none; border-width:1px; border-color:black")
        self.time = QtGui.QLabel("0:00")
        self.time.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.time.setStyleSheet("border-style:solid; border-left:none;"
                                   "border-top:none; border-width:1px; border-color:black; font-size: 20px;")

        self.itemNameRed = rates.Name()
        self.itemNameRed.setName("")
        self.sceneNameRed = QtGui.QGraphicsScene()
        self.sportsmenRed = QtGui.QGraphicsView(self.sceneNameRed)
        self.sportsmenRed.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sportsmenRed.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sceneNameRed.addItem(self.itemNameRed)

        self.itemNameBlue = rates.Name()
        self.itemNameBlue.setName("")
        self.sceneNameBlue = QtGui.QGraphicsScene()
        self.sportsmenBlue = QtGui.QGraphicsView(self.sceneNameBlue)
        self.sportsmenBlue.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sportsmenBlue.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sceneNameBlue.addItem(self.itemNameBlue)
        
        self.sceneBlue = QtGui.QGraphicsScene()
        self.sceneRed = QtGui.QGraphicsScene() #MyQGraphicsScene()
        
        self.rateRed = MyGraphicsView()
        self.rateRed.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.rateRed.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.rateRed.setMinimumHeight(20)
        self.rateRed.setStyleSheet("border-style:solid; border-width:1px; border-color:black")
        self.rateRed.setScene(self.sceneRed)
        
        
        self.rateBlue = MyGraphicsView()
        self.rateBlue.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.rateBlue.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.rateBlue.setMinimumHeight(20)
        self.rateBlue.setStyleSheet("border-style:solid; border-top:none; border-width:1px; border-color:black;")
        self.rateBlue.setScene(self.sceneBlue)
        

        self.margin = 6
        
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(0)
        self.grid.setMargin(self.margin)

        self.grid.addWidget(self.btnNk,         0,  0, 3, 3)
        self.grid.addWidget(self.btnV,          0,  3, 3, 3)      
        self.grid.addWidget(self.btnBP,         0,  6, 3, 3)
        self.grid.addWidget(self.btnUd,         0,  9, 3, 3)
        self.grid.addWidget(self.btnNkT,        0, 12, 3, 3)
        self.grid.addWidget(self.btnYP,         0, 15, 3, 3)      
        self.grid.addWidget(self.btnPT,         0, 18, 3, 3)
        self.grid.addWidget(self.btnDoc,        0, 21, 3, 3)
        
        self.grid.addWidget(self.btnOPB,        3,  0, 3, 3)
        self.grid.addWidget(self.btnNPB,        3,  3, 3, 3)
        self.grid.addWidget(self.btnNkd,        3,  6, 3, 3)      
        self.grid.addWidget(self.btnTNk,        3,  9, 3, 3)
        self.grid.addWidget(self.btnAr,         3, 12, 3, 3)
        self.grid.addWidget(self.btnPs,         3, 15, 3, 3)
        self.grid.addWidget(self.btnNy,         3, 18, 3, 3)
        self.grid.addWidget(self.btnVin,        3, 21, 3, 3)
        
        self.grid.addWidget(self.btn2,          1, 24, 4, 4)
        self.grid.addWidget(self.btn1,          1, 28, 4, 4)
        self.grid.addWidget(self.btnA,          1, 32, 4, 4)
        self.grid.addWidget(self.btn2P,         1, 36, 4, 4)      
        self.grid.addWidget(self.btn1P,         1, 40, 4, 4)
        self.grid.addWidget(self.btnAP,         1, 44, 4, 4)
        self.grid.addWidget(self.btnZv,         1, 48, 4, 4)
        self.grid.addWidget(self.btnVyh,        1, 52, 4, 4)      
        self.grid.addWidget(self.btnZp,         1, 56, 4, 4)
        self.grid.addWidget(self.btnP1,         1, 60, 4, 4)
        self.grid.addWidget(self.btnP2,         1, 64, 4, 4)
        self.grid.addWidget(self.btnBack,       1, 68, 4, 4) 
        self.grid.addWidget(self.sportsmenRed,  6, 0, 4, 10)
        self.grid.addWidget(self.sportsmenBlue, 10, 0, 4, 10)
        self.grid.addWidget(self.rateRed,       6, 10, 4, 45)
        self.grid.addWidget(self.rateBlue,      10, 10, 4, 45)
        self.grid.addWidget(self.BallsRed,      6,  55, 2, 5)
        self.grid.addWidget(self.AktRed,        8,  55, 2, 5)
        self.grid.addWidget(self.BallsBlue,     10, 55, 2, 5)
        self.grid.addWidget(self.AktBlue,       12, 55, 2, 5)
        self.grid.addWidget(self.ResultRed,     6,  60, 4, 5)
        self.grid.addWidget(self.ResultBlue,    10, 60, 4, 5)

        self.grid.addWidget(lblRef,              6, 65, 1, 7)
        self.grid.addWidget(self.nameMain,       7, 65, 1, 7)
        self.grid.addWidget(self.nameRef,        8, 65, 1, 7)
        self.grid.addWidget(self.nameSide,       9, 65, 1, 7)
        self.grid.addWidget(lblTime,            10, 65, 1, 7)
        self.grid.addWidget(self.time,          11, 65, 3, 7)
        
        self.setLayout(self.grid)
        
        self.font = QtGui.QFont()
        self.connect(self.rateRed, QtCore.SIGNAL("shift(int, int)"), self.shiftBlue)
        self.connect(self.rateBlue, QtCore.SIGNAL("shift(int, int)"), self.shiftRed)
        
        self.connect(self.rateRed, QtCore.SIGNAL("strike(int, int)"), self.strikeBlue)
        self.connect(self.rateBlue, QtCore.SIGNAL("strike(int, int)"), self.strikeRed)

        self.num_fight = None

    def setMat(self, mat):
        self.mat = int(mat) * 1111

    def setAddr(self, addr):
        self.address = addr

    def rate_to_png(self):
        if self.num_fight == None:
            return
        pix = QtGui.QPixmap(self.sportsmenRed.width() + self.rateRed.width()
                                                      + self.BallsRed.width()
                                                      + self.ResultRed.width()
                                                      + self.time.width(),
                            self.rateRed.height() * 2)
        self.render(pix, targetOffset=QtCore.QPoint(-self.sportsmenRed.pos().x(), -self.sportsmenRed.pos().y()))

        ba = QtCore.QByteArray()
        buff = QtCore.QBuffer(ba)
        buff.open(QtCore.QIODevice.WriteOnly) 
        ok = pix.save(buff, "PNG")
        pix_bytes = ba.data()
        ba.prepend(int(self.num_fight).to_bytes(1, byteorder='big'))
        pixmap_bytes = ba.data()

        con = sqlite3.connect('baza_out.db')
        cur = con.cursor()
        sql = "UPDATE rounds SET result = ? WHERE fight = " + self.num_fight
        try:
            cur.execute(sql, (pix_bytes,))
            con.commit()
        except sqlite3.DatabaseError as err:
            print("error ", err)
        finally:
            cur.close()
            con.close()
             
        thread = QtCore.QThread()
        client = TcpClient(pixmap_bytes, (self.address, self.mat))
        client.moveToThread(thread)
        self.connect(thread, QtCore.SIGNAL("started()"), client.run)
        thread.start()
        thread.quit()
        thread.wait()
        
    def calculation(self):
        clearVin = False    #флаг чистой победы
        red_p2 = False      #флаг второго нарушения правил
        blue_p2 = False
        red_p1 = False
        blue_p1 = False
        red_zp = False
        blue_zp = False
        red_zv = False
        blue_zv = False
        red_v = False
        blue_v = False
        red_plus = False
        blue_plus = False

        finish = False      #флаг окончания боя
        
        self.itemNameRed.setStatus(0)
        self.itemNameBlue.setStatus(0)
        l = self.sceneRed.items()
        redBall = 0
        redAct = 0
        
        for each in l:
            val = each.getValue()
            if val == 1 or val == 2:
                if each.strikethrough == False:
                    redBall += val
            elif val == "A":
                if each.strikethrough == False:
                    redAct += 1
            elif val == "V" and each.strikethrough == False:
                self.itemNameRed.setStatus(1)
                self.itemNameBlue.setStatus(2)
                self.ResultRed.setText("5")
                self.ResultBlue.setText("0")
                clearVin = True
            elif val == "П2" and each.strikethrough == False:
                red_p2 = True
            elif val == "П1" and each.strikethrough == False:
                red_p1 = True
            elif val == "ЗП" and each.strikethrough == False:
                red_zp = True
            elif val == "В" and each.strikethrough == False:
                red_v = True
            elif val == "ЗВ" and each.strikethrough == False:
                red_zv = True
            elif val == "+" and each.strikethrough == False:
                red_plus = True
            '''
            elif val == "V" and each.strikethrough == True:
                self.itemNameRed.setStatus(0)
                self.itemNameBlue.setStatus(0)
            '''

        self.BallsRed.setText(str(redBall))
        self.AktRed.setText(str(redAct))
                
        l = self.sceneBlue.items()
        blueBall = 0
        blueAct = 0
        
        for each in l:
            val = each.getValue()
            if val == 1 or val == 2:
                if each.strikethrough == False:
                    blueBall += val
            elif val == "A":
                if each.strikethrough == False:
                    blueAct += 1
            elif val == "V" and each.strikethrough == False:
                self.itemNameBlue.setStatus(1)
                self.itemNameRed.setStatus(2)
                self.ResultRed.setText("0")
                self.ResultBlue.setText("5")
                clearVin = True
            elif val == "П2" and each.strikethrough == False:
                blue_p2 = True
            elif val == "П1" and each.strikethrough == False:
                blue_p1 = True
            elif val == "ЗП" and each.strikethrough == False:
                blue_zp = True
            elif val == "В" and each.strikethrough == False:
                blue_v = True
            elif val == "ЗВ" and each.strikethrough == False:
                blue_zv = True
            elif val == "+" and each.strikethrough == False:
                blue_plus = True
            '''
            elif val == "V" and each.strikethrough == True:
                self.itemNameBlue.setStatus(0)
                self.itemNameRed.setStatus(0)
            '''
        self.BallsBlue.setText(str(blueBall))
        self.AktBlue.setText(str(blueAct))
        if clearVin == False:
            finish = True
            if self.vin == 1:
                self.itemNameBlue.setStatus(1)
                self.itemNameRed.setStatus(2)
                if redBall == blueBall:
                    self.ResultRed.setText("2")
                    self.ResultBlue.setText("3")
                else:
                    self.ResultRed.setText("1")
                    self.ResultBlue.setText("4")
            elif self.vin == 2:
                self.itemNameBlue.setStatus(2)
                self.itemNameRed.setStatus(1)
                if redBall == blueBall:
                    self.ResultRed.setText("3")
                    self.ResultBlue.setText("2")
                else:
                    self.ResultRed.setText("4")
                    self.ResultBlue.setText("1")
            else:
                self.ResultRed.setText("")
                self.ResultBlue.setText("")
                finish = False
        else:
            finish = True

        if red_p2:
            self.emit(QtCore.SIGNAL("change_prav(int, QString)"), 0, 'П2')     #первый аргумент: 0 - красный, 1 - синий
        elif red_p1:
            self.emit(QtCore.SIGNAL("change_prav(int, QString)"), 0, 'П1')
        elif red_zp:
            self.emit(QtCore.SIGNAL("change_prav(int, QString)"), 0, 'ЗП')
        else:
            self.emit(QtCore.SIGNAL("change_prav(int, QString)"), 0, '')

        if blue_p2:
            self.emit(QtCore.SIGNAL("change_prav(int, QString)"), 1, 'П2')     #первый аргумент: 0 - красный, 1 - синий
        elif blue_p1:
            self.emit(QtCore.SIGNAL("change_prav(int, QString)"), 1, 'П1')
        elif blue_zp:
            self.emit(QtCore.SIGNAL("change_prav(int, QString)"), 1, 'ЗП')
        else:
            self.emit(QtCore.SIGNAL("change_prav(int, QString)"), 1, '')

        if red_v:
            self.emit(QtCore.SIGNAL("change_vyh(int, QString)"), 0, 'В')
        elif red_zv:
            self.emit(QtCore.SIGNAL("change_vyh(int, QString)"), 0, 'ЗВ')
        else:
            self.emit(QtCore.SIGNAL("change_vyh(int, QString)"), 0, '')

        if blue_v:
            self.emit(QtCore.SIGNAL("change_vyh(int, QString)"), 1, 'В')
        elif blue_zv:
            self.emit(QtCore.SIGNAL("change_vyh(int, QString)"), 1, 'ЗВ')
        else:
            self.emit(QtCore.SIGNAL("change_vyh(int, QString)"), 1, '')

        if red_plus:
            self.emit(QtCore.SIGNAL("set_plus(int, QString)"), 0, "+")
        else:
            self.emit(QtCore.SIGNAL("set_plus(int, QString)"), 0, "")

        if blue_plus:
            self.emit(QtCore.SIGNAL("set_plus(int, QString)"), 1, "+")
        else:
            self.emit(QtCore.SIGNAL("set_plus(int, QString)"), 1, "")
            
        self.emit(QtCore.SIGNAL("change_rate(int, int, int, int)"), redBall, blueBall, redAct, blueAct)

        return finish
        

    def strikeBlue(self, x, y):
        item = self.rateBlue.scene().itemAt(x, y)
        if item == None:
            self.calculation()
            return
        item.strikethrough = True
        penWidth = 1
        item.update(QtCore.QRectF(-item.w / 2 - penWidth / 2, -item.h / 2 - penWidth / 2, item.w + penWidth, item.h + penWidth))
        self.calculation()

    def strikeRed(self, x, y):
        item = self.rateRed.scene().itemAt(x, y)
        if item == None:
            self.calculation()
            return
        item.strikethrough = True
        penWidth = 1
        item.update(QtCore.QRectF(-item.w / 2 - penWidth / 2, -item.h / 2 - penWidth / 2, item.w + penWidth, item.h + penWidth))
        self.calculation()
        #self.itemNameRed.update()
        
    def shiftBlue(self, shift, x):    
        l = self.rateBlue.items(x, 0, self.rateBlue.scene().width() - x, self.rateBlue.scene().height(), 1)
        for each in l:
            each.setPos(each.pos().x() + shift, each.pos().y())

    def shiftRed(self, shift, x):
        l = self.rateRed.items(x, 0, self.rateRed.scene().width() - x, self.rateRed.scene().height(), 1)
        for each in l:
            each.setPos(each.pos().x() + shift, each.pos().y())

    def Back(self):
        global currentX
        if self.lastItem != None:
            scene = self.lastItem.scene()
            currentX -= self.lastItem.w / 1
            scene.removeItem(self.lastItem)
            self.lastItem = None
            if self.pairedItem != None:
                scene = self.pairedItem.scene()
                scene.removeItem(self.pairedItem)
                self.pairedItem = None
            self.calculation()

    def Rate(self, button, name):
        if self.num_fight == None:
            return
        self.pairedItem = None
        global currentX
        if name == "btn1":
            item = rates.Rate("1", False, False, 1)
            item.setSize(self.rateRed.height()/5.8, self.rateRed.height()/3)
        elif name == "A":
            item = rates.Rate("A", False, False, "A")
            item.setSize(self.rateRed.height()/3.4, self.rateRed.height()/3)
        elif name == "NK":
            item = rates.Rate("V", False, False, "V")
            item.setSize(self.rateRed.height()/3.4, self.rateRed.height()/3)
            self.pairedItem = rates.Rate("Нк", False, True)
            self.pairedItem.setSize(self.rateRed.height()/2.4, self.rateRed.height()/3)
            self.pairedItem.setPos(currentX + item.w / 2, self.rateRed.height()/2)
        elif name == "NY":
            item = rates.Rate("н/я")
            item.setSize(self.rateRed.height()/2.1, self.rateRed.height()/3)
        elif name == "V":
            item = rates.Rate("V", False, False, "V")
            item.setSize(self.rateRed.height()/3.4, self.rateRed.height()/3)
        elif name == "BP":
            item = rates.Rate("V", False, False, "V")
            item.setSize(self.rateRed.height()/3.4, self.rateRed.height()/3)
            self.pairedItem = rates.Rate("БП", False, True)
            self.pairedItem.setSize(self.rateRed.height()/2.1, self.rateRed.height()/3)
            self.pairedItem.setPos(currentX + item.w / 2, self.rateRed.height()/2)
        elif name == "Ud":
            item = rates.Rate("V", False, False, "V")
            item.setSize(self.rateRed.height()/3.4, self.rateRed.height()/3)
            self.pairedItem = rates.Rate("Уд", False, True)
            self.pairedItem.setSize(self.rateRed.height()/2.3, self.rateRed.height()/3)
            self.pairedItem.setPos(currentX + item.w / 2, self.rateRed.height()/2)
        elif name == "NKT":
            item = rates.Rate("V", False, False, "V")
            item.setSize(self.rateRed.height()/3.4, self.rateRed.height()/3)
            self.pairedItem = rates.Rate("Нк-Т", False, True)
            self.pairedItem.setSize(self.rateRed.height()/1.35, self.rateRed.height()/3)
            self.pairedItem.setPos(currentX + item.w / 2, self.rateRed.height()/2)
        elif name == "DOCT":
            item = rates.Rate("сн.вр")
            item.setSize(self.rateRed.height()/1.28, self.rateRed.height()/3)
            #self.pairedItem = rates.Rate("V", False, True, "V")
            #self.pairedItem.setSize(self.rateRed.height()/3.4, self.rateRed.height()/3)
            #self.pairedItem.setPos(currentX + item.w / 2, self.rateRed.height()/2)
        elif name == "YP":
            item = rates.Rate("V", False, False, "V")
            item.setSize(self.rateRed.height()/3.4, self.rateRed.height()/3)
            self.pairedItem = rates.Rate("ЯП", False, True)
            self.pairedItem.setSize(self.rateRed.height()/2.1, self.rateRed.height()/3)
            self.pairedItem.setPos(currentX + item.w / 2, self.rateRed.height()/2)
        elif name == "PLUS":
            item = rates.Rate("+", False, False, "+")
            item.setSize(self.rateRed.height()/4.0, self.rateRed.height()/3)
        elif name == "OPB":
            item = rates.Rate("ОПБ")
            item.setSize(self.rateRed.height()/1.4, self.rateRed.height()/3)
        elif name == "NPB":
            item = rates.Rate("НПБ")
            item.setSize(self.rateRed.height()/1.4, self.rateRed.height()/3)
        elif name == "Nkd":
            item = rates.Rate("Нкд")
            item.setSize(self.rateRed.height()/1.7, self.rateRed.height()/3)
            self.pairedItem = rates.Rate("2", False, True, 2)
            self.pairedItem.setSize(self.rateRed.height()/4.9, self.rateRed.height()/3)
            self.pairedItem.setPos(currentX + item.w / 2, self.rateRed.height()/2)
        elif name == "TNK":
            item = rates.Rate("V", False, False, "V")
            item.setSize(self.rateRed.height()/3.4, self.rateRed.height()/3)
            self.pairedItem = rates.Rate("ТНк", False, True)
            self.pairedItem.setSize(self.rateRed.height()/1.6, self.rateRed.height()/3)
            self.pairedItem.setPos(currentX + item.w / 2, self.rateRed.height()/2)
        elif name == "AR":
            item = rates.Rate("Ар", False, False, "A")
            item.setSize(self.rateRed.height()/2.3, self.rateRed.height()/3)
        elif name == "PS":
            item = rates.Rate("Пс")
            item.setSize(self.rateRed.height()/2.3, self.rateRed.height()/3)
        elif name == "TWO":
            item = rates.Rate("2", False, False, 2)
            item.setSize(self.rateRed.height()/4.9, self.rateRed.height()/3)
        elif name == "2P":
            item = rates.Rate("2", True, False, 2)
            item.setSize(self.rateRed.height()/3.0, self.rateRed.height()/3)
        elif name == "1P":
            item = rates.Rate("1", True, False, 1)
            item.setSize(self.rateRed.height()/3, self.rateRed.height()/3)
        elif name == "AP":
            item = rates.Rate("A", True, False, "A")
            item.setSize(self.rateRed.height()/3, self.rateRed.height()/3)
        elif name == "ZV":
            item = rates.Rate("Зв", False, False, "ЗВ")
            item.setSize(self.rateRed.height()/2.3, self.rateRed.height()/3)
        elif name == "VYH":
            self.pairedItem = rates.Rate("1", False, True, 1)
            item = rates.Rate("В", False, False, "В")
            item.setSize(self.rateRed.height()/3.0, self.rateRed.height()/3)
            self.pairedItem.setSize(self.rateRed.height()/5.8, self.rateRed.height()/3)
            self.pairedItem.setPos(currentX + item.w / 2, self.rateRed.height()/2)
        elif name == "ZP":
            item = rates.Rate("Зп", False, False, "ЗП")
            item.setSize(self.rateRed.height()/2.3, self.rateRed.height()/3)
        elif name == "P1":
            self.pairedItem = rates.Rate("1", False, True, 1)
            item = rates.Rate("П1", False, False, "П1")
            item.setSize(self.rateRed.height()/2.4, self.rateRed.height()/3)
            self.pairedItem.setSize(self.rateRed.height()/5.8, self.rateRed.height()/3)
            self.pairedItem.setPos(currentX + item.w / 2, self.rateRed.height()/2)
        elif name == "P2":
            self.pairedItem = rates.Rate("2", False, True, 2)
            item = rates.Rate("П2", False, False, "П2")
            item.setSize(self.rateRed.height()/2.3, self.rateRed.height()/3)         
            self.pairedItem.setSize(self.rateRed.height()/4.9, self.rateRed.height()/3)
            self.pairedItem.setPos(currentX + item.w / 2, self.rateRed.height()/2)
        elif name == "VIN":
            if button:
                if self.vin == 1:
                    self.vin = 0
                else:
                    self.vin = 1
            else:
                if self.vin == 2:
                    self.vin = 0
                else:
                    self.vin = 2
            self.calculation()
            self.rate_to_png()
            return

        item.setPos(currentX + item.w / 2, self.rateRed.height()/2)
        currentX += item.w
        self.lastItem = item

        if button:
            self.sceneBlue.addItem(item)
            if self.pairedItem != None:
                self.sceneRed.addItem(self.pairedItem)
        else:
            self.sceneRed.addItem(item)
            if self.pairedItem != None:
                self.sceneBlue.addItem(self.pairedItem)

        if self.calculation():
            self.rate_to_png()

    def resetRate(self):
        global currentX
        currentX = 0
        items = self.sceneBlue.items()
        for item in items:
            self.sceneBlue.removeItem(item)
        items = self.sceneRed.items()
        for item in items:
            self.sceneRed.removeItem(item)
        self.vin = 0
        self.calculation()
        self.rate_to_png()
            
    def resizeEvent(self, e):
        self.sceneRed.setSceneRect(0, 0, self.rateRed.width(), self.rateRed.height())
        self.sceneBlue.setSceneRect(0, 0, self.rateRed.width(), self.rateRed.height())
        
        self.itemNameRed.setSize(self.sportsmenRed.width(), self.sportsmenRed.height())
        self.sceneNameRed.setSceneRect(0, 0, self.sportsmenRed.width(), self.sportsmenRed.height())
        self.itemNameRed.setPos(self.itemNameRed.w / 2, self.itemNameRed.h / 2)

        self.itemNameBlue.setSize(self.sportsmenBlue.width(), self.sportsmenBlue.height())
        self.sceneNameBlue.setSceneRect(0, 0, self.sportsmenBlue.width(), self.sportsmenBlue.height())
        self.itemNameBlue.setPos(self.itemNameBlue.w / 2, self.itemNameBlue.h / 2)
        #self.sceneBlue.setSceneRect(0, 0, self.rateRed.width(), self.rateRed.height())

    def showQueue(self):
        self.q = queuefight.FightQueue()
        #self.q.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.connect(self.q, QtCore.SIGNAL("select_fight(QString)"), self.selectFight)
        self.connect(self.q, QtCore.SIGNAL("show_fight(QString)"), self.showFight)
        res = self.q.exec_()
        #self.q.show()
        del self.q
        #self.resetRate()
    '''
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_F:
            self.q = queuefight.FightQueue()
            self.q.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.connect(self.q, QtCore.SIGNAL("select_fight(QString)"), self.selectFight)
            self.connect(self.q, QtCore.SIGNAL("show_fight(QString)"), self.showFight)
            res = self.q.exec_()
            del self.q
            self.resetRate()
    '''
    def showFight(self, s):
        #obj = self.q.findChild(queuefight.Fight, s)

        con = sqlite3.connect('baza_out.db')
        cur = con.cursor()
        sql = "SELECT result FROM rounds WHERE fight = " + s

        try:
            cur.execute(sql)
            data = cur.fetchall()
        except sqlite3.DatabaseError as err:
            print("error ", err)
        #print(data)
        pix = QtGui.QPixmap()
        pix.loadFromData(data[0][0], "PNG")
        #self.lblFight.setPixmap(pix.scaled(self.lblFight.width(), self.lblFight.height()))
        #self.lblFight.setVisible(True)
        
        #print(pix.size())

        view = queuefight.viewFight(pix, self.q)
        view.show()

    def pastTime(self, t):
        self.time.setText(t)

    def selectFight(self, s):
        obj = self.q.findChild(queuefight.Fight, s)
        dialog = QtGui.QMessageBox(QtGui.QMessageBox.Question, "Выбор спортсменов", obj.red + "\n" + obj.blue,
                                    buttons=QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel, parent=self)
        #dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        #geom = self.geometry()
        #dialog.move(geom.x() + geom.width(), geom.y())
        #print(geom, dialog.geometry())
        #dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        result = dialog.exec_()
        if result == QtGui.QMessageBox.Ok:
            self.itemNameRed.setName(obj.red)
            r = obj.red.split("\n")
            if len(r) > 1:
                self.emit(QtCore.SIGNAL("nameRed(QString)"), r[0].split(" ")[0])
                self.emit(QtCore.SIGNAL("regRed(QString)"),  r[1].split("(")[0])
            self.itemNameBlue.setName(obj.blue)
            b = obj.blue.split("\n")
            if len(b) > 1:
                self.emit(QtCore.SIGNAL("nameBlue(QString)"), b[0].split(" ")[0])
                self.emit(QtCore.SIGNAL("regBlue(QString)"),  b[1].split("(")[0])
            pix = QtGui.QPixmap(self.sportsmenRed.width() + self.rateRed.width() + self.BallsRed.width() + self.ResultRed.width(),
                            self.sportsmenRed.height() * 2)
            self.render(pix, targetOffset=QtCore.QPoint(-self.sportsmenRed.pos().x(), -self.sportsmenRed.pos().y()))
            obj.lblFight.setPixmap(pix.scaled(obj.lblFight.width(), obj.lblFight.height()))
            obj.lblFight.setVisible(True)

            ba = QtCore.QByteArray()
            buff = QtCore.QBuffer(ba)
            buff.open(QtCore.QIODevice.WriteOnly) 
            ok = pix.save(buff, "PNG")
            pixmap_bytes = ba.data()

            self.num_fight = obj.objectName()
            
            con = sqlite3.connect('baza_out.db')
            cur = con.cursor()
            sql = "INSERT INTO rounds (fight, result) VALUES (?, ?)"
            try:
                cur.execute(sql, (obj.objectName(), pixmap_bytes))
                con.commit()
            except sqlite3.DatabaseError as err:
                print("error ", err)
            finally:
                cur.close()
                con.close()

            con = sqlite3.connect('baza_in.db')
            cur = con.cursor()
            sql = "SELECT * FROM referees WHERE id_fight = " + self.num_fight
            try:
                cur.execute(sql)
                ref = cur.fetchall()
                if ref != []:
                    self.nameMain.setText(ref[0][2])
                    self.nameRef.setText(ref[0][3])
                    self.nameSide.setText(ref[0][4])
            except sqlite3.DatabaseError as err:
                print("error ", err)
            finally:
                cur.close()
                con.close()
            self.resetRate()
            self.emit(QtCore.SIGNAL("setWeight(QString)"),  obj.title.split(",")[2])

    def paintEvent(self,e):
        pn = QtGui.QPainter(self)
        pn.begin(self)
        pn.setPen(QtCore.Qt.black)
        pn.end()

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    secr = Secretary()
    #secr.resize(1000, 240)
    secr.show()
    sys.exit(app.exec_())
