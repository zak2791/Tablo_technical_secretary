from PyQt4 import QtCore, QtGui
import sqlite3

class viewFight(QtGui.QSplashScreen):
    def __init__(self, pix, parent=None):
        QtGui.QSplashScreen.__init__(self, parent)
        self.setGeometry(50, 50, pix.width(), pix.height())
        self.setPixmap(pix)
        self.pix = pix
        

    def mousePressEvent(self, e):
        self.deleteLater()

class Fight(QtGui.QLabel):
    def __init__(self, r, b, nr, nb, t, nf, parent=None):
        QtGui.QLabel.__init__(self, parent)
        red = r.split(":")
        if len(red) == 2:
            self.red = red[1] + " (" + red[0] + ")"
        else:
            self.red = r
        blue = b.split(":")
        if len(blue) == 2:
            self.blue = blue[1] + " (" + blue[0] + ")"
        else:
            self.blue = b
        self.note_red = nr
        self.note_blue = nb
        self.num_fight = nf
        self.title = t
        self.setGeometry(0, 0, 560, 100)

        lblRef = QtGui.QLabel("Судьи", self)
        lblRef.setGeometry(400, 20, 160, 20)
        lblRef.setAlignment(QtCore.Qt.AlignHCenter)

        self.lblFight = QtGui.QLabel(self)
        self.lblFight.setGeometry(0, 20, 560, 80)
        self.lblFight.setVisible(False)
        
        #судьи
        self.cmbMain = None
        self.refMain = ""
        
        self.cmbRef = None
        self.refRef = ""
        
        self.cmbSaid = None
        self.refSaid = ""
        
        self.setFrameStyle(1)
        
        referees = QtCore.QFile("referees.txt")
        if not referees.exists():
            referees.open(QtCore.QFile.WriteOnly)
            referees.close()

        self.show()

    def setCombo(self):
        referees = QtCore.QFile("referees.txt")
        ref = [""]

        f = QtCore.QFile("referees.txt")
        f.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text)
        inf = QtCore.QTextStream(f)
        inf.setCodec("utf-8")
        while not inf.atEnd():
            line = inf.readLine()
            ref.append(line)
        f.close()

        con = sqlite3.connect('baza_in.db')
        cur = con.cursor()
        sql = "SELECT * FROM referees WHERE id_fight = " + self.num_fight
        try:
            cur.execute(sql)
            data = cur.fetchall()
        except sqlite3.DatabaseError as err:
            print("error ", err)
        finally:
            cur.close()
            con.close()
        
        self.cmbMain = QtGui.QComboBox(self)
        self.cmbMain.setGeometry(401, 40, 159, 20)
        self.cmbMain.addItems(ref)
        self.cmbMain.setObjectName("main")
        self.connect(self.cmbMain, QtCore.SIGNAL("activated(const QString&)"), self.selectRef)
        self.cmbRef = QtGui.QComboBox(self)
        self.cmbRef.setGeometry(401, 60, 159, 20)
        self.cmbRef.addItems(ref)
        self.cmbRef.setObjectName("ref")
        self.connect(self.cmbRef, QtCore.SIGNAL("activated(const QString&)"), self.selectRef)
        self.cmbSaid = QtGui.QComboBox(self)
        self.cmbSaid.setGeometry(401, 80, 159, 20)
        self.cmbSaid.addItems(ref)
        self.cmbSaid.setObjectName("said")
        self.connect(self.cmbSaid, QtCore.SIGNAL("activated(const QString&)"), self.selectRef)

        if data != []:
            self.refMain = data[0][2]
            index = self.cmbMain.findText(self.refMain)
            self.cmbMain.setCurrentIndex(index)
            self.refRef  = data[0][3]
            index = self.cmbRef.findText(self.refRef)
            self.cmbRef.setCurrentIndex(index)
            self.refSaid = data[0][4]
            index = self.cmbSaid.findText(self.refSaid)
            self.cmbSaid.setCurrentIndex(index)

    def selectRef(self, s):
        if self.sender().objectName() == "main":
            self.refMain = s
        elif self.sender().objectName() == "ref":
            self.refRef = s
        else:
            self.refSaid = s

        con = sqlite3.connect('baza_in.db')
        cur = con.cursor()

        try:
            cur.execute("SELECT * FROM referees WHERE id_fight = " + self.num_fight)
            info = cur.fetchone()
            if info is None:
                sql = "INSERT INTO referees (id_fight, ref1, ref2, ref3) VALUES (?, ?, ?, ?)"
                cur.execute(sql, (self.num_fight, self.refMain, self.refRef, self.refSaid))
                con.commit()
            else:
                sql = "UPDATE referees SET ref1 = ?, ref2 = ?, ref3 = ? WHERE id_fight = ?"
                cur.execute(sql, (self.refMain, self.refRef, self.refSaid, self.num_fight))
                con.commit()
        except sqlite3.DatabaseError as err:
            print("error ", err)
        finally:
            cur.close()
            con.close()
        
    def setPix(self, data):
        pix = QtGui.QPixmap()
        pix.loadFromData(data, "PNG")
        self.lblFight.setPixmap(pix.scaled(self.lblFight.width(), self.lblFight.height()))
        self.lblFight.setVisible(True)
       
    def mousePressEvent(self, e):
        if self.lblFight.isVisible():
            self.emit(QtCore.SIGNAL("show_fight(QString)"), self.objectName())
        else:
            self.emit(QtCore.SIGNAL("select_fight(QString)"), self.objectName())
            
    
    def paintEvent(self, e):
        p = QtGui.QPainter(self)
        
        p.drawLine(0, 0, 560, 0)
        p.drawLine(0, 20, 560, 20)
        p.drawLine(0, 60, 400, 60)
        p.drawLine(0, 99, 560, 99)

        p.drawLine(40, 0, 40, 20)
        p.drawLine(200, 20, 200, 100)
        p.drawLine(400, 20, 400, 100)
        #p.drawLine(0, 99, 560, 99)
        
        p.drawText(0, 20, 200, 40, QtCore.Qt.AlignCenter, self.red)
        p.drawText(0, 60, 200, 40, QtCore.Qt.AlignCenter, self.blue)
        p.drawText(200, 20, 200, 40, QtCore.Qt.AlignCenter, self.note_red)
        p.drawText(200, 60, 200, 40, QtCore.Qt.AlignCenter, self.note_blue)
        p.drawText(0, 0, 40, 20, QtCore.Qt.AlignCenter, str(self.num_fight))
        p.drawText(40, 0, 520, 20, QtCore.Qt.AlignCenter, self.title)
    
