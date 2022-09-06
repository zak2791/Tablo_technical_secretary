#*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
import xlrd

class MyTableView(QtGui.QTableView):
    def __init__(self, parent=None):
        QtGui.QTableView.__init__(self, parent)

    def mouseReleaseEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.emit(QtCore.SIGNAL("lr"),0)
        elif e.button() == QtCore.Qt.RightButton:
            self.emit(QtCore.SIGNAL("lr"),1)

class list_family(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.b = ''
        self.r = ''
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.CustomizeWindowHint)
        self.setWindowState(QtCore.Qt.WindowFullScreen)
        self.sel_data = ''
        
        self.l = list()
        self.l.append('-')

        try:
            rb = xlrd.open_workbook('sportsmens.xlsx')
        except FileNotFoundError:
            rb = -1

        lWeight = ['']
        lAge = ['']
        self.sportsmens = []
            
        if rb != -1:    
            sheet = rb.sheet_by_index(0)
            for rownum in range(sheet.nrows):
                row = sheet.row_values(rownum)
                self.sportsmens.append(row[0] + ';' + row[1] + ';' + row[2] + ';' + str(row[3]).replace('.0', ''))
                self.l.append(row[0] + ';' + row[1])
                lAge.append(row[2])                  
                lWeight.append(str(row[3]))
                
            #self.l = self.l[:-1]
            self.l.sort()

        #print(self.sportsmens)
        
        lWeight = list(dict.fromkeys(lWeight))
        lWeight = [each.replace('.0', '') for each in lWeight]
        lWeight.sort()
        #print(lWeight, self.sportsmens)

        lAge = list(dict.fromkeys(lAge))
        lAge.sort()
        #print(self.category)    
        '''
        print(l)
        try:
            f=open("cam.txt", 'r', encoding="cp1251")
            f.close()
        except:
            f=open("cam.txt", 'w', encoding="cp1251")
            f.close()
        '''
        #сортировка по возрасту и весу
        self.cBox = QtGui.QCheckBox(self);
        #выбор возраста
        self.age=QtGui.QComboBox(self)
        self.age.addItems(lAge)                            
        #выбор весовой категории
        self.weight=QtGui.QComboBox(self)
        self.weight.addItems(lWeight)   
        #фамилия "синего"
        self.lbl_blue=QtGui.QLabel('<font color="Blue">blue fam</font>',self)
        self.lbl_blue.setAlignment(QtCore.Qt.AlignCenter)
        #фамилия "красного#
        self.lbl_red=QtGui.QLabel('<font color="Red">red fam</font>',self)
        self.lbl_red.setAlignment(QtCore.Qt.AlignCenter)
        #кнопка скрытия
        btnHide = QtGui.QPushButton("СКРЫТЬ")
        QtCore.QObject.connect(btnHide, QtCore.SIGNAL("clicked()"), self._hide)
        #ввод фамилии
        self.inFam=QtGui.QLineEdit(self)
        self.inFam.setMaxLength(7)
        #self.l=list('-')

        f = QtGui.QFont()
        f.setPointSize(10)

        self.inFam.setFont(f)
        self.weight.setFont(f)
        '''
        try:
            f=open("fam.csv", encoding="cp1251")
            i=1
            for line in f:
                self.l.append(line.rstrip("\n"))
            self.l.sort()
            f.close()
        except:
            pass
        '''
        num_fam = len(self.l)   #количество фамилий в списке
        self.col = 6            #количество колонок в таблице
        raw = num_fam//self.col
        if num_fam % self.col:
            raw += 1            #количество строк в таблице
     
        mdl = QtGui.QStandardItemModel(raw,self.col)

        i = 0        
        for c in range(0,self.col):
            for r in range(0,raw):
                i += 1
                if i>num_fam:
                    break
                item = QtGui.QStandardItem(self.l[i-1])
                mdl.setItem(r,c,item)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.lbl_red,10)
        hbox.addWidget(QtGui.QLabel("Сортировать по возрасту и весу"))
        hbox.addWidget(self.cBox,1)
        hbox.addWidget(QtGui.QLabel("Возраст:"))
        hbox.addWidget(self.age,1)
        hbox.addWidget(QtGui.QLabel("Вес:"))
        hbox.addWidget(self.weight,1)
        hbox.addWidget(btnHide)
        hbox.addWidget(self.inFam,2)
        hbox.addWidget(self.lbl_blue,10)

        self.tbl = MyTableView()
        mainbox = QtGui.QVBoxLayout()
        self.tbl.setModel(mdl)

        sel = self.tbl.selectionModel()
        self.tbl.setGridStyle(2)
        w = self.tbl.width()//self.col
        
        self.tbl.resizeRowsToContents()
        self.tbl.horizontalHeader().hide()
        self.tbl.verticalHeader().hide()
        self.tbl.setShowGrid(True)
        self.tbl.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        
        mainbox.addLayout(hbox)
        #mainbox.addLayout(hbox2)
        mainbox.addWidget(self.tbl)
        
        self.setLayout(mainbox)

        self.connect(sel, QtCore.SIGNAL("selectionChanged(const QItemSelection&, const QItemSelection&)"), self.sel)
        self.connect(self.tbl,    QtCore.SIGNAL("lr"), self.sell)
        self.connect(self.inFam,  QtCore.SIGNAL("textEdited(const QString&)"), self.textEdited)
        
        self.connect(self.weight, QtCore.SIGNAL("activated(const QString&)"),  self.set_weight)
        self.connect(self.weight, QtCore.SIGNAL("activated(const QString&)"),  self.selectWeight)
        self.connect(self.age,    QtCore.SIGNAL("activated(const QString&)"),  self.selectAge)
        self.connect(self.cBox,   QtCore.SIGNAL("stateChanged(int)"),          self.allowSorting)

        if rb == -1:
            dialog = QtGui.QMessageBox(QtGui.QMessageBox.Information, "Внимание!", "Нет корректного файла с фамилиями спортсменов ('fam.xlsx')", QtGui.QMessageBox.Ok)
            dialog.exec_()
        
