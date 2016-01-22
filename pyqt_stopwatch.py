"""
Mini project for Introduction to Interactive Programming in Python utilizing PyQt5. Stopwatch: The Game.
Written on: 20/6/2015  
"""

import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton,
                             QFrame, QDesktopWidget, QLabel,
                             QCheckBox)
from PyQt5.QtCore import (Qt, QBasicTimer)
from PyQt5.QtGui import (QPainter,QColor, QFont)

class StopWatch(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.timer = QBasicTimer()
        self.counter = 0
        self.rt = False
        self.nstops = 0
        self.nsuccess = 0
        
        # Main window
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(100, 200, 300, 200)
        size = self.geometry()
        self.move(screen.width() - size.width() - 50,
                  50)
        self.setWindowTitle("Stopwatch")

        # Define controls
        startbtn = QPushButton("START", self)
        startbtn.move(10, 20)
        startbtn.clicked.connect(self.start_timer)

        stopbtn = QPushButton("STOP", self)
        stopbtn.move(10, 60)
        stopbtn.clicked.connect(self.stop_timer)

        resetbtn = QPushButton("RESET", self)
        resetbtn.move(10, 100)
        resetbtn.clicked.connect(self.reset_timer)

        self.counterlbl = QLabel(self.format_counter(),self)
        self.counterlbl.move(120,40)
        self.counterlbl.setFont(QFont("Helvetica", 40))

        self.scorelbl = QLabel("    ",self)
        self.scorelbl.move(230,150)
        self.scorelbl.setFont(QFont("Courier", 20))

        playcb = QCheckBox('Check this box to play reaction time',self)
        playcb.move(10,160)
        playcb.stateChanged.connect(self.toggle_rt)
        
        self.show()

    def format_counter(self):

        D = self.counter % 10
        C = (self.counter//10) % 10
        B = (self.counter//100) % 6
        A = self.counter // 600

        return str(A) + ":" + str(B) + str(C) + "." + str(D) 

    def start_timer(self):

        self.timer.start(100,self)

    def stop_timer(self):

        if self.timer.isActive():
            self.timer.stop()

        if self.rt:
            self.nstops += 1
            if self.counter % 10 == 0:
                self.nsuccess += 1
            self.scorelbl.setText(str(self.nsuccess) + "/" + str(self.nstops))            

    def reset_timer(self):

        self.timer.stop()
        self.counter = 0
        self.counterlbl.setText(self.format_counter())

        if self.rt:
            self.nstops = 0
            self.nsuccess = 0
            self.scorelbl.setText(str(self.nsuccess) + "/" + str(self.nstops))            

    def toggle_rt(self):

        self.rt = not self.rt

        self.nstops = 0
        self.nsuccess = 0

        if self.rt:
            self.scorelbl.setText(str(self.nsuccess) + "/" + str(self.nstops))
        else:
            self.scorelbl.setText("   ")

    def timerEvent(self, event):

        if event.timerId() == self.timer.timerId():
            self.counter += 1
            self.counterlbl.setText(self.format_counter())
           

if __name__ == '__main__':

    app = QApplication(sys.argv)
    sw = StopWatch()
    sys.exit(app.exec_())
                

    
