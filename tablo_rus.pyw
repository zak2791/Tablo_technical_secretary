#!E:\Python34\pythonw
# -*- coding: utf-8 -*-
import sys, sqlite3
import os
import first, ball, fam_reg, plus
from PyQt4 import QtGui, QtCore, uic
import narusheniya_pravil
import narusheniya_vihody
import dualwiev
#import new_list_window

import category, secretary2, udp_client


HEIGHT_REGION = 0
HEIGHT_FAMILY = 0

class ev_L(QtCore.QEvent):
    idType = QtCore.QEvent.registerEventType()
    def __init__(self):
        QtCore.QEvent.__init__(self, ev_L.idType)

class ev_R(QtCore.QEvent):
    idType = QtCore.QEvent.registerEventType()
    def __init__(self):
        QtCore.QEvent.__init__(self, ev_R.idType)
class ThreadSound(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        #self.zvuk = wav
    def run(self):
        zvuk = QtGui.QSound('1.wav')
        zvuk.play()

class FormView(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi("FormView.ui", self)
        '''
        self.label_2.setMargin(3)
        self.label_3.setMargin(3)
        self.label_4.setMargin(3)
        self.label_5.setMargin(3)
        '''

class frmTime(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi("frmTime.ui", self)

class GridLayout2(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        if not os.path.isfile('baza_in.db'):
            con = sqlite3.connect('baza_in.db')
            cur = con.cursor()
            sql = """
                     CREATE TABLE rounds (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         num_round INTEGER,
                         name_round TEXT,
                         name_red TEXT,
                         name_blue TEXT,
                         note_red TEXT,
                         note_blue TEXT,
                         num_fight INTEGER);
                     CREATE TABLE referees (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         id_fight INTEGER,
                         ref1 TEXT,
                         ref2 TEXT,
                         ref3 TEXT);
                  """
            try:
                cur.executescript(sql)
                con.commit()
            except sqlite3.DatabaseError as err:
                print("error ", err)
            cur.close()
            con.close()

        if not os.path.isfile('baza_out.db'):
            con = sqlite3.connect('baza_out.db')
            cur = con.cursor()
            sql = """
                     CREATE TABLE rounds (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         fight INTEGER,
                         result BLOB)
                  """
            try:
                cur.execute(sql)
                con.commit()
            except sqlite3.DatabaseError as err:
                print("error ", err)
            cur.close()
            con.close()

        self.setWindowState(QtCore.Qt.WindowFullScreen)

        self.formView = FormView()
        self.View = 0

        self.formTime = frmTime()
        self.connect(self.formTime.dMin, QtCore.SIGNAL("valueChanged(int)"), self.setTime)
        self.connect(self.formTime.dSec, QtCore.SIGNAL("valueChanged(int)"), self.setTime)
        self.connect(self.formTime.dSec2, QtCore.SIGNAL("valueChanged(int)"), self.setTime)
        
        self.minimum_height = 0

        self.percent_height = 0
        #####################################################################################################
        self.spacing = 2                                                #дистанция между элементами табло
        self.margin = 6                                                 #отступ от края экрана до элементов табло
        #self.height_tablo = self.height() - 2 * self.margin             #высота используемой части экрана
        #####################################################################################################
        palW = self.palette()
        palW.setColor(QtGui.QPalette.Window,QtGui.QColor("black"))
        palW.setColor(QtGui.QPalette.WindowText, QtGui.QColor("yellow"))
        self.setPalette(palW)      
        '''
        #окно ввода фамилий
        self.w = new_list_window.list_family(self)
        self.str_blue = '-'
        self.str_red = '-'
        ####################
        #первое техн. для вывода в сеть
        self.pl_l = ' '
        self.pl_r = ' '
        ################################
        '''
        self.flag = QtGui.QPixmap()
        
        self.flag_blue = QtGui.QLabel(self)
        self.flag_blue.setScaledContents(True)

        self.flag_red = QtGui.QLabel(self)
        self.flag_red.setScaledContents(True)
        #####################-----камеры-----##########################
        #self.camera1 = v.video(rtsp1, 'out1.avi', self)
        #self.camera2 = v.video(rtsp2, 'out2.avi', self)
        ###############################################################
        
        col_left = 'white'#'lightblue'#'steelblue'
        col_right = 'white'#'hotpink'
        
        fnt = QtGui.QFont()
        fnt_btn = QtGui.QFont()
        desk = QtGui.QApplication.desktop()

        self.form_vis = 0                           #видимая форма

        self.ves = [' ','6','0','кг']
        
        self.gong_short = QtGui.QSound('2.wav')
       
        self.desk2 = QtGui.QDesktopWidget()#
######################################################################################

        self.kat = category.Category()#QtGui.QLabel()
        self.kat.setStyleSheet("background-color: black; color: yellow")

        fnt.setPixelSize(self.height() / 10)

        fnt_btn.setPixelSize(self.height()/40)    

        self.famLeft = fam_reg.Fam(col_left,'',63)
        self.regLeft = fam_reg.Fam(col_left,'',10,'Lucida Console')
        
        self.famRight = fam_reg.Fam(col_right,'',63)
        self.regRight = fam_reg.Fam(col_right,'',10,'Lucida Console')

        self.plus_red = plus.plus(col_left, self)
               
        self.plus_blue = plus.plus(col_right, self)
              
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
        
        ##############################################
        self.ev_L = ev_L()
        self.ev_R = ev_R()
        ###########################################
           
################################################################################        
        self.sek = first.DigitalClock(self.ev_L.idType, self.ev_R.idType, "chartreuse","green", 1.30, -1, False, False)
        #self.sek.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        self.sek_left = first.DigitalClock(self.ev_L.idType, self.ev_R.idType, 'lightblue',"blue", 0.20, 1, True, False)
        
        self.sek_right = first.DigitalClock(self.ev_L.idType, self.ev_R.idType, "salmon", "red", 0.20, 1, True, False)
        
        self.sek_left.setVisible(False)
        self.sek_right.setVisible(False)

        self.sek_left_TV = first.DigitalClock(self.ev_L.idType, self.ev_R.idType, "lightblue", 'blue', 2.00,1, True, False)
        
        self.sek_right_TV = first.DigitalClock(self.ev_L.idType, self.ev_R.idType, "salmon", 'red', 2.00,1, True, False)
        
        self.sek_left_TV.setVisible(False)
        self.sek_right_TV.setVisible(False)
################################################################################
        self.btnTime = QtGui.QPushButton("ВРЕМЯ")
        self.btnTime.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        self.btnTime.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnTime, QtCore.SIGNAL("clicked()"), self.fightTime) #self.but_timer)

        self.btnSetTime = QtGui.QPushButton("Установка\nвремени")
        self.btnSetTime.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        self.btnSetTime.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnSetTime, QtCore.SIGNAL("clicked()"), self.formTime, QtCore.SLOT("show()"))

        self.btnParter_red = QtGui.QPushButton("ПАРТЕР")
        self.btnParter_red.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        self.btnParter_red.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnParter_red, QtCore.SIGNAL("clicked()"), self.parter_red)
        
        self.btnParter_blue = QtGui.QPushButton("ПАРТЕР")
        self.btnParter_blue.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        self.btnParter_blue.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnParter_blue, QtCore.SIGNAL("clicked()"), self.parter_blue)

        self.btnTechnical_red = QtGui.QPushButton("ТЕХ.ВР.")
        self.btnTechnical_red.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        self.btnTechnical_red.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnTechnical_red, QtCore.SIGNAL("clicked()"), self.t_red)

        self.btnTechnical_blue = QtGui.QPushButton("ТЕХ.ВР.")
        self.btnTechnical_blue.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        self.btnTechnical_blue.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnTechnical_blue, QtCore.SIGNAL("clicked()"), self.t_blue)

        self.btnSettings = QtGui.QPushButton("НАСТРОЙКИ")
        self.btnSettings.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        self.btnSettings.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnSettings, QtCore.SIGNAL("clicked()"), self.family)

        self.btnScreenshot = QtGui.QPushButton("Второй экран")
        self.btnScreenshot.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        self.btnScreenshot.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnScreenshot, QtCore.SIGNAL("clicked()"), self.screenshot)
        
        self.btnPlus_red = QtGui.QPushButton("+")
        self.btnPlus_red.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        self.btnPlus_red.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnPlus_red, QtCore.SIGNAL("clicked()"), self.plu_red)

        self.btnPlus_blue = QtGui.QPushButton("+")
        self.btnPlus_blue.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        self.btnPlus_blue.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnPlus_blue, QtCore.SIGNAL("clicked()"), self.plu_blue)

        self.btnView = QtGui.QPushButton("Вид")
        self.btnView.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        self.btnView.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.btnView, QtCore.SIGNAL("clicked()"), self.formView, QtCore.SLOT("show()"))

        self.btnQueue = QtGui.QPushButton("Очередь")
        self.btnQueue.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        self.btnQueue.setFocusPolicy(QtCore.Qt.NoFocus)
        

        num_disp = QtGui.QLabel("Нет подключения внешнего экрана\nв режиме 'расширенного рабочего стола'")
        font = QtGui.QFont()
        font.setPixelSize(15)
        num_disp.setFont(font)
        num_disp.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        #num_disp.setFontSize(num_disp.height())

        self.secr = secretary2.Secretary(self)
        QtCore.QObject.connect(self.btnQueue, QtCore.SIGNAL("clicked()"), self.secr.showQueue)

        #окно индикации наличия связи
        self.winConnect = QtGui.QLabel("нет\nсоединения")
        self.winConnect.setAlignment(QtCore.Qt.AlignCenter)
        self.winConnect.setStyleSheet("QLabel{border-style: solid; border-color: red; border-width: 2px; border-radius: 5px; \
                                      background-color: black; color: red; font: bold}")
        ##############################################################################
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(3)
        
        #self.grid.addWidget(self.famRight,          0, 0, 6, 34)
        #self.grid.addWidget(self.famLeft,           0, 34, 6, 34)
        
        self.grid.addWidget(self.ball_right,        0, 0, 19, 24)
        self.grid.addWidget(self.ball_left,         0, 44, 19, 24)
        self.grid.addWidget(self.akt_right,         19, 0, 13, 14)
        self.grid.addWidget(self.akt_left,          19, 54, 13, 14)

        self.grid.addWidget(self.btnQueue,          29, 14, 3, 5)
        self.grid.addWidget(self.btnSetTime,        29, 19, 3, 5)

        self.grid.addWidget(self.btnParter_red,     26, 44, 2, 5)
        self.grid.addWidget(self.btnTime,           29, 44, 3, 10)
        self.grid.addWidget(self.btnParter_blue,    26, 49, 2, 5)

        self.grid.addWidget(self.btnTechnical_red,  24, 44, 2, 5)
        #self.grid.addWidget(self.btnSettings,       6, 30, 2, 8)
        self.grid.addWidget(self.btnTechnical_blue, 24, 49, 2, 5)

        self.grid.addWidget(self.NP_left,           19, 19, 5, 5)
        self.grid.addWidget(self.NP_right,          19, 44, 5, 5)

        self.grid.addWidget(self.NV_left,           19, 14, 5, 5)
        self.grid.addWidget(self.NV_right,          19, 49, 5, 5)
        
        

        #self.grid.addWidget(self.btnPlus_red,       8, 28, 2, 3)
        #self.grid.addWidget(self.btnPlus_blue,      8, 37, 2, 3)

        self.grid.addWidget(self.plus_red,        8, 24, 4, 4)
        self.grid.addWidget(self.plus_blue,         8, 40, 4, 4)

        if self.desk2.numScreens()==1:
            self.grid.addWidget(num_disp,          12, 24, 4, 20)
        
        self.grid.addWidget(self.kat,               0, 30, 2, 4)
        self.grid.addWidget(self.winConnect,        0, 34, 2, 4)
        
        self.grid.addWidget(self.btnView,           2, 38, 2, 6)
        self.grid.addWidget(self.btnScreenshot,     0, 38, 2, 6)
        

        
        
        self.grid.addWidget(self.sek_right,         9, 0, 12, 24)
        self.grid.addWidget(self.sek_left,          9, 44, 12, 24)

        self.grid.addWidget(self.sek_right_TV,      9, 0, 12, 24)
        self.grid.addWidget(self.sek_left_TV,       9, 44, 12, 24)
        
        #self.grid.addWidget(self.flag_red,          29, 14, 8, 10)
        #self.grid.addWidget(self.flag_blue,         29, 44, 8, 10)
        
        self.grid.addWidget(self.sek,               19, 24, 13, 20)
        
        #self.grid.addWidget(self.regRight,          37, 0, 5, 34)
        #self.grid.addWidget(self.regLeft,           37, 34, 5, 34)

        self.grid.addWidget(self.secr,              32, 0, 10, 68)

        self.grid.setAlignment(self.grid, QtCore.Qt.AlignVCenter)

        self.setLayout(self.grid)
        
        self.thread_sound = ThreadSound()
        
   
        if self.desk2.numScreens()==1:
            dialog = QtGui.QMessageBox(QtGui.QMessageBox.Information, "Внимание!", "Для корректной работы программы подключите  внешний \
                                                                       дисплей и в настройках графики в разделе'Дисплеи' укажите \
                                                                       'расширенный рабочий стол' или 'дополнительный дисплей(dualwiev). \
                                                                       Основным дисплеем должен быть указан дисплей ноутбука.'", QtGui.QMessageBox.Ok)
            dialog.exec_()
        else:
            self.secondDisplay = dualwiev.desktop(self.ev_L.idType, self.ev_R.idType, self.View)
            self.secondDisplay.setGeometry(desk.availableGeometry(1).left(),0,100,100)
            self.secondDisplay.showFullScreen()
        
 #################################################################################################################               
        self.connect(self.sek, QtCore.SIGNAL("sound"), self.sound)
        self.connect(self.sek_left, QtCore.SIGNAL("sound"), self.gong_short.play)
        self.connect(self.sek_right, QtCore.SIGNAL("sound"), self.gong_short.play)

        #self.connect(self.w, QtCore.SIGNAL("family"), self.family)
        
        #self.connect(self.w.weight,QtCore.SIGNAL("activated(const QString&)"),self.kat.setText)
        #if self.desk2.numScreens()==2:
            #self.connect(self.w.weight,QtCore.SIGNAL("activated(const QString&)"),self.secondDisplay.kat.setText)
        
        #self.connect(self.w.weight,QtCore.SIGNAL("activated(const QString&)"),self.weight)        

        #self.connect(self.w, QtCore.SIGNAL("hide"), self.family_blue)
        #self.connect(self.w, QtCore.SIGNAL("hide"), self.family_red)

        if self.desk2.numScreens()==2:
            self.connect(self.NP_right, QtCore.SIGNAL("change_np"), self.secondDisplay.NP_right.setValue)
            self.connect(self.NP_left, QtCore.SIGNAL("change_np"), self.secondDisplay.NP_left.setValue)
            self.connect(self.NV_right, QtCore.SIGNAL("change_nv"), self.secondDisplay.NV_right.setValue)
            self.connect(self.NV_left, QtCore.SIGNAL("change_nv"), self.secondDisplay.NV_left.setValue)

            self.connect(self.sek,  QtCore.SIGNAL("sec_sig(QString, QPalette)"), self.secondDisplay.sek.doubleTime)
