import socket, time, sqlite3
from PyQt4 import QtCore

class udpClient(QtCore.QObject):
    def __init__(self, mat, parent=None):
        QtCore.QObject.__init__(self, parent)
        self.process = True
        self.udpSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.udpSocket.settimeout(1)
        self.mat = mat
        self.addr = socket.gethostbyname(socket.gethostname())[:-3] + "255"
        self.port = int(mat) * 10000
        
        
    def run(self):
        while self.process:
            time.sleep(1)
            self.udpSocket.sendto(self.mat, (self.addr, self.port))
            try:
                data, addr = self.udpSocket.recvfrom(1024)
                if data == self.mat:
                    self.emit(QtCore.SIGNAL("conn"), addr[0], addr[1])
                else:
                    self.emit(QtCore.SIGNAL("conn"), "", "")
            except socket.timeout:
                self.emit(QtCore.SIGNAL("conn"), "", "")

    def stopProcess(self):
        self.process = False

class TcpServer(QtCore.QObject):
    def __init__(self, mat, parent=None):
        QtCore.QObject.__init__(self, parent)
        self.process = True
        #self.sock = socket.socket()
        #self.udpSocket.settimeout(1)
        #self.mat = mat
        #self.addr = socket.gethostbyname(socket.gethostname())[:-3] + "255"
        self.port = int(mat) * 1000
        
        
    def run(self):
        while self.process:
            #time.sleep(1)
            sock = socket.socket()
            try:              
                sock.bind( ("", self.port) )
                sock.listen(10)
                sock.settimeout(2)
                conn, addr = sock.accept()
                conn.settimeout(2)
                try:
                    data = conn.recv(16384)
                    d = data.decode()
                    dd = d.split("=")
                    rnd = dd[0]
                    rnd_name = dd[1]
                    ddd = dd[2].split("<")
                    con = sqlite3.connect('baza_in.db')
                    cur = con.cursor()
                    try:
                        sql = "SELECT * FROM rounds WHERE num_round = " + rnd
                        print("sql = ", sql)
                        cur.execute(sql)
                        s = cur.fetchall()
                        print("s = ", s, rnd, sql)
                        if s == []:
                            #print("rnd = ", rnd)
                            for each in ddd[1:]:
                                #print("ddd[1:] = ", each)
                                e = each.split(";")
                                #print("e = ", e)
                                #print("red = ", e[0], "blue = ", e[1], "n_red = ", e[2], "n_nlue = ", e[3])
                                sql = """INSERT INTO rounds
                                         (num_round, name_round,
                                          name_red, name_blue,
                                          note_red, note_blue, num_fight)
                                        VALUES (?, ?, ?, ?, ?, ?, ?)
                                      """
                                cur.execute(sql, (rnd, rnd_name, e[0], e[1], e[2], e[3], str(e[4])))
                                con.commit()
                                
                        conn.send(bytes(rnd, "utf-8"))
                    except sqlite3.DatabaseError as err:
                        print("error", err)
                    finally:
                        cur.close()
                        con.close()
                    #print("data = ", rnd, dd, ddd)
                except socket.timeout:
                    pass
                    #print("conn timeout")
                finally: conn.close()
            except socket.timeout:
                pass
                #print("sock timeout")

            finally: sock.close()
            

    def stopProcess(self):
        self.process = False
