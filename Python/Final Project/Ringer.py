from PyQt4 import QtGui, QtCore
import sys, os, platform

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        #Main Window
        super(MainWindow, self).__init__()
        self.appName = "Ringer"
        self.version = "1.00"
        self.setWindowTitle(self.appName)
        self.setWindowIcon(QtGui.QIcon('./icons/MainIcon.ico'))
        self.resize(755, 515)
        self.move(QtGui.QApplication.desktop().screen().rect().center() - self.rect().center())
        self.statusBar()

        self.checkRoot()
        # Widget
        self.centralwidget = QtGui.QWidget()
        self.setCentralWidget(self.centralwidget)

        #main menu
        importFileMenu = QtGui.QAction("&Import File", self)
        importFileMenu.setShortcut("Ctrl+O")
        importFileMenu.setStatusTip('Import file to Ringer')
        importFileMenu.setToolTip('Import file to Ringer')
        importFileMenu.setIcon(QtGui.QIcon('./icons/AddFile.ico'))
        importFileMenu.triggered.connect(self.import_file)

        importFolderMenu = QtGui.QAction("&Import Folder", self)
        #importFolderMenu.setShortcut("Ctrl+O")
        importFolderMenu.setStatusTip('Import folder to Ringer')
        importFolderMenu.setToolTip('Import folder to Ringer')
        importFolderMenu.setIcon(QtGui.QIcon('./icons/AddFolder.ico'))
        importFolderMenu.triggered.connect(self.Open_File)

        quitMenu = QtGui.QAction("&Quit", self)
        quitMenu.setShortcut("Ctrl+Q")
        quitMenu.setIcon(QtGui.QIcon('./icons/Exit.ico'))
        quitMenu.setStatusTip('Quit from application')
        quitMenu.setToolTip('Quit from application')
        quitMenu.triggered.connect(self.quit_app)

        Checkupdate = QtGui.QAction("&Check Update", self)
        Checkupdate.setShortcut("Ctrl+U")
        Checkupdate.setStatusTip('Check for updates')
        Checkupdate.setToolTip('Check for updates')
        Checkupdate.triggered.connect(self.Open_File)

        aboutMenu1 = QtGui.QAction("&About", self)
        aboutMenu1.setShortcut("Ctrl+A")
        aboutMenu1.setStatusTip('About this application')
        aboutMenu1.setToolTip('About this application')
        aboutMenu1.setIcon(QtGui.QIcon('./icons/About.ico'))
        aboutMenu1.triggered.connect(self.aboutApp)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(importFileMenu)
        fileMenu.addAction(importFolderMenu)
        fileMenu.addSeparator()
        fileMenu.addAction(quitMenu)

        aboutMenu = mainMenu.addMenu('&About')
        aboutMenu.addAction(Checkupdate)
        aboutMenu.addSeparator()
        aboutMenu.addAction(aboutMenu1)

        #import file label
        importLabel = QtGui.QLabel("Import Files", self)
        importLabel.setGeometry(QtCore.QRect(95, 30, 281, 31))
        importLabel.setStyleSheet("font: bold 13pt ARIEL")

        # check list
        self.importList = QtGui.QListWidget(self.centralwidget)
        self.importList.setGeometry(QtCore.QRect(10, 40, 281, 411))
        self.importList.setObjectName("importList")

        #import file btn
        importFilebtn = QtGui.QPushButton("Import File", self)
        importFilebtn.setGeometry(QtCore.QRect(10, 475, 91, 31))
        importFilebtn.setIcon(QtGui.QIcon('./icons/AddFile.ico'))
        importFilebtn.clicked.connect(self.import_file)

        #import folder
        importFolderbtn = QtGui.QPushButton("Import Folder", self)
        importFolderbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        importFolderbtn.setGeometry(QtCore.QRect(106, 475, 91, 31))
        importFolderbtn.setIcon(QtGui.QIcon('./icons/AddFolder.ico'))

        #clear list
        importFolderbtn = QtGui.QPushButton("Clear List", self)
        importFolderbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        importFolderbtn.setGeometry(QtCore.QRect(202, 475, 91, 31))
        importFolderbtn.setIcon(QtGui.QIcon('./icons/Clear.ico'))

        #ringtone btn
        QtGui.QToolButton
        ringtonebtn = QtGui.QToolButton(self)
        ringtonebtn.setText("Ringtone Maker")
        ringtonebtn.setGeometry(QtCore.QRect(301, 60, 153, 44))
        ringtonebtn.setIcon(QtGui.QIcon('./icons/Ringtone.ico'))
        ringtonebtn.setIconSize(QtCore.QSize(48, 39))
        ringtonebtn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        ringtonebtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        #ringtonebtn.setStyleSheet("QToolButton {background-color:transparent;}")

        # move
        movebtn = QtGui.QToolButton(self)
        movebtn.setText("Move Song")
        movebtn.setIcon(QtGui.QIcon('./icons/LeftArrow.ico'))
        movebtn.setGeometry(QtCore.QRect(301, 110, 153, 44))
        movebtn.setIconSize(QtCore.QSize(48, 39))
        movebtn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        movebtn.clicked.connect(QtCore.QCoreApplication.instance().quit)

        #move All
        moveAllbtn = QtGui.QToolButton(self)
        moveAllbtn.setText("Move All Songs")
        moveAllbtn.setGeometry(301, 160, 153, 44)
        moveAllbtn.setIcon(QtGui.QIcon('./icons/LeftArrow.ico'))
        moveAllbtn.setIconSize(QtCore.QSize(48, 39))
        moveAllbtn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        moveAllbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)

        # Play
        Playbtn = QtGui.QToolButton(self)
        Playbtn.setText("Play Songs")
        Playbtn.setGeometry(301, 210, 153, 44)
        Playbtn.setIcon(QtGui.QIcon('./icons/Play1.ico'))
        Playbtn.setIconSize(QtCore.QSize(48, 39))
        Playbtn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

       # Playbtn.clicked.connect(self.MediaFrame())

        # List file in Ringer label
        listLabel = QtGui.QLabel("List file in Ringer", self)
        listLabel.setGeometry(QtCore.QRect(540, 30, 281, 31))
        listLabel.setStyleSheet("font: bold 13pt ARIEL")

        # check list
        self.listFile = QtGui.QListWidget(self.centralwidget)
        self.listFile.setGeometry(QtCore.QRect(464, 40, 281, 411))
        self.listFile.setObjectName("listFile")

        # remove file btn
        importFilebtn = QtGui.QPushButton("Remove Song", self)
        importFilebtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        importFilebtn.setGeometry(QtCore.QRect(463, 475, 95, 31))
        importFilebtn.setIcon(QtGui.QIcon('./icons/DeleteFile.ico'))

        # remove all file
        importFolderbtn = QtGui.QPushButton("Remove All Songs", self)
        importFolderbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        importFolderbtn.setGeometry(QtCore.QRect(570, 475, 115, 31))
        importFolderbtn.setIcon(QtGui.QIcon('./icons/Delete.ico'))

        self.show()

    def check_os(self):
        return platform.system()

    def muzic_player(self):
        pass

    def Open_File(self):
        pass

    def import_file(self):
        if self.check_os() == "Windows":
            fileName = QtGui.QFileDialog.getOpenFileName(self, "Import File", "c:/users/zahi/Desktop/","MP3 File (*.mp3);;WMV File (*.WMV)")
            if fileName:
                    item = QtGui.QListWidgetItem()
                    item.setText(fileName)
                    item.setCheckState(QtCore.Qt.Unchecked)
                    self.importList.addItem(item)


        elif self.check_os() == "Linux":
            fileName = QtGui.QFileDialog.getOpenFileName(self, 'Import File', os.environ['HOME']+"/Desktop",
                                                                       "MP3 File (*.mp3);;WMV File (*.WMV)")
        else:
            fileName = QtGui.QFileDialog.getOpenFileName(self, 'Import File', "","MP3 File (*.mp3);;WMV File (*.WMV)")

    def quit_app(self):
        choice = QtGui.QMessageBox.question(self, 'Ringer!', "Do you really want to exit?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()

    def aboutApp(self):
        website = "##"
        email = "zachi40@gmail.com"
        license_link = "##"
        license_name = "Ringer"

        msgBox = QtGui.QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon('./icons/Mainicon.ico'))
        msgBox.setWindowTitle(self.tr("About " + self.appName))
        msgBox.setTextFormat(QtCore.Qt.RichText)
        msgBox.setIconPixmap(QtGui.QPixmap('./icons/About.ico'))
        msgBox.setText("<br>" +
                       self.appName +
                       " V" +
                       self.version +
                       "<br>" +
                       "&copy;2016 Zahi Ohana<br><br>" +
                       "<a href='{0}'>{0}</a><br><br>".format(website) +
                       "<a href='mailto:{0}'>{0}</a><br><br>".format(email) +
                       "License: <a href='{0}'>{1}</a>".format(license_link, license_name))
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.exec_()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def checkRoot(self):
        if self.check_os() == 'Linux':
           if not os.geteuid() == 0:
                msgBox = QtGui.QMessageBox()
                msgBox.setIcon(QtGui.QMessageBox.Critical)
                msgBox.setWindowIcon(QtGui.QIcon('./icons/Mainicon.ico'))
                msgBox.setWindowTitle(self.appName)
                msgBox.setText('You must run this app as Root user')
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
                msgBox.exec_()
                sys.exit()

def run():
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
run()