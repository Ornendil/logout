#!/usr/bin/python3
# coding: utf-8

import locale
import subprocess
import sys
from datetime import datetime, timedelta
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsScene, QGraphicsView, QLabel, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPolygonF, QPolygon, QPen, QColor, QBrush

# When to display countdown (in seconds)
idleCountdownShow = 60

# When to log off (in seconds)
idleCountdownEnd = 60 * 6

# Språket til innlogget bruker
spraak = locale.getlocale()
if 'nb_NO' in spraak:
    logoutButtonText = 'Logg ut og slett alt'
    inactiveUserText = 'Inaktiv bruker. Logger ut om '
    activeUserText = 'Logget inn i '
else:
    logoutButtonText = 'Logout and delete everything'
    inactiveUserText = 'Inactive user. Logging out in '
    activeUserText = 'Logged in for '

class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # Get time app was started
        self.startTime = datetime.now()

        # Get screen dimensions and set window dimensions
        screen = app.primaryScreen()
        size = screen.size()
        self.winWidth = 500
        self.winHeight = 30
        left = int((size.width() / 2) - (self.winWidth / 2))
        self.setGeometry(left,0,self.winWidth,self.winHeight + 5)

        # self.setWindowOpacity(0.9)
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.Tool |
            Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Make non-square background
        self.scene = QGraphicsScene()
        self.polygon = self.scene.addPolygon(
            QPolygonF(
                QPolygon(
                    [
                        QPoint(0,-1),
                        QPoint(self.winHeight - 1,self.winHeight - 2),
                        QPoint(self.winWidth - self.winHeight, self.winHeight - 2),
                        QPoint(self.winWidth, -1)
                    ]
                )
            ),
            QPen(QColor(80,80,80,255), 1, Qt.SolidLine),
            QBrush(QColor(50,85,164,240))
        )
        effect = QGraphicsDropShadowEffect()
        effect.setOffset(0, 1)
        effect.setBlurRadius(10)
        self.polygon.setGraphicsEffect(effect)

        self.view = QGraphicsView(self.scene, self)
        self.view.move(0, 0)
        self.view.setAlignment(Qt.AlignTop)
        self.view.setFixedSize(self.winWidth, self.winHeight + 5)
        self.view.setStyleSheet("background: transparent; border: 0px")
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Set label
        self.guestLabel = QLabel(self)
        self.guestLabel.setText('Gjestebruker')
        self.guestLabel.setStyleSheet('background-color: transparent; color: white')
        self.guestLabel.resize(100,self.winHeight)
        self.guestLabel.move(40, -1)

        # set clock
        self.clockLabel = QLabel(self)
        self.clockLabel.setText(activeUserText + self.secondsToClock(datetime.now() - self.startTime))
        self.clockLabel.setStyleSheet('background-color: transparent; color: white')
        self.clockLabel.resize(400, self.winHeight)
        self.clockLabel.setAlignment(Qt.AlignCenter)
        self.clockLabel.move(35, -1)

        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        # Logg ut-knapp
        self.loggUtKnapp = QPushButton('Logg ut', self)
        self.loggUtKnapp.setToolTip('Logger deg ut og sletter alle dokmenter du har lagret.')
        self.loggUtKnapp.resize(100, int(self.winHeight / 1.5))
        self.loggUtKnapp.move(360, int(self.winHeight / 6) - 1)
        self.loggUtKnapp.clicked.connect(self.logOut)

    # Konverter sekunder til timer:minutter:sekunder
    def secondsToClock(self, td):
        totalMinute, second = divmod(td.seconds, 60)
        hour, minute = divmod(totalMinute, 60)
        if hour >= 1:
            return f"{hour:02}:{minute:02}:{second:02}"
        else:
            return f"{minute:02}:{second:02}"
    
    def showTime(self):
        idleTime = int(int(subprocess.getoutput('xprintidle')) / 1000)
        idleTimeLeft = idleCountdownEnd - idleTime
        idleClock = self.secondsToClock(timedelta(seconds=idleTimeLeft))
        clock = self.secondsToClock(datetime.now() - self.startTime)
        if idleTime >= idleCountdownEnd:
            self.timer.stop()
            self.logOut()
        if idleTime >= idleCountdownShow:
            self.clockLabel.setText(inactiveUserText + idleClock)
            self.polygon.setBrush(QColor(254, 74, 73, 240))
        else:
            self.clockLabel.setText(activeUserText + clock)
            self.polygon.setBrush(QColor(50, 85, 164, 240))

    # Funksjonen som logger ut brukeren
    def logOut(self):
        subprocess.run('cinnamon-session-quit --logout --force', shell=True)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
