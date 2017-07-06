#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import sys,os
import vlc, time
from mutagen import File
from tinytag import TinyTag
from PyQt4 import QtGui, QtCore

class Player(QtGui.QMainWindow):
    def __init__(self, master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.setWindowIcon(QtGui.QIcon('../icons/MainIcon.ico'))
        self.setWindowTitle("Ringer Player")
        self.resize(475, 182)
        self.setFixedSize(475, 182)
        self.move(QtGui.QApplication.desktop().screen().rect().center() - self.rect().center())
        self.setStyleSheet("QListWidget{background-color:transparent;}"
                           "QLineEdit{background-color:transparent;font: bold 12pt ARIEL;}"
                           "QPushButton{background-color:transparent;}"
                           )
        self.instance = vlc.Instance()
        self.mediaplayer = self.instance.media_player_new()
        self.is_pause = False
        self.path_songs = []

        self.createUI()
        self.load()

    def createUI(self):
        self.widget = QtGui.QWidget(self)
        self.setCentralWidget(self.widget)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.updateUI)

        self.diskImage = QtGui.QLabel(self)
        self.diskImage.setPixmap(QtGui.QPixmap('./icons/disk.png'))
        self.diskImage.setGeometry(QtCore.QRect(0, 0, 141, 71))
        self.diskImage.setScaledContents(True)

        self.songList = QtGui.QListWidget(self)
        self.songList.setGeometry(QtCore.QRect(140, 0, 336, 81))
        self.songList.setFrameShape(QtGui.QFrame.NoFrame)
        self.songList.setAutoScroll(True)
        self.songList.doubleClicked.connect(lambda :self.Play(self.songList.currentRow()))

        self.songTitle = QtGui.QLineEdit(self)
        self.songTitle.setGeometry(QtCore.QRect(0, 85, 474, 20))
        self.songTitle.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.songTitle.setFrame(False)
        self.songTitle.setReadOnly(True)

        self.positionslider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.positionslider.setGeometry(QtCore.QRect(5, 110, 465, 22))
        self.positionslider.setToolTip("Position")
        self.positionslider.setMaximum(1000)
        self.positionslider.setEnabled(False)
        self.positionslider.sliderMoved[int].connect(self.setPosition)

        self.songTime = QtGui.QLabel("0:00:00", self)
        self.songTime.setGeometry(QtCore.QRect(355, 126, 381, 22))
        self.songTime.setStyleSheet("font: bold 10pt ARIEL")

        self.gres = QtGui.QLabel("-", self)
        self.gres.setGeometry(QtCore.QRect(410, 126, 381, 22))
        self.gres.setStyleSheet("font: bold 10pt ARIEL")

        self.songTimeAll = QtGui.QLabel("0:00:00", self)
        self.songTimeAll.setGeometry(QtCore.QRect(420, 126, 381, 22))
        self.songTimeAll.setStyleSheet("font: bold 10pt ARIEL")

        self.prevSongs = QtGui.QPushButton(self)
        self.prevSongs.setGeometry(QtCore.QRect(0, 140, 54, 48))
        self.prevSongs.setIcon(QtGui.QIcon('./icons/player_prev.png'))
        self.prevSongs.setIconSize(QtCore.QSize(48, 39))
        self.prevSongs.clicked.connect(self.prevSong)

        self.pauseSongs = QtGui.QPushButton(self)
        self.pauseSongs.setGeometry(QtCore.QRect(59, 140, 54, 48))
        self.pauseSongs.setIcon(QtGui.QIcon('./icons/player_pause.png'))
        self.pauseSongs.setIconSize(QtCore.QSize(48, 39))
        self.pauseSongs.clicked.connect(self.pause)

        self.playSong = QtGui.QPushButton(self)
        self.playSong.setGeometry(QtCore.QRect(118, 140, 54, 48))
        self.playSong.setIcon(QtGui.QIcon('./icons/player_play.png'))
        self.playSong.setIconSize(QtCore.QSize(48, 39))
        self.playSong.clicked.connect(lambda :self.Play(self.songList.currentRow()))

        self.stopsong = QtGui.QPushButton(self)
        self.stopsong.setGeometry(QtCore.QRect(177, 140, 54, 48))
        self.stopsong.setIcon(QtGui.QIcon('./icons/player_stop.png'))
        self.stopsong.setIconSize(QtCore.QSize(48, 39))
        self.stopsong.clicked.connect(self.Stop)

        self.nextsong = QtGui.QPushButton(self)
        self.nextsong.setGeometry(QtCore.QRect(236, 140, 54, 48))
        self.nextsong.setIcon(QtGui.QIcon('./icons/player_next.png'))
        self.nextsong.setIconSize(QtCore.QSize(48, 39))
        self.nextsong.clicked.connect(self.nextSong)

        self.volumeslider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.volumeslider.setGeometry(QtCore.QRect(355, 155, 109, 22))
        self.volumeslider.setMaximum(100)
        self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
        self.volumeslider.setToolTip("Volume")
        self.volumeslider.valueChanged[int].connect(self.setVolume)

        self.muteVolume = QtGui.QLabel(self)
        self.muteVolume.setGeometry(QtCore.QRect(315, 150, 32, 32))
        self.muteVolume.setPixmap(QtGui.QPixmap('./icons/volume4.ico'))
        self.muteVolume.setScaledContents(True)
        self.muteVolume.mouseReleaseEvent = self.mute_Volume

    def load(self):
        with codecs.open("C:\Users\zahi\Dropbox\zahi\Extra\Python\Final Project\player\songlist.txt", encoding="cp1255") as lines:
            for line in lines:
                self.path_songs.append(line)
                item = QtGui.QListWidgetItem()
                item.setText(os.path.basename(line).strip().strip('.mp3').strip('.wav'))
                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.songList.addItem(item)
            #self.Play(self.path_songs[0])

    def updateUI(self):
        if not self.mediaplayer.is_playing():
            self.timer.stop()
        else:
            self.positionslider.setValue(self.mediaplayer.get_position() * 1000)
            self.songTime.setText(self.time_progres(self.mediaplayer.get_time()/1000))
            #if self.songTime.text() == self.songTimeAll.text():
            #   if self.nextsong.isEnabled() == False:
            #       self.Stop()
            #   else:
            #       self.nextSong()
            #elif (self.time_progres(self.mediaplayer.get_time() / 1000)) == (self.time_progres(self.mediaplayer.get_length() / 1000 - 1)):
            #    self.nextSong()

    def Play(self,song):
        if self.is_pause == True:
            self.mediaplayer.play()
            self.timer.start()
            self.is_pause = False
        else:
            self.mediaplayer.stop()
            self.mediaplayer = self.instance.media_player_new()
            self.song_file=self.path_songs[song].replace('\\','/').strip()
            self.media = self.instance.media_new(self.song_file)

            try:
                file = File(self.song_file)
                with open('./icons/diskimage.jpg', 'wb') as img:
                    img.write(file.tags['APIC:Cover Image'].data)
                self.diskImage.setPixmap(QtGui.QPixmap('./icons/diskimage.jpg'))
            except:
                self.diskImage.setPixmap(QtGui.QPixmap('./icons/disk.png'))
            self.media.get_mrl()
            self.mediaplayer.set_media(self.media)
            self.timer.start()
            self.songTitle.setText(self.media.get_meta(0).encode('utf-8').decode('utf-8').strip(".mp3").strip(".wav"))
            self.mediaplayer.play()
            time.sleep(1)
            if not self.mediaplayer.is_playing():
                    self.songTitle.setText("Could not open the file")
                    self.positionslider.setEnabled(False)
                    self.positionslider.setValue(0)
                    self.diskImage.setPixmap(QtGui.QPixmap('./icons/disk.png'))
            else:
                self.songTimeAll.setText(self.time_progres(self.mediaplayer.get_length() / 1000))
                self.positionslider.setEnabled(True)
                self.playSong.setEnabled(False)
                self.nextsong.setEnabled(True)
                self.songList.item(self.songList.currentRow()).setSelected(True)

    def Stop(self):
        self.mediaplayer.stop()
        self.playSong.setEnabled(True)
        self.positionslider.setValue(0)
        self.songTimeAll.setText("0:00:00")
        self.songTime.setText("0:00:00")
        self.positionslider.setEnabled(False)
        self.songTitle.setText("")
        self.diskImage.setPixmap(QtGui.QPixmap('./icons/disk.png'))

    def setPosition(self, position):
        self.mediaplayer.set_position(position / 1000.0)
        self.songTime.setText(self.time_progres(self.mediaplayer.get_time() / 1000))
        if self.songTime.text() == self.songTimeAll.text():
            if self.nextsong.isEnabled() == False:
                self.Stop()
            else:
                self.nextSong()
        elif (self.time_progres(self.mediaplayer.get_time() / 1000)) == (self.time_progres(self.mediaplayer.get_length() / 1000 - 1)):
                self.nextSong()

    def setVolume(self, Volume):
        self.mediaplayer.audio_set_volume(Volume)
        if Volume == 0:
            self.muteVolume.setPixmap(QtGui.QPixmap('./icons/volume1.ico'))
        elif Volume > 0 and Volume <= 30:
            self.muteVolume.setPixmap(QtGui.QPixmap('./icons/volume2.ico'))
        elif Volume > 30 and Volume < 80:
            self.muteVolume.setPixmap(QtGui.QPixmap('./icons/volume3.ico'))
        else:
            self.muteVolume.setPixmap(QtGui.QPixmap('./icons/volume4.ico'))

    def mute_Volume(self,event):
        if self.mediaplayer.audio_get_volume() == 0:
            self.volumeslider.setValue(50)
            self.mediaplayer.audio_set_volume(50)
            self.muteVolume.setPixmap(QtGui.QPixmap('./icons/volume3.ico'))
        else:
            self.mediaplayer.audio_set_volume(0)
            self.volumeslider.setValue(0)
            self.muteVolume.setPixmap(QtGui.QPixmap('./icons/volume1.ico'))

    def nextSong(self):
        songsindex = self.songList.currentRow() + 1
        if songsindex == self.songList.count():
            self.nextsong.setEnabled(False)
        else:
            self.songList.item(songsindex).setSelected(True)
            self.songList.setCurrentRow(songsindex)
            self.Play(songsindex)
            self.nextsong.setEnabled(True)
            self.prevSongs.setEnabled(True)

    def prevSong(self):
        songsindex = self.songList.currentRow() -1
        if songsindex == -1:
            self.prevSongs.setEnabled(False)
        else:
            self.songList.item(songsindex).setSelected(True)
            self.songList.setCurrentRow(songsindex)
            self.Play(songsindex)
            self.nextsong.setEnabled(True)
            self.prevSongs.setEnabled(True)

    def pause(self):
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.songTime.setText(self.time_progres(self.mediaplayer.get_time() / 1000))
            self.playSong.setEnabled(True)
            self.is_pause = True
        else:
            self.is_pause = False
            self.timer.start()
            self.mediaplayer.play()
            self.playSong.setEnabled(False)
            self.songTime.setText(self.time_progres(self.mediaplayer.get_time() / 1000))

    def time_progres(self,time):
        m, s = divmod(time, 60)
        h, m = divmod(m, 60)
        return ("%d:%02d:%02d" % (h, m, s))

    def info(self,song):

        title = self.tag.title + " - " +self.tag.artist


        return title

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    player = Player()
    player.show()
    sys.exit(app.exec_())