#############################################################################################################################################

        

        #time.sleep(5)
        self.famil_r=''
        self.famil_l=''

        self.show()
 
        self.btnTime.setStyleSheet("color: green; font: bold " + str(round(self.btnTime.height() / 2)) + "px;")
        self.btnParter_red.setStyleSheet("color: red; font: bold " + str(round(self.btnParter_red.height() / 2)) + "px;")
        self.btnParter_blue.setStyleSheet("color: blue; font: bold " + str(round(self.btnParter_blue.height() / 2)) + "px;")
        self.btnTechnical_red.setStyleSheet("color: red; font: bold " + str(round(self.btnTechnical_red.height() / 2)) + "px;")
        self.btnTechnical_blue.setStyleSheet("color: blue; font: bold " + str(round(self.btnTechnical_blue.height() / 2)) + "px;")
        self.btnSettings.setStyleSheet("color: green; font: bold " + str(round(self.btnSettings.height() / 2)) + "px;")
        self.btnPlus_red.setStyleSheet("color: red; font: bold " + str(round(self.btnPlus_red.height() / 2)) + "px;")
        self.btnPlus_blue.setStyleSheet("color: blue; font: bold " + str(round(self.btnPlus_blue.height() / 2)) + "px;")
        self.btnView.setStyleSheet("color: black; font: bold " + str(round(self.btnView.height() / 2)) + "px;")

        QtCore.QObject.connect(self.formView.rbView1, QtCore.SIGNAL("toggled(bool)"), self.setView)
        QtCore.QObject.connect(self.formView.rbView2, QtCore.SIGNAL("toggled(bool)"), self.setView)
        QtCore.QObject.connect(self.formView.rbView3, QtCore.SIGNAL("toggled(bool)"), self.setView)
        QtCore.QObject.connect(self.formView.sbFrame, QtCore.SIGNAL("valueChanged(int)"), self.setFrameWidth)
        QtCore.QObject.connect(self.formView.sbSpacing, QtCore.SIGNAL("valueChanged(int)"), self.setSpace)
        QtCore.QObject.connect(self.formView.sbSec, QtCore.SIGNAL("valueChanged(int)"), self.setSec)
        QtCore.QObject.connect(self.formView.btnNameMinus, QtCore.SIGNAL("clicked()"),  self.changeSize)
        QtCore.QObject.connect(self.formView.btnNamePlus,  QtCore.SIGNAL("clicked()"),  self.changeSize)
        QtCore.QObject.connect(self.formView.btnRegMinus,  QtCore.SIGNAL("clicked()"),  self.changeSize)
        QtCore.QObject.connect(self.formView.btnRegPlus,   QtCore.SIGNAL("clicked()"),  self.changeSize)

        if self.desk2.numScreens() == 2:
            self.connect(self.plus_red,   QtCore.SIGNAL("textChange(QString)"), self.secondDisplay.plus_right.setData)
            self.connect(self.plus_blue,  QtCore.SIGNAL("textChange(QString)"), self.secondDisplay.plus_left.setData)
            '''
            self.connect(self.famRight,  QtCore.SIGNAL("sigText(QString)"), self.secondDisplay.fam_red.text)
            self.connect(self.famLeft,   QtCore.SIGNAL("sigText(QString)"), self.secondDisplay.fam_blue.text)
            self.connect(self.regRight,  QtCore.SIGNAL("sigText(QString)"), self.secondDisplay.reg_red.text)
            self.connect(self.regLeft,   QtCore.SIGNAL("sigText(QString)"), self.secondDisplay.reg_blue.text)
            '''
            self.connect(self.secr, QtCore.SIGNAL("nameRed(QString)"),  self.secondDisplay.fam_red.text)
            self.connect(self.secr, QtCore.SIGNAL("nameBlue(QString)"), self.secondDisplay.fam_blue.text)
            self.connect(self.secr, QtCore.SIGNAL("regRed(QString)"),   self.secondDisplay.reg_red.text)
            self.connect(self.secr, QtCore.SIGNAL("regBlue(QString)"),  self.secondDisplay.reg_blue.text)

            self.connect(self.secr, QtCore.SIGNAL("setWeight(QString)"),  self.kat.setData)
            if self.desk2.numScreens() == 2:
                self.connect(self.secr, QtCore.SIGNAL("setWeight(QString)"),  self.secondDisplay.kat.setData)
            
            self.connect(self.ball_right, QtCore.SIGNAL("ball(int)"), self.secondDisplay.ball_right.setBall)
            self.connect(self.ball_left, QtCore.SIGNAL("ball(int)"), self.secondDisplay.ball_left.setBall)
            self.connect(self.akt_right, QtCore.SIGNAL("ball(int)"), self.secondDisplay.akt_right.setBall)
            self.connect(self.akt_left, QtCore.SIGNAL("ball(int)"), self.secondDisplay.akt_left.setBall)

            self.connect(self.sek_right, QtCore.SIGNAL("sec_visible(bool)"),                self.secondDisplay.sek_right.setVisible)
            self.connect(self.sek_right,  QtCore.SIGNAL("sec_sig(QString, QPalette)"),      self.secondDisplay.sek_right.doubleTime)

            self.connect(self.sek_left, QtCore.SIGNAL("sec_visible(bool)"),                 self.secondDisplay.sek_left.setVisible)
            self.connect(self.sek_left,  QtCore.SIGNAL("sec_sig(QString, QPalette)"),       self.secondDisplay.sek_left.doubleTime)

            self.connect(self.sek_right_TV, QtCore.SIGNAL("sec_visible(bool)"),             self.secondDisplay.sek_right_TV.setVisible)
            self.connect(self.sek_right_TV,  QtCore.SIGNAL("sec_sig(QString, QPalette)"),   self.secondDisplay.sek_right_TV.doubleTime)

            self.connect(self.sek_left_TV, QtCore.SIGNAL("sec_visible(bool)"),              self.secondDisplay.sek_left_TV.setVisible)
            self.connect(self.sek_left_TV,  QtCore.SIGNAL("sec_sig(QString, QPalette)"),    self.secondDisplay.sek_left_TV.doubleTime)

        if self.desk2.numScreens()==1:
            self.btnScreenshot.setEnabled(False)
        '''
        self.FileStart = QtCore.QFile("start.txt")
        if not self.FileStart.exists():
            self.FileStart.open(QtCore.QFile.WriteOnly)
            self.FileStart.close()
        else:
            self.FileStart.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
            st = QtCore.QTextStream(self.FileStart)
            i = 0
            while not st.atEnd():
                line = st.readLine()
                i += 1
                self.process_line(i, line)
        
        self.FileStart.close()
        '''
        
        self.mat = QtCore.QFile("mat.txt")
        if not self.mat.exists():
            self.mat.open(QtCore.QFile.WriteOnly)
            self.mat.write("1")
            self.mat.close()
        self.mat.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        mat = self.mat.read(1)
        self.mat.close()
        self.secr.setMat(mat)

        
        
        self.thr = QtCore.QThread()
        self.udpClient = udp_client.udpClient(mat)
        self.udpClient.moveToThread(self.thr)
        self.connect(self.thr, QtCore.SIGNAL("started()"), self.udpClient.run)
        self.connect(self.udpClient, QtCore.SIGNAL("conn"), self.connUdp)
        self.connect(self.udpClient, QtCore.SIGNAL("conn"), self.secr.setAddr)
        self.thr.start()

        self.tcpThread = QtCore.QThread()
        self.tcpServer = udp_client.TcpServer(mat)
        self.tcpServer.moveToThread(self.tcpThread)
        self.connect(self.tcpThread, QtCore.SIGNAL("started()"), self.tcpServer.run)
        self.tcpThread.start()
        
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.connect(self.sek, QtCore.SIGNAL("past_time(QString)"), self.secr.pastTime)
        self.connect(self.secr, QtCore.SIGNAL("change_rate(int, int, int, int)"), self.setRates)
        self.connect(self.secr, QtCore.SIGNAL("change_prav(int, QString)"), self.setPrav)
        self.connect(self.secr, QtCore.SIGNAL("change_vyh(int, QString)"), self.setVyh)
        self.connect(self.secr, QtCore.SIGNAL("set_plus(int, QString)"), self.setPlus)

        self.screen = QtGui.QLabel(self)
        self.screen.setFixedSize(self.width() / 2, self.height() / 2)
        self.screen.move(0, 0)
        self.screen.hide()

    def setPlus(self, rb, p):
        if rb:
            self.plus_blue.setData(p)
        else:
            self.plus_red.setData(p)
        
    def setVyh(self, rb, v):
        if rb:
            self.NV_right.setValue(v)
            if self.desk2.numScreens() == 2:
                self.secondDisplay.NV_right.setValue(v)
        else:
            self.NV_left.setValue(v)
            if self.desk2.numScreens() == 2:
                self.secondDisplay.NV_left.setValue(v)
                
    def setPrav(self, rb, p):
        if rb:
            self.NP_right.setValue(p)
            if self.desk2.numScreens() == 2:
                self.secondDisplay.NP_right.setValue(p)
        else:
            self.NP_left.setValue(p)
            if self.desk2.numScreens() == 2:
                self.secondDisplay.NP_left.setValue(p)

    def setRates(self, rb, bb, ra, ba):
        self.ball_right.setBall(rb)
        self.ball_left.setBall(bb)
        self.akt_right.setBall(ra)
        self.akt_left.setBall(ba)

    def connUdp(self, s, i):
        if i == "":
            self.winConnect.setStyleSheet("QLabel{border-style: solid; border-color: red; border-width: 2px; \
                                          border-radius: 5px; background-color: black; color: red; font: bold}")
            self.winConnect.setText("нет\nсоединения")
        else:
            self.winConnect.setStyleSheet("QLabel{border-style: solid; border-color: lightgreen; border-width: 2px; \
                                          border-radius: 5px; background-color: black; color: lightgreen; font: bold}")
            
            self.winConnect.setText("Соединено\nc ковром " + str(int(int(i) / 10000)))
        
    def process_line(self, i, s):
        if i == 1:
            self.famRight.text(s)
        elif i ==  2:
            self.famLeft.text(s)
        elif i == 3:
            self.ball_right.setBall(int(s))
        elif i == 4:
            self.ball_left.setBall(int(s))
        elif i == 5:
            if s == "1":
                self.plus_red.setData("+")
            if s == "2":
                self.plus_blue.setData("+")
        elif i == 6:
            self.kat.setData(s)
        elif i == 7:
            self.akt_right.setBall(int(s))
        elif i == 8:
            self.akt_left.setBall(int(s))
        elif i == 9:
            self.NV_right.setValue(s)
            if self.desk2.numScreens() == 2:
                self.secondDisplay.NV_right.setValue(s)
        elif i == 10:
            self.NP_right.setValue(s)
            if self.desk2.numScreens() == 2:
                self.secondDisplay.NP_right.setValue(s)
        elif i == 11:
            self.NP_left.setValue(s)
            if self.desk2.numScreens() == 2:
                self.secondDisplay.NP_left.setValue(s)
        elif i == 12:
            self.NV_left.setValue(s)
            if self.desk2.numScreens() == 2:
                self.secondDisplay.NV_left.setValue(s)
        elif i == 13:
            self.sek.showLastTime(s)
        elif i == 14:
            self.regRight.text(s)
        elif i == 15:
            self.regLeft.text(s)

    def fightTime(self):
        if self.sek_right_TV.isActive() or self.sek_left_TV.isActive():
            return
        if self.sek_right_TV.getVisible() or self.sek_left_TV.getVisible():
            self.sek_right_TV.setVisible(False)
            self.sek_right_TV.sec_visible(False)
            self.sek_left_TV.setVisible(False)
            self.sek_left_TV.sec_visible(False)
            return
        
        if(self.sek.isActive()):
            if(self.sek_right.isActive()):
                self.sek_right.startstop()
            if(self.sek_left.isActive()):
                self.sek_left.startstop()
            self.sek.startstop()
        else:
            if(self.sek_right.getVisible() or self.sek_left.getVisible()):
                self.sek_right.setVisible(False)
                self.sek_right.sec_visible(False)
                self.sek_left.setVisible(False)
                self.sek_left.sec_visible(False)
            else:
                self.sek.startstop()
                self.sek_right.clearTimer()
                self.sek_left.clearTimer()

    def parter_red(self):
        if self.sek_right_TV.getVisible() or self.sek_left_TV.getVisible():
            return
        if self.sek_right.getVisible() == False:
            self.sek_right.setVisible(True)
            if self.sek.isActive():
                self.sek_right.startstop()
            else:
                self.sek_right.sec_visible(True)
        else:
            if self.sek.isActive():
                if not self.sek_right.isActive():
                    self.sek_right.clearTimer()
                self.sek_right.startstop()
            else:
                self.sek_right.setVisible(False)
                self.sek_right.sec_visible(False)

    def parter_blue(self):
        if self.sek_right_TV.getVisible() or self.sek_left_TV.getVisible():
            return
        if self.sek_left.getVisible() == False:
            self.sek_left.setVisible(True)
            if self.sek.isActive():
                self.sek_left.startstop()
            else:
                self.sek_left.sec_visible(True)
        else:
            if self.sek.isActive():
                if not self.sek_left.isActive():
                    self.sek_left.clearTimer()
                self.sek_left.startstop()
            else:
                self.sek_left.setVisible(False)
                self.sek_left.sec_visible(False)

    def t_red(self):
        if not self.sek.isActive() and not self.sek_right.getVisible() and  not self.sek_left.getVisible():
            self.sek_right_TV.setVisible(True)
            self.sek_right_TV.startstop()

    def t_blue(self):
        if not self.sek.isActive() and not self.sek_right.getVisible() and not self.sek_left.getVisible():
            self.sek_left_TV.setVisible(True)
            self.sek_left_TV.startstop()

    def setTime(self):
        min1 = self.formTime.dMin.value()
        sec1 = self.formTime.dSec.value()
        sec2 = self.formTime.dSec2.value()
        if min1 == 0 and sec1 == 0 and sec2 == 0:
            return
        self.sek.setTime(min1, sec1, sec2)
        
    def setSec(self, s):
        #self.grid.removeWidget(self.sek)
        if self.desk2.numScreens() != 1:
            self.secondDisplay.grid.removeWidget(self.secondDisplay.sek)
        if s == 3:
             #self.grid.addWidget(self.sek, 24, 24, 13, 20)
             if self.desk2.numScreens() != 1:
                 self.secondDisplay.grid.addWidget(self.secondDisplay.sek, 24, 24, 13, 20)
        elif s == 2:
             #self.grid.addWidget(self.sek, 25, 24, 11, 20)
             if self.desk2.numScreens() != 1:
                 self.secondDisplay.grid.addWidget(self.secondDisplay.sek, 25, 24, 11, 20)
        else:
             #self.grid.addWidget(self.sek, 26, 24, 9, 20)
             if self.desk2.numScreens() != 1:
                 self.secondDisplay.grid.addWidget(self.secondDisplay.sek, 26, 24, 9, 20)
        self.updateScreen()

    def setSpace(self, s):
        #self.grid.setSpacing(s)
        #self.repaint()
        if self.desk2.numScreens() != 1:
            self.secondDisplay.grid.setSpacing(s)
            self.secondDisplay.repaint()
            self.updateScreen()
            
    def setView(self):
        if self.formView.rbView1.isChecked():
            self.View = 0
            self.ball_right.setViewStyle(0, self.formView.sbFrame.value())
            self.ball_left.setViewStyle(0,  self.formView.sbFrame.value())
            self.akt_right.setViewStyle(0,  self.formView.sbFrame.value())
            self.akt_left.setViewStyle(0,   self.formView.sbFrame.value())
            self.famRight.setViewStyle(0)
            self.famLeft.setViewStyle(0)
            self.regRight.setViewStyle(0)
            self.regLeft.setViewStyle(0)
            self.famRight.align = 0
            self.famLeft.align  = 0
            self.regRight.align = 0
            self.regLeft.align  = 0
            self.sek.setFrameShape(QtGui.QFrame.Box)
            self.plus_red.setColor("white")
            self.plus_blue.setColor("white")
            if self.desk2.numScreens() != 1:
                self.secondDisplay.View = 0
                self.secondDisplay.ball_right.setViewStyle(0, self.formView.sbFrame.value())
                self.secondDisplay.ball_left.setViewStyle(0,  self.formView.sbFrame.value())
                self.secondDisplay.akt_right.setViewStyle(0,  self.formView.sbFrame.value())
                self.secondDisplay.akt_left.setViewStyle(0,   self.formView.sbFrame.value())
                self.secondDisplay.fam_red.setViewStyle(0)
                self.secondDisplay.fam_blue.setViewStyle(0)
                self.secondDisplay.reg_red.setViewStyle(0)
                self.secondDisplay.reg_blue.setViewStyle(0)
                self.secondDisplay.fam_red.align  = 0
                self.secondDisplay.fam_blue.align = 0
                self.secondDisplay.reg_red.align  = 0
                self.secondDisplay.reg_blue.align = 0
                self.secondDisplay.sek.setFrameShape(QtGui.QFrame.Box)
                self.secondDisplay.plus_right.setColor("white")
                self.secondDisplay.plus_left.setColor("white")
                self.secondDisplay.repaint()
        elif self.formView.rbView2.isChecked():
            self.View = 1
            self.ball_right.setViewStyle(1, self.formView.sbFrame.value())
            self.ball_left.setViewStyle(2,  self.formView.sbFrame.value())
            self.akt_right.setViewStyle(1,  self.formView.sbFrame.value())
            self.akt_left.setViewStyle(2,   self.formView.sbFrame.value())
            self.famRight.setViewStyle(1)
            self.famLeft.setViewStyle(2)
            self.regRight.setViewStyle(1)
            self.regLeft.setViewStyle(2)
            self.famRight.align = 1
            self.famLeft.align  = 2
            self.regRight.align = 1
            self.regLeft.align  = 2
            self.sek.setFrameShape(QtGui.QFrame.Box)
            self.plus_red.setColor("red")
            self.plus_blue.setColor("blue")
            if self.desk2.numScreens() != 1:
                self.secondDisplay.View = 1
                self.secondDisplay.ball_right.setViewStyle(1, self.formView.sbFrame.value())
                self.secondDisplay.ball_left.setViewStyle(2,  self.formView.sbFrame.value())
                self.secondDisplay.akt_right.setViewStyle(1,  self.formView.sbFrame.value())
                self.secondDisplay.akt_left.setViewStyle(2,   self.formView.sbFrame.value())
                self.secondDisplay.fam_red.setViewStyle(1)
                self.secondDisplay.fam_blue.setViewStyle(2)
                self.secondDisplay.reg_red.setViewStyle(1)
                self.secondDisplay.reg_blue.setViewStyle(2)
                self.secondDisplay.fam_red.align  = 2
                self.secondDisplay.fam_blue.align = 1
                self.secondDisplay.reg_red.align  = 2
                self.secondDisplay.reg_blue.align = 1
                self.secondDisplay.sek.setFrameShape(QtGui.QFrame.Box)
                self.secondDisplay.plus_right.setColor("red")
                self.secondDisplay.plus_left.setColor("blue")
                self.secondDisplay.repaint()
        else:
            self.View = 1
            self.ball_right.setViewStyle(3, self.formView.sbFrame.value())
            self.ball_left.setViewStyle(4,  self.formView.sbFrame.value())
            self.akt_right.setViewStyle(3,  self.formView.sbFrame.value())
            self.akt_left.setViewStyle(4,   self.formView.sbFrame.value())
            self.famRight.setViewStyle(1)
            self.famLeft.setViewStyle(2)
            self.regRight.setViewStyle(1)
            self.regLeft.setViewStyle(2)
            self.famRight.align = 1
            self.famLeft.align  = 2
            self.regRight.align = 1
            self.regLeft.align  = 2
            self.sek.setFrameShape(QtGui.QFrame.NoFrame)
            self.plus_red.setColor("red")
            self.plus_blue.setColor("blue")
            if self.desk2.numScreens() != 1:
                self.secondDisplay.View = 1
                self.secondDisplay.ball_right.setViewStyle(3, self.formView.sbFrame.value())
                self.secondDisplay.ball_left.setViewStyle(4,  self.formView.sbFrame.value())
                self.secondDisplay.akt_right.setViewStyle(3,  self.formView.sbFrame.value())
                self.secondDisplay.akt_left.setViewStyle(4,   self.formView.sbFrame.value())
                self.secondDisplay.fam_red.setViewStyle(1)
                self.secondDisplay.fam_blue.setViewStyle(2)
                self.secondDisplay.reg_red.setViewStyle(1)
                self.secondDisplay.reg_blue.setViewStyle(2)
                self.secondDisplay.fam_red.align  = 2
                self.secondDisplay.fam_blue.align = 1
                self.secondDisplay.reg_red.align  = 2
                self.secondDisplay.reg_blue.align = 1
                self.secondDisplay.sek.setFrameShape(QtGui.QFrame.NoFrame)
                self.secondDisplay.plus_right.setColor("red")
                self.secondDisplay.plus_left.setColor("blue")
                self.secondDisplay.repaint()
        self.repaint()
        self.updateScreen()
        
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

    def changeSize(self):
        global HEIGHT_REGION
        global HEIGHT_FAMILY

        if self.sender().objectName() == "btnNameMinus":
            i = 1
        elif self.sender().objectName() == "btnNamePlus":
            i = 0
        elif self.sender().objectName() == "btnRegPlus":
            i = 2
        else:
            i = 3
        
        if i == 0:
            if HEIGHT_FAMILY < 5:
                HEIGHT_FAMILY += 1
                '''
                self.grid.setRowMinimumHeight(0, self.minimum_height + HEIGHT_FAMILY * self.percent_height / 6)
                self.grid.setRowMinimumHeight(1, self.minimum_height + HEIGHT_FAMILY * self.percent_height / 6)
                self.grid.setRowMinimumHeight(2, self.minimum_height + HEIGHT_FAMILY * self.percent_height / 6)
                self.grid.setRowMinimumHeight(3, self.minimum_height + HEIGHT_FAMILY * self.percent_height / 6)
                self.grid.setRowMinimumHeight(4, self.minimum_height + HEIGHT_FAMILY * self.percent_height / 6)
                self.grid.setRowMinimumHeight(5, self.minimum_height + HEIGHT_FAMILY * self.percent_height / 6)
                '''
                if self.desk2.numScreens() != 1:
                    self.secondDisplay.grid.setRowMinimumHeight(0, self.secondDisplay.minimum_height + HEIGHT_FAMILY * self.secondDisplay.percent_height / 6)
                    self.secondDisplay.grid.setRowMinimumHeight(1, self.secondDisplay.minimum_height + HEIGHT_FAMILY * self.secondDisplay.percent_height / 6)
                    self.secondDisplay.grid.setRowMinimumHeight(2, self.secondDisplay.minimum_height + HEIGHT_FAMILY * self.secondDisplay.percent_height / 6)
                    self.secondDisplay.grid.setRowMinimumHeight(3, self.secondDisplay.minimum_height + HEIGHT_FAMILY * self.secondDisplay.percent_height / 6)
                    self.secondDisplay.grid.setRowMinimumHeight(4, self.secondDisplay.minimum_height + HEIGHT_FAMILY * self.secondDisplay.percent_height / 6)
                    self.secondDisplay.grid.setRowMinimumHeight(5, self.secondDisplay.minimum_height + HEIGHT_FAMILY * self.secondDisplay.percent_height / 6)
                if HEIGHT_FAMILY == -5:
                    '''
                    self.famRight.setVisible(True)
                    self.famLeft.setVisible(True)
                    self.grid.addWidget(self.famRight, 0, 0,  6, 34)
                    self.grid.addWidget(self.famLeft,  0, 34, 6, 34)
                    '''
                    if self.desk2.numScreens() != 1:
                        self.secondDisplay.fam_red.setVisible(True)
                        self.secondDisplay.fam_blue.setVisible(True)
                        self.secondDisplay.grid.addWidget(self.secondDisplay.fam_red,  0, 34, 6, 34)
                        self.secondDisplay.grid.addWidget(self.secondDisplay.fam_blue, 0,  0, 6, 34)
        elif i == 1:
            if HEIGHT_FAMILY > -6:
                HEIGHT_FAMILY -= 1
                if HEIGHT_FAMILY != -6:
                    '''
                    self.grid.setRowMinimumHeight(0, self.minimum_height + HEIGHT_FAMILY * self.percent_height / 6)
                    self.grid.setRowMinimumHeight(1, self.minimum_height + HEIGHT_FAMILY * self.percent_height / 6)
                    self.grid.setRowMinimumHeight(2, self.minimum_height + HEIGHT_FAMILY * self.percent_height / 6)
                    self.grid.setRowMinimumHeight(3, self.minimum_height + HEIGHT_FAMILY * self.percent_height / 6)
                    self.grid.setRowMinimumHeight(4, self.minimum_height + HEIGHT_FAMILY * self.percent_height / 6)
                    self.grid.setRowMinimumHeight(5, self.minimum_height + HEIGHT_FAMILY * self.percent_height / 6)
                    '''
                    if self.desk2.numScreens() != 1:
                        self.secondDisplay.grid.setRowMinimumHeight(0, self.secondDisplay.minimum_height + HEIGHT_FAMILY * self.secondDisplay.percent_height / 6)
                        self.secondDisplay.grid.setRowMinimumHeight(1, self.secondDisplay.minimum_height + HEIGHT_FAMILY * self.secondDisplay.percent_height / 6)
                        self.secondDisplay.grid.setRowMinimumHeight(2, self.secondDisplay.minimum_height + HEIGHT_FAMILY * self.secondDisplay.percent_height / 6)
                        self.secondDisplay.grid.setRowMinimumHeight(3, self.secondDisplay.minimum_height + HEIGHT_FAMILY * self.secondDisplay.percent_height / 6)
                        self.secondDisplay.grid.setRowMinimumHeight(4, self.secondDisplay.minimum_height + HEIGHT_FAMILY * self.secondDisplay.percent_height / 6)
                        self.secondDisplay.grid.setRowMinimumHeight(5, self.secondDisplay.minimum_height + HEIGHT_FAMILY * self.secondDisplay.percent_height / 6)
                else:
                    '''
                    self.grid.setRowMinimumHeight(0, 0)
                    self.grid.setRowMinimumHeight(1, 0)
                    self.grid.setRowMinimumHeight(2, 0)
                    self.grid.setRowMinimumHeight(3, 0)
                    self.grid.setRowMinimumHeight(4, 0)
                    self.grid.setRowMinimumHeight(5, 0)
                    self.famRight.setVisible(False)
                    self.famLeft.setVisible(False)
                    self.grid.removeWidget(self.famRight)
                    self.grid.removeWidget(self.famLeft)
                    '''
                    if self.desk2.numScreens() != 1:
                        self.secondDisplay.grid.setRowMinimumHeight(0, 0)
                        self.secondDisplay.grid.setRowMinimumHeight(1, 0)
                        self.secondDisplay.grid.setRowMinimumHeight(2, 0)
                        self.secondDisplay.grid.setRowMinimumHeight(3, 0)
                        self.secondDisplay.grid.setRowMinimumHeight(4, 0)
                        self.secondDisplay.grid.setRowMinimumHeight(5, 0)
                        self.secondDisplay.fam_red.setVisible(False)
                        self.secondDisplay.fam_blue.setVisible(False)
                        self.secondDisplay.grid.removeWidget(self.secondDisplay.fam_red)
                        self.secondDisplay.grid.removeWidget(self.secondDisplay.fam_blue)

        elif i == 2:
            if HEIGHT_REGION < 5:
                HEIGHT_REGION += 1
                '''
                self.grid.setRowMinimumHeight(37, self.minimum_height + HEIGHT_REGION * self.percent_height / 5)
                self.grid.setRowMinimumHeight(38, self.minimum_height + HEIGHT_REGION * self.percent_height / 5)
                self.grid.setRowMinimumHeight(39, self.minimum_height + HEIGHT_REGION * self.percent_height / 5)
                self.grid.setRowMinimumHeight(40, self.minimum_height + HEIGHT_REGION * self.percent_height / 5)
                self.grid.setRowMinimumHeight(41, self.minimum_height + HEIGHT_REGION * self.percent_height / 5)
                '''
                if self.desk2.numScreens() != 1:
                    self.secondDisplay.grid.setRowMinimumHeight(37, self.secondDisplay.minimum_height + HEIGHT_REGION * self.secondDisplay.percent_height / 5)
                    self.secondDisplay.grid.setRowMinimumHeight(38, self.secondDisplay.minimum_height + HEIGHT_REGION * self.secondDisplay.percent_height / 5)
                    self.secondDisplay.grid.setRowMinimumHeight(39, self.secondDisplay.minimum_height + HEIGHT_REGION * self.secondDisplay.percent_height / 5)
                    self.secondDisplay.grid.setRowMinimumHeight(40, self.secondDisplay.minimum_height + HEIGHT_REGION * self.secondDisplay.percent_height / 5)
                    self.secondDisplay.grid.setRowMinimumHeight(41, self.secondDisplay.minimum_height + HEIGHT_REGION * self.secondDisplay.percent_height / 5)
                if HEIGHT_REGION == -5:
                    '''
                    self.regLeft.setVisible(True)
                    self.regRight.setVisible(True)
                    self.grid.addWidget(self.regRight,          37, 0, 5, 34)
                    self.grid.addWidget(self.regLeft,           37, 34, 5, 34)
                    
                    self.flag_red.setVisible(True)
                    self.flag_blue.setVisible(True)
                    self.grid.addWidget(self.flag_red,          29, 14, 8, 10)
                    self.grid.addWidget(self.flag_blue,         29, 44, 8, 10)

                    self.grid.removeWidget(self.NP_left)
                    self.grid.removeWidget(self.NP_right)
                    self.grid.addWidget(self.NP_left,           24, 19, 5, 5)
                    self.grid.addWidget(self.NP_right,          24, 44, 5, 5)
                    
                    self.grid.removeWidget(self.NV_left)
                    self.grid.removeWidget(self.NV_right)
                    self.grid.addWidget(self.NV_left,           24, 14, 5, 5)
                    self.grid.addWidget(self.NV_right,          24, 49, 5, 5)
                    '''
                    if self.desk2.numScreens() != 1:
                        self.secondDisplay.reg_blue.setVisible(True)
                        self.secondDisplay.reg_red.setVisible(True)
                        self.secondDisplay.grid.addWidget(self.secondDisplay.reg_red,       37, 34, 5, 34)
                        self.secondDisplay.grid.addWidget(self.secondDisplay.reg_blue,      37,  0, 5, 34)
                        
                        self.secondDisplay.flag_red.setVisible(True)
                        self.secondDisplay.flag_blue.setVisible(True)
                        self.secondDisplay.grid.addWidget(self.secondDisplay.flag_red,      29, 14, 8, 10)
                        self.secondDisplay.grid.addWidget(self.secondDisplay.flag_blue,     29, 44, 8, 10)

                        self.secondDisplay.grid.removeWidget(self.secondDisplay.NP_left)
                        self.secondDisplay.grid.removeWidget(self.secondDisplay.NP_right)
                        self.secondDisplay.grid.addWidget(self.secondDisplay.NP_left,       24, 44, 5, 5)
                        self.secondDisplay.grid.addWidget(self.secondDisplay.NP_right,      24, 19, 5, 5)
                        
                        self.secondDisplay.grid.removeWidget(self.secondDisplay.NV_left)
                        self.secondDisplay.grid.removeWidget(self.secondDisplay.NV_right)
                        self.secondDisplay.grid.addWidget(self.secondDisplay.NV_left,       24, 49, 5, 5)
                        self.secondDisplay.grid.addWidget(self.secondDisplay.NV_right,      24, 14, 5, 5)
                    
        else:
            if HEIGHT_REGION > -6:
                HEIGHT_REGION -= 1
                if HEIGHT_REGION != -6:
                    '''
                    self.grid.setRowMinimumHeight(37, self.minimum_height + HEIGHT_REGION * self.percent_height / 5)
                    self.grid.setRowMinimumHeight(38, self.minimum_height + HEIGHT_REGION * self.percent_height / 5)
                    self.grid.setRowMinimumHeight(39, self.minimum_height + HEIGHT_REGION * self.percent_height / 5)
                    self.grid.setRowMinimumHeight(40, self.minimum_height + HEIGHT_REGION * self.percent_height / 5)
                    self.grid.setRowMinimumHeight(41, self.minimum_height + HEIGHT_REGION * self.percent_height / 5)
                    '''
                    if self.desk2.numScreens() != 1:
                        self.secondDisplay.grid.setRowMinimumHeight(37, self.secondDisplay.minimum_height + HEIGHT_REGION * self.secondDisplay.percent_height / 5)
                        self.secondDisplay.grid.setRowMinimumHeight(38, self.secondDisplay.minimum_height + HEIGHT_REGION * self.secondDisplay.percent_height / 5)
                        self.secondDisplay.grid.setRowMinimumHeight(39, self.secondDisplay.minimum_height + HEIGHT_REGION * self.secondDisplay.percent_height / 5)
                        self.secondDisplay.grid.setRowMinimumHeight(40, self.secondDisplay.minimum_height + HEIGHT_REGION * self.secondDisplay.percent_height / 5)
                        self.secondDisplay.grid.setRowMinimumHeight(41, self.secondDisplay.minimum_height + HEIGHT_REGION * self.secondDisplay.percent_height / 5)
                else:
                    '''
                    self.grid.setRowMinimumHeight(37, 0)
                    self.grid.setRowMinimumHeight(38, 0)
                    self.grid.setRowMinimumHeight(39, 0)
                    self.grid.setRowMinimumHeight(40, 0)
                    self.grid.setRowMinimumHeight(41, 0)
                    self.regLeft.setVisible(False)
                    self.regRight.setVisible(False)
                    self.grid.removeWidget(self.regLeft)
                    self.grid.removeWidget(self.regRight)
                    
                    self.grid.removeWidget(self.flag_red)
                    self.grid.removeWidget(self.flag_blue)
                    self.flag_red.setVisible(False)
                    self.flag_blue.setVisible(False)
                    
                    self.grid.removeWidget(self.NP_left)
                    self.grid.removeWidget(self.NP_right)
                    self.grid.addWidget(self.NP_left,           28, 19, 5, 5)
                    self.grid.addWidget(self.NP_right,          28, 44, 5, 5)

                    self.grid.removeWidget(self.NV_left)
                    self.grid.removeWidget(self.NV_right)
                    self.grid.addWidget(self.NV_left,           28, 14, 5, 5)
                    self.grid.addWidget(self.NV_right,          28, 49, 5, 5)
                    '''
                    if self.desk2.numScreens() != 1:
                        self.secondDisplay.grid.setRowMinimumHeight(37, 0)
                        self.secondDisplay.grid.setRowMinimumHeight(38, 0)
                        self.secondDisplay.grid.setRowMinimumHeight(39, 0)
                        self.secondDisplay.grid.setRowMinimumHeight(40, 0)
                        self.secondDisplay.grid.setRowMinimumHeight(41, 0)
                        self.secondDisplay.reg_blue.setVisible(False)
                        self.secondDisplay.reg_red.setVisible(False)
                        self.secondDisplay.grid.removeWidget(self.secondDisplay.reg_blue)
                        self.secondDisplay.grid.removeWidget(self.secondDisplay.reg_red)
                        
                        self.secondDisplay.grid.removeWidget(self.secondDisplay.flag_red)
                        self.secondDisplay.grid.removeWidget(self.secondDisplay.flag_blue)
                        self.secondDisplay.flag_red.setVisible(False)
                        self.secondDisplay.flag_blue.setVisible(False)
                        
                        self.secondDisplay.grid.removeWidget(self.secondDisplay.NP_left)
                        self.secondDisplay.grid.removeWidget(self.secondDisplay.NP_right)
                        self.secondDisplay.grid.addWidget(self.secondDisplay.NP_left,           28, 44, 5, 5)
                        self.secondDisplay.grid.addWidget(self.secondDisplay.NP_right,          28, 19, 5, 5)

                        self.secondDisplay.grid.removeWidget(self.secondDisplay.NV_left)
                        self.secondDisplay.grid.removeWidget(self.secondDisplay.NV_right)
                        self.secondDisplay.grid.addWidget(self.secondDisplay.NV_left,           28, 49, 5, 5)
                        self.secondDisplay.grid.addWidget(self.secondDisplay.NV_right,          28, 14, 5, 5)
        self.updateScreen()
        
    def setFrameWidth(self, f):
        self.sek.setLineWidth(f / 2)
        if self.desk2.numScreens() != 1:
            self.secondDisplay.sek.setLineWidth(f / 2)
        if self.formView.rbView1.isChecked():
            self.ball_right.setViewStyle(0, f)
            self.ball_left.setViewStyle(0,  f)
            self.akt_right.setViewStyle(0,  f)
            self.akt_left.setViewStyle(0,   f)
            if self.desk2.numScreens() != 1:
                self.secondDisplay.ball_right.setViewStyle(0, f)
                self.secondDisplay.ball_left.setViewStyle(0,  f)
                self.secondDisplay.akt_right.setViewStyle(0,  f)
                self.secondDisplay.akt_left.setViewStyle(0,   f)
        elif self.formView.rbView2.isChecked():
            self.ball_right.setViewStyle(1, f)
            self.ball_left.setViewStyle(2,  f)
            self.akt_right.setViewStyle(1,  f)
            self.akt_left.setViewStyle(2,   f)
            if self.desk2.numScreens() != 1:
                self.secondDisplay.ball_right.setViewStyle(1, f)
                self.secondDisplay.ball_left.setViewStyle(2,  f)
                self.secondDisplay.akt_right.setViewStyle(1,  f)
                self.secondDisplay.akt_left.setViewStyle(2,   f)
        else:
            self.ball_right.setViewStyle(3, f)
            self.ball_left.setViewStyle(4,  f)
            self.akt_right.setViewStyle(3,  f)
            self.akt_left.setViewStyle(4,   f)
            if self.desk2.numScreens() != 1:
                self.secondDisplay.ball_right.setViewStyle(3, f)
                self.secondDisplay.ball_left.setViewStyle(4,  f)
                self.secondDisplay.akt_right.setViewStyle(3,  f)
                self.secondDisplay.akt_left.setViewStyle(4,   f)
        self.updateScreen()
        
    def closeEvent(self, event):
        if self.desk2.numScreens()==2:
            self.secondDisplay.close()
        self.udpClient.stopProcess()
        self.tcpServer.stopProcess()
        self.thr.quit()
        self.tcpThread.quit()
        self.thr.wait()
        self.tcpThread.wait()
        
    def paintEvent(self,e):
        pn = QtGui.QPainter(self)
        pn.begin(self)
        pn.setPen(QtCore.Qt.NoPen)
        if self.View == 0:
            pn.setBrush(QtCore.Qt.red)
            pn.drawRect(0, 0, self.width() / 2, self.height())
            pn.setBrush(QtCore.Qt.blue)
            pn.drawRect(self.width() / 2, 0, self.width() / 2, self.height())
        else:
            pn.setBrush(QtCore.Qt.black)
            pn.drawRect(0, 0, self.width(), self.height())
        pn.end()
      
    def sep(self, fam):
        f = fam.split()
        fm = ''
        for i in f:
            fl =True
            for j in i:
                if not j.isupper():
                    if (j != "'") and (j != "-"):
                        fl = False
            if fl:
                fm = fm + ' ' + i
        return fm
    
    def family(self):
        #QtGui.QApplication.beep()
        if not self.w.isVisible():
            self.w.show()
        else:
            self.w.hide()
    def family_blue(self, stt, x):
        try:
            self.str_blue = stt
            if not stt == '-':
                stt=stt.split(';')
                self.regLeft.text(str.upper(stt[1]))#########################################################################
                #if self.desk2.numScreens()==2:
                #    self.secondDisplay.reg_blue.text(str.upper(stt[1]))
                #self.tr.rb = stt[1]
                stt2=stt[0].split()
                self.famLeft.text(self.sep(str.upper(stt2[0]) + ' ' + stt2[1]))##########################################################
                #if self.desk2.numScreens()==2:
                #   self.secondDisplay.fam_blue.text(self.sep(str.upper(stt2[0]) + ' ' + stt2[1]))
                #self.tr.fb = stt[0]
                path = r"flags/"
                #path = path + str.upper(stt[1]) + ".svg"
                path = path + stt[1] + ".png"
                if os.path.exists(path):
                    self.flag.load(path)
                    self.flag_blue.setPixmap(self.flag.scaled(self.flag_blue.size()))
                    if self.desk2.numScreens()==2:
                        self.secondDisplay.flag_blue.setPixmap(self.flag.scaled(self.flag_blue.size()))
                else:
                    self.flag_blue.clear()
                    if self.desk2.numScreens()==2:
                        self.secondDisplay.flag_blue.clear()
            else:
                self.famLeft.text('')
                self.regLeft.text('')
                self.flag_blue.clear()
                if self.desk2.numScreens()==2:
                    #self.secondDisplay.fam_blue.text('')
                    #self.secondDisplay.reg_blue.text('')
                    self.secondDisplay.flag_blue.clear()
        except:
            pass
          
    def family_red(self, x, stt):
        try:
            self.str_red = stt
            if not stt == '-':
                stt=stt.split(';')
                self.regRight.text(str.upper(stt[1]))#################################################################
                #if self.desk2.numScreens()==2:
                #    self.secondDisplay.reg_red.text(str.upper(stt[1]))
                #self.tr.rr = stt[1]
                stt2=stt[0].split()
                self.famRight.text(self.sep(str.upper(stt2[0]) + ' ' + stt2[1]))################################################
                #if self.desk2.numScreens()==2:
                #    self.secondDisplay.fam_red.text(self.sep(str.upper(stt2[0]) + ' ' + stt2[1]))
                #self.tr.fr = stt[0]
                path = r"flags/"
                path = path + stt[1] + ".png"
                if os.path.exists(path):
                    self.flag.load(path)
                    self.flag_red.setPixmap(self.flag.scaled(self.flag_red.size()))
                    if self.desk2.numScreens()==2:
                        self.secondDisplay.flag_red.setPixmap(self.flag.scaled(self.flag_red.size()))
                else:
                    self.flag_red.clear()
                    if self.desk2.numScreens()==2:
                        self.secondDisplay.flag_red.clear()
            else:
                self.famRight.text('')
                self.regRight.text('')
                self.flag_red.clear()
                if self.desk2.numScreens()==2:
                    self.secondDisplay.flag_red.clear()
                    self.secondDisplay.reg_red.text('')
                    #self.secondDisplay.fam_red.text('')
        except:
            pass
        
    def weight(self, w):
        #self.tr.w = w
        pass
                
    def plu_red(self):
        if self.plus_red.getText() == "+":
            self.plus_red.setData("")
        elif self.plus_blue.getText() == "":
            self.plus_red.setData("+")
        
    def plu_blue(self):
        if self.plus_blue.getText() == "+":
            self.plus_blue.setData("")
        elif self.plus_red.getText() == "":
            self.plus_blue.setData("+")
        
    def stroka(self,si,st):
        if si < 2:
            pass
        else:
            pass
        
    def sound(self):
        self.thread_sound.start()
    
    def sbros(self):
        if not self.sek.fl_state:
            self.form_vis = 1
            self.sek_left.clearTimer()
            self.sek_right.clearTimer()
            self.sek_left_TV.clearTimer()
            self.sek_right_TV.clearTimer()
            self.sek.clearTimer()
            self.ball_left.sbros()
            self.ball_right.sbros()
            self.akt_left.sbros()
            self.akt_right.sbros() 
            self.plus_red.setData("")
            self.plus_blue.setData("")
            #########################################
            '''
            if self.desk2.numScreens() == 2:
                self.secondDisplay.sek_left.clearTimer()
                self.secondDisplay.sek_right.clearTimer()
                self.secondDisplay.sek_left_TV.clearTimer()
                self.secondDisplay.sek_right_TV.clearTimer()
                self.secondDisplay.sek.clearTimer()
                self.secondDisplay.ball_left.sbros()
                self.secondDisplay.ball_right.sbros()
                self.secondDisplay.akt_left.sbros()
                self.secondDisplay.akt_right.sbros() 
                self.secondDisplay.plus_left.setVisible(False)
                self.secondDisplay.plus_right.setVisible(False)
            '''
            #######################################################
            sss = ''.join(self.ves)
            self.pl_l = ' '
            self.pl_r = ' '
            self.NV_left.sbros()
            self.NV_right.sbros()
            self.NP_left.sbros()
            self.NP_right.sbros()
            #################################################
            if self.desk2.numScreens()==2:
                self.secondDisplay.NV_left.sbros()
                self.secondDisplay.NV_right.sbros()
                self.secondDisplay.NP_left.sbros()
                self.secondDisplay.NP_right.sbros()

    def screenshot(self):
        if not self.screen.isVisible():
            self.screen.show()
        else:
            self.screen.hide()
        self.updateScreen()
          
    def updateScreen(self):
        if self.screen.isVisible():
            pm = QtGui.QPixmap.grabWidget(self.secondDisplay)
            pm.scaled(self.screen.width(), self.screen.height())
            self.screen.setPixmap(pm.scaled(self.screen.size()))
    ###################################################################################
							#upravlenie vremenem          
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            '''
            self.FileStart.open(QtCore.QFile.WriteOnly)

            out = QtCore.QTextStream(self.FileStart)
            out << self.famRight.getText() << "\n"
            out << self.famLeft.getText() << "\n"
            out << self.ball_right.text() << "\n"
            out << self.ball_left.text() << "\n"
            if self.plus_red.getText() == "+":
                out << "1" << "\n"
            elif self.plus_blue.getText() == "+":
                out << "2" << "\n"
            else:
                out << "0" << "\n"
            
            out << self.kat.text() << "\n"
            out << self.akt_right.text() << "\n"
            out << self.akt_left.text() << "\n"
            out << self.NV_right.text() << "\n"
            out << self.NP_right.text() << "\n"
            out << self.NP_left.text() << "\n"
            out << self.NV_left.text() << "\n"
            out << self.sek.getLastTime() << "\n"
            out << self.regRight.getText() << "\n"
            out << self.regLeft.getText()

            self.FileStart.close()
            '''
            QtGui.QApplication.closeAllWindows()
        
        elif e.key() ==  QtCore.Qt.Key_Backspace:###########################################################################
            self.sbros()
        
        elif e.key() == QtCore.Qt.Key_Up:
            self.changeSize(0)
            self.updateScreen()
        elif e.key() == QtCore.Qt.Key_Down:
            self.changeSize(1)
            self.updateScreen()
        elif e.key() == QtCore.Qt.Key_Right:
            self.changeSize(2)
            self.updateScreen()
        elif e.key() == QtCore.Qt.Key_Left:
            self.changeSize(3)
            self.updateScreen()
            
        elif e.key() == QtCore.Qt.Key_Space:
            self.fightTime()
        elif e.key() == QtCore.Qt.Key_Z:
            self.parter_red()
        elif e.key() == QtCore.Qt.Key_X:
            self.parter_blue()
        elif e.key() == QtCore.Qt.Key_A:
            self.t_red()
        elif e.key() == QtCore.Qt.Key_S:
            self.t_blue()
        
            '''
            e = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonPress, QtCore.QPoint(5, 5),
                                  QtCore.Qt.LeftButton, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
            QtCore.QCoreApplication.sendEvent(self.btnTime, e)
            '''
        #return QtCore.QEvent(e)
###################################################################################       
app = QtGui.QApplication(sys.argv)
qb = GridLayout2()
qb.show()
sys.exit(app.exec_())

