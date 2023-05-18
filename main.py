from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import QDialog

class Ui_MainWindow(object):
    #메인창 내용물
    def setupUi(self, MainWindow):
        #메인창 관련
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        MainWindow.setAnimated(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        #ps창 관련
        self.Psframe = QtWidgets.QFrame(self.centralwidget)
        self.Psframe.setGeometry(QtCore.QRect(410, 460, 371, 81))
        self.Psframe.setFrameShape(QtWidgets.QFrame.Box)
        self.Psframe.setObjectName("Psframe")
        self.PsTitle = QtWidgets.QLabel(self.Psframe)
        self.PsContents = QtWidgets.QLabel(self.Psframe)
        self.PsTitle.setGeometry(QtCore.QRect(10, 10, 91, 21))
        self.PsContents.setGeometry(QtCore.QRect(20, 30, 351, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        self.PsTitle.setFont(font)
        self.PsTitle.setObjectName("PsTitle")
        self.PsContents.setObjectName("PsContents")
        
        #검색창 관련
        self.SearchFrame = QtWidgets.QFrame(self.centralwidget)
        self.SearchFrame.setGeometry(QtCore.QRect(410, 10, 381, 51))
        self.SearchFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.SearchFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SearchFrame.setObjectName("SearchFrame")
        self.SearchEdit = QtWidgets.QLineEdit(self.SearchFrame)
        self.SearchEdit.setGeometry(QtCore.QRect(10, 10, 321, 31))
        self.SearchEdit.setObjectName("SearchEdit")
        self.SearchButton = QtWidgets.QPushButton(self.SearchFrame)
        self.SearchButton.setGeometry(QtCore.QRect(330, 10, 41, 31))
        icon = QtGui.QIcon()
        
        #검색 버튼에 아이콘 추가: 링크 맞춰서 넣으심 돼요
        icon.addPixmap(QtGui.QPixmap("TeamProjects/ClueIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.SearchButton.setIcon(icon)
        self.SearchButton.setObjectName("SearchButton")
        
        #탭 내용 정의 전 틀
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(410, 70, 381, 381))
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setObjectName("tabWidget")
        self.Tab1 = QtWidgets.QWidget()
        self.Tab1.setObjectName("Tab1")
        
        #스크롤바 관련
        self.scrollArea = QtWidgets.QScrollArea(self.Tab1)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 381, 351))
        self.scrollArea.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(False)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 358, 729))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        
        self.NameLabel1 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.NameLabel1.setGeometry(QtCore.QRect(10, 10, 361, 31))
        self.NameLabel2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.NameLabel2.setGeometry(QtCore.QRect(10, 180, 361, 31))
        self.NameLabel3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.NameLabel3.setGeometry(QtCore.QRect(10, 350, 361, 31))
        
        #로딩될 리뷰들 제목 나오는 큰 글씨
        font = QtGui.QFont()
        font.setFamily("한컴산뜻돋움")
        font.setPointSize(16)
        self.NameLabel1.setFont(font)
        self.NameLabel2.setFont(font)
        self.NameLabel3.setFont(font)
        self.NameLabel1.setObjectName("NameLabel1")
        self.NameLabel2.setObjectName("NameLabel2")
        self.NameLabel3.setObjectName("NameLabel3")
        
        #로딩될 리뷰들 내용 나오는 작은 글씨
        self.ContentLabel1 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.ContentLabel2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.ContentLabel3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.ContentLabel1.setGeometry(QtCore.QRect(20, 40, 351, 131))
        self.ContentLabel2.setGeometry(QtCore.QRect(20, 210, 341, 131))
        self.ContentLabel3.setGeometry(QtCore.QRect(20, 380, 321, 131))
        self.ContentLabel1.setObjectName("ContentLabel1")
        self.ContentLabel2.setObjectName("ContentLabel2")
        self.ContentLabel3.setObjectName("ContentLabel3")
        
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.tabWidget.addTab(self.Tab1, "")
        
        #탭2 추가
        self.Tab2 = QtWidgets.QWidget()
        self.Tab2.setObjectName("Tab2")
        self.tabWidget.addTab(self.Tab2, "")
        
        #지도 관련
        self.Map = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.Map.setGeometry(QtCore.QRect(10, 10, 381, 531))
        self.Map.setUrl(QtCore.QUrl("file:///C:/Users/31125/Desktop/python_files/TeamProjects/map.html"))
        self.Map.setObjectName("webEngineView")
        
        #위에 메뉴바 관련
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuMenu = QtWidgets.QMenu(self.menuBar)
        self.menuMenu.setObjectName("menuabout")
        MainWindow.setMenuBar(self.menuBar)
        
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setShortcutContext(QtCore.Qt.WidgetWithChildrenShortcut)
        self.actionAbout.setObjectName("actionAbout")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionAbout)
        self.menuMenu.addAction(self.actionQuit)
        self.menuBar.addAction(self.menuMenu.menuAction())

        #정의할 것들 다 했고 시그널 등
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.actionAbout.triggered.connect(self.aboutOpen)
        self.actionQuit.triggered.connect(app.quit)
        self.SearchButton.clicked.connect(self.SearchClicked)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.Dialog = QDialog()
    
    #메인창 내용물에 한글로 글자들 번역해서 넣어줌
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TripWithGPT"))
        self.PsTitle.setText(_translate("MainWindow", "P.S."))
        self.PsContents.setText(_translate("MainWindow", "GPT의 TMI 설명부분"))
        self.NameLabel1.setText(_translate("MainWindow", "NameLabel1"))
        self.ContentLabel1.setText(_translate("MainWindow", "<html><head/><body><p>대충 내용물1</p></body></html>"))
        self.NameLabel3.setText(_translate("MainWindow", "NameLabel3"))
        self.NameLabel2.setText(_translate("MainWindow", "NameLabel2"))
        self.ContentLabel2.setText(_translate("MainWindow", "<html><head/><body><p>대충 내용물 2</p></body></html>"))
        self.ContentLabel3.setText(_translate("MainWindow", "<html><head/><body><p>대충 내용물 3</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab1), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab2), _translate("MainWindow", "Tab 2"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionQuit.setText(_translate("MainWindow","Quit"))
    
    #메뉴바에 about 누르면 창 열리게
    def aboutOpen(self):
        self.Dialog.setObjectName("Dialog")
        self.Dialog.resize(400, 300)
        self.label_4 = QtWidgets.QLabel(self.Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 231, 16))
        font = QtGui.QFont()
        font.setFamily("굴림")
        font.setPointSize(8)
        font.setKerning(True)
        self.label_4.setFont(font)
        self.label_4.setTextFormat(QtCore.Qt.AutoText)
        self.label_4.setIndent(-1)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.Dialog)
        self.label_5.setGeometry(QtCore.QRect(10, 30, 64, 15))
        font = QtGui.QFont()
        font.setFamily("굴림")
        font.setPointSize(8)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label = QtWidgets.QLabel(self.Dialog)
        self.label.setGeometry(QtCore.QRect(10, 70, 381, 71))
        font = QtGui.QFont()
        font.setFamily("굴림")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.Dialog)
        self.label_3.setGeometry(QtCore.QRect(100, 130, 231, 81))
        self.label_3.setObjectName("label_3")
        self.label_2 = QtWidgets.QLabel(self.Dialog)
        self.label_2.setGeometry(QtCore.QRect(60, 130, 64, 15))
        self.label_2.setObjectName("label_2")
        self.CloseButton = QtWidgets.QPushButton(self.Dialog)
        self.CloseButton.setGeometry(QtCore.QRect(280, 240, 93, 28))
        self.CloseButton.setObjectName("CloseButton")

        self.aboutRetranslateUi(self.Dialog)
        self.CloseButton.clicked.connect(self.Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)
        self.Dialog.show()

    #about 창도 한글로 글자들 넣어줌
    def aboutRetranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "About"))
        self.label_4.setText(_translate("Dialog", "<html><head/><body><p>23-1학기 오픈소스 기초프로젝트</p></body></html>"))
        self.label_5.setText(_translate("Dialog", "<html><head/><body><p>3팀 0차0차</p></body></html>"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">★팀장: 2022041062 최상영 - 크롤링 및 총괄 담당★</p></body></html>"))
        self.label_3.setText(_translate("Dialog", "<html><head/><body><p>2020039070 전종영 - 크롤링 담당</p><p>2022041081 홍준석 - API 담당</p><p>2022041056 윤정아 - GUI 담당</p><p><br/></p></body></html>"))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p>팀원:</p></body></html>"))
        self.CloseButton.setText(_translate("Dialog", "닫기"))

    #검색 버튼 누르면 크롤링, API로 나온 내용들 로딩되게 구현할 예정
    #현재는 NameLabel1이 검색창에 입력한 내용으로 변함
    def SearchClicked(self):
        self.text = self.SearchEdit.text()
        self.NameLabel1.setText(self.text)
        #apis.APIS(1,self.text)
        #self.Map.setUrl(QtCore.QUrl("file:///C:/Users/31125/Desktop/python_files/TeamProjects/map.html"))
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