###############
    def set_weight(self, s):
        self.emit(QtCore.SIGNAL("sig_category(QString)"), s)

    def selectWeight(self, s):
        if self.cBox.isChecked():
            self.l.clear();
            for i in range(0, len(self.sportsmens)):
                if self.sportsmens[i].split(";")[3] == s or s == "":
                    if self.sportsmens[i].split(";")[2] == self.age.currentText() or self.age.currentText() == "":
                        self.l.append(self.sportsmens[i].split(";")[0] + ";" + self.sportsmens[i].split(";")[1])
            self.l.insert(0, "-")
            self.textEdited(self.inFam.text())
        self.inFam.setFocus()
        
    def selectAge(self, s):
        if self.cBox.isChecked():
            self.l.clear()
            for i in range(0, len(self.sportsmens)):
                if self.sportsmens[i].split(";")[2] == s or s == "":
                    if self.sportsmens[i].split(";")[3] == self.weight.currentText() or self.weight.currentText() == "":
                        self.l.append(self.sportsmens[i].split(";")[0] + ";" + self.sportsmens[i].split(";")[1])
            self.l.insert(0, "-");
            self.textEdited(self.inFam.text());
        self.inFam.setFocus()

    def allowSorting(self, i):
        if i:
            self.selectWeight(self.weight.currentText())
        else:
            self.l.clear()
            for i in range(0, len(self.sportsmens)):
                self.l.append(self.sportsmens[i].split(";")[0] + ";" + self.sportsmens[i].split(";")[1])
            self.l.insert(0, "-")
            self.textEdited(self.inFam.text())
        self.inFam.setFocus()

    def showEvent(self, e):
        self.inFam.setFocus()
    #########################################################################################
    def textEdited(self,x):
        inL=list()
        for i in self.l:
            if i.upper().startswith(x.upper()):
                inL.append(i)
        if x=='':
            lst=self.l
        else:
            lst=inL

        num_fam = len(lst)   #количество фамилий в списке
        raw = num_fam//self.col
        if num_fam % self.col:
            raw += 1        #количество строк в таблице
     
        mdl = QtGui.QStandardItemModel(raw,self.col)

        i = 0
        
        for c in range(0,self.col):
            for r in range(0,raw):
                i += 1
                if i>num_fam:
                    break
                item = QtGui.QStandardItem(lst[i-1])
                mdl.setItem(r,c,item)
        self.tbl.setModel(mdl)      
        self.connect(self.tbl.selectionModel(),QtCore.SIGNAL("selectionChanged(const QItemSelection&, const QItemSelection&)"),self.sel)
############################################################################################   
    def _hide(self):
        self.emit(QtCore.SIGNAL("family"))
        self.emit(QtCore.SIGNAL("hide"), self.b, self.r)

    def sel(self,a,b):
        self.sel_data = a.indexes()[0].data()
        self.inFam.setFocus()

    def sell(self,lr):
        if lr:
            self.lbl_blue.setText('<font color="Blue"size=5>' + self.sel_data + '</font>')
            self.b = self.sel_data
        else:
            self.lbl_red.setText('<font color="Red" size=5>' + self.sel_data + '</font>')
            self.r = self.sel_data
        self.inFam.setFocus()
        
    def resizeEvent(self,e):
        for i in range(0,self.col):
            self.tbl.setColumnWidth(i,(self.tbl.rect().width()-20)//self.col)
            
        
if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    bl = list_family()
    bl.show()
    
    sys.exit(app.exec_())