class FightQueue(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setGeometry(10, 50, 600, 600)

        scroll = QtGui.QScrollArea(self)
        scroll.setGeometry(10, 10, 580, 580)
        scroll.setVerticalScrollBarPolicy(2)

        self.fight_window = QtGui.QWidget()
        self.fight_window.setGeometry(0, 0, 560, 0)
        
        #scroll.setWidget(fight_window)
        
        con = sqlite3.connect('baza_in.db')
        cur = con.cursor()
        sql = "SELECT * FROM rounds"
        try:
            cur.execute(sql)
            data = cur.fetchall()
        except sqlite3.DatabaseError as err:
            print("error ", err)
        finally:
            cur.close()
            con.close()
        #print(data)
        currentY = 0
        
        con = sqlite3.connect('baza_out.db')
        cur = con.cursor()
        sql = "SELECT * FROM rounds WHERE fight = "
        
        
        for each in data:
            f = Fight(each[3], each[4], each[5], each[6], each[2], str(each[7]), self.fight_window)
            f.move(0, currentY)
            f.setObjectName(str(each[7]))
            try:
                cur.execute(sql + str(each[7]))
                data_out = cur.fetchall()
            except sqlite3.DatabaseError as err:
                print("error ", err)

            if data_out != []:
                f.setPix(data_out[0][2])
            else:
                f.setCombo()
            
            self.connect(f, QtCore.SIGNAL("select_fight(QString)"), self.selectFight)
            self.connect(f, QtCore.SIGNAL("show_fight(QString)"), self.showFight)
            currentY += 110
            
        self.fight_window.setGeometry(0, 0, 560, currentY)
        scroll.setWidget(self.fight_window)

        sql = "SELECT MAX(fight) FROM rounds"

        try:
            cur.execute(sql)
            max_fight = cur.fetchall()[0][0]
        except sqlite3.DatabaseError as err:
            print("error ", err)

        cur.close()
        con.close()
        obj = self.findChild(Fight, str(max_fight))
        scroll.ensureWidgetVisible(obj)
        #print("max_fight = ", max_fight, obj.geometry().y())
   
    def selectFight(self, s):
        self.emit(QtCore.SIGNAL("select_fight(QString)"), s)
    
    def showFight(self, s):
        self.emit(QtCore.SIGNAL("show_fight(QString)"), s)
        
    def closeEvent(self, e):
        self.reject()
        #currentY = 0
        #currentHeight = 0

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    q = FightQueue()
    q.show()
    sys.exit(app.exec_())
