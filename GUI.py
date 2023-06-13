from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtTest
import os
from urllib import parse

import chatgpt
import search
import map


class Ui_MainWindow(QMainWindow):
#메인창 내용물
    def setupUi(self, MainWindow):
    #메인창 관련
    #메인창 크기 1200*700
        MainWindow.resize(1200, 700)
    #메인창 크기 조정 못하게
        MainWindow.setMinimumSize(QtCore.QSize(1200, 700))
        MainWindow.setMaximumSize(QtCore.QSize(1200, 700))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        
        
    #ps창 관련
    #ps창 프레임
        self.Psframe = QtWidgets.QFrame(self.centralwidget)
        self.Psframe.setGeometry(QtCore.QRect(590, 520, 591, 121))
        self.Psframe.setFrameShape(QtWidgets.QFrame.Box)
    #p.s. 적힌 글씨 라벨 크기
        self.PsTitle = QtWidgets.QLabel(self.Psframe)
        self.PsTitle.setGeometry(QtCore.QRect(7, 4, 591, 21))
    #ps에 적힌 내용물 라벨 크기 지정, 크기보다 크면 줄바꿈
        self.PsContents = QtWidgets.QLabel(self.Psframe)
        self.PsContents.setGeometry(QtCore.QRect(20, 10, 561, 110))
        self.PsContents.setWordWrap(True)
        
        
    #검색창 관련
    #검색창 프레임 크기 지정, 테두리
        self.SearchFrame = QtWidgets.QFrame(self.centralwidget)
        self.SearchFrame.setGeometry(QtCore.QRect(590, 10, 591, 51))
        self.SearchFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.SearchFrame.setFrameShadow(QtWidgets.QFrame.Raised)
    #검색창에 글씨 입력하는 부분 크기 지정
        self.SearchEdit = QtWidgets.QLineEdit(self.SearchFrame)
        self.SearchEdit.setGeometry(QtCore.QRect(10, 10, 531, 31))
    #검색 버튼 크기 지정
        self.SearchButton = QtWidgets.QPushButton(self.SearchFrame)
        self.SearchButton.setGeometry(QtCore.QRect(540, 10, 40, 32))
    #검색 버튼 아이콘
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./ClueIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.SearchButton.setIcon(icon)
    #검색 종료 여부에 사용될 bool타입 변수
        self.SearchEnd = bool(False)
    #검색 중 나올 로딩 안내문
        self.SearchLoading = QtWidgets.QLabel(self.centralwidget)
        self.SearchLoading.setGeometry(470,210,300,100)
        self.SearchLoading.setAlignment(Qt.AlignCenter)


    #스크롤바 관련
    #스크롤바 틀 크기 지정
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(590, 100, 591, 411))
    #스크롤바 내용물 크기 지정
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 561, 1000))


    #삭제 관련, 교체 관련
    #삭제 버튼(check to delete) 크기 지정
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setGeometry(QtCore.QRect(1040, 65, 142, 31))
    #쓰레기통 그려진 버튼 크기 지정, 숨김
        self.trashCan = QtWidgets.QPushButton(self.centralwidget)
        self.trashCan.setGeometry(QtCore.QRect(1150, 65, 31, 31))
        self.trashCan.hide()
    #쓰레기통 버튼 아이콘 지정
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./replace.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.trashCan.setIcon(icon1)
    #삭제 취소버튼 크기 지정, 숨김
        self.cancelBtn = QtWidgets.QPushButton(self.centralwidget)
        self.cancelBtn.setGeometry(QtCore.QRect(1070, 65, 71, 31))
        self.cancelBtn.hide()
    #리뷰끼리 위치 바꾸는 변경버튼 크기 지정
        self.changeButton = QtWidgets.QPushButton(self.centralwidget)
        self.changeButton.setGeometry(QtCore.QRect(590, 65, 112, 30))
        self.changeButton.setText("위치 변경")
        self.changeOpened = bool(False)
    #변경버튼 아이콘 지정
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./change.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.changeButton.setIconSize(QtCore.QSize(70,25))
        self.changeButton.setIcon(icon1)
    # 리무브 관련 체크여부를 확인할 인덱스 리스트
        self.index_list = []
        self.point_list = []


    #맵 관련: 지금은 같이 올린 html 파일 주소 입력되어 있음
        self.Map = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.Map.setGeometry(QtCore.QRect(20, 10, 551, 641))
        self.map_path = 'map.html'
        abs_map_path = os.path.abspath(self.map_path)
        abs_map_path = abs_map_path.replace('\\','/')
        self.Map.setUrl(QtCore.QUrl(abs_map_path))
        self.place_names_list = []

    #최적화 버튼 크기 지정
        self.optimize = QtWidgets.QPushButton(self.centralwidget)
        self.optimize.setGeometry(QtCore.QRect(470, 17, 94, 28))
        self.isOptimizeAble = bool(True)

    #메뉴바 관련
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
    #메뉴바 생성
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1200, 26))
    #메뉴바에 Menu 써진 메뉴 생성
        self.menuabout = QtWidgets.QMenu(self.menuBar)
        MainWindow.setMenuBar(self.menuBar)
    #Menu 누르면 나오는 action에 About과 Quit, error(시험용) 생성
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionError = QtWidgets.QAction(MainWindow)
    #생성된 About과 Quit을 Menu에 추가, 메뉴바에 Menu 추가
        self.menuabout.addAction(self.actionAbout)
        self.menuabout.addAction(self.actionQuit)
        self.menuabout.addAction(self.actionError)
        self.menuBar.addAction(self.menuabout.menuAction())


    #내용물 정의 완료, 시그널로 제어
    #리뷰들 생성하는 makeReviews
        self.makeReviews()
    #scrollArea에 내용물인 scrollAreaWidgetContents 넣음
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
    #메인창 필요한 곳에 text 세팅
        self.setTexts(MainWindow)
        

    #각 버튼들 클릭시 연결된 이벤트 발생
        self.optimize.clicked.connect(self.optimize_func)
        self.changeButton.clicked.connect(self.changeOpen)
        self.actionAbout.triggered.connect(self.aboutOpen)
        self.actionQuit.triggered.connect(app.quit)
        self.actionError.triggered.connect(self.ErrorOpen)
        self.SearchButton.clicked.connect(self.SearchClicked)
        
        self.deleteButton.clicked.connect(self.deleteClicked)
        self.cancelBtn.clicked.connect(self.removeEnd)
        self.trashCan.clicked.connect(self.removeItems)
        
    #메인창 말고 about창, 위치변경창도 Dialog(창)으로 정의
        self.Dialog = QDialog()
        self.Form = QDialog()
        self.ErrorDialog = QDialog()

    #로딩 안내문이 맨 앞으로 오게 raise로 당겨주기
        self.SearchLoading.raise_()
        self.errorHappened = bool(False)


#메인창 내용물에 text들 채워줌
    def setTexts(self, MainWindow):
    #폰트 지정
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        self.PsTitle.setFont(font)
        font.setFamily("나눔고딕")
        font.setPointSize(15)
        self.SearchLoading.setFont(font)

    #글자 내용들
        MainWindow.setWindowTitle("TripWithGPT")
        self.PsTitle.setText("P.S.")
        self.PsContents.setText("일본은 최첨단 기술뿐만 아니라 고대 문화가 풍부한 대조적인 나라로 가득합니다. 상징적인 랜드마크와 번화한 도시부터 산과 바다의 고요한 자연의 아름다움까지, 이 매혹적인 나라에는 모두를 위한 무언가가 있습니다. 전통과 현대의 독특한 조화를 경험할 준비를 하시고 여행 중에 맛있는 현지 요리를 맛보는 것도 잊지 마세요!")
        self.deleteButton.setText("다른 지역으로 교체")
        self.cancelBtn.setText("Cancel")
        self.menuabout.setTitle("메뉴")
        self.actionAbout.setText("About")
        self.optimize.setText("경로 최적화")
        self.actionQuit.setText("Exit")
        self.actionError.setText("Error")


#리뷰들에 들어가는 제목, 내용물, 리뷰 별과 갯수, 이미지, 체크박스를 생성
    def makeReviews(self):
        self.names = [QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents)]
        self.contents = [QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents)]
        self.imgs = [QtWebEngineWidgets.QWebEngineView(self.scrollAreaWidgetContents),QtWebEngineWidgets.QWebEngineView(self.scrollAreaWidgetContents),QtWebEngineWidgets.QWebEngineView(self.scrollAreaWidgetContents),QtWebEngineWidgets.QWebEngineView(self.scrollAreaWidgetContents),QtWebEngineWidgets.QWebEngineView(self.scrollAreaWidgetContents)]
        self.reviewPoints = [QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents)]
        self.reviewStars = [QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),]
        self.reviews = [QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents)]
        self.checkBoxes = [QtWidgets.QCheckBox(self.scrollAreaWidgetContents),QtWidgets.QCheckBox(self.scrollAreaWidgetContents),QtWidgets.QCheckBox(self.scrollAreaWidgetContents),QtWidgets.QCheckBox(self.scrollAreaWidgetContents),QtWidgets.QCheckBox(self.scrollAreaWidgetContents)]
    #메인 스레드에서 setUrl을 하기 위해 saveUrls에 검색으로 얻은 Url들 저장
        self.saveUrls = [str,str,str,str,str]
    #지역 유명장소 리턴 공간
        self.LandmarksName = [QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents)]
    #이미지 없을 때 띄울 no_image를 위한 라벨
        self.no_imgs = [QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents)]

    #리뷰 제목에 적용할 폰트
        font = QtGui.QFont()
        font.setFamily("한컴산뜻돋움")
        font.setPointSize(14)
        font.setWeight(50)

    #Qpixmap으로 no_imgs에 사진 넣기
        pixmap = QPixmap("no_image.png")
        pixmap = pixmap.scaled(130,122)

        for i in range(0,5,1):
    #리뷰 제목들 위치, 폰트, text 세팅
            self.names[i].setGeometry(QtCore.QRect(10, 8+195*i, 535, 31))
            self.names[i].setFont(font)
            self.names[i].setText(("%s번째") % str(i+1))
    #리뷰 제목들 위치, text, 줄바꿈 세팅
            self.contents[i].setGeometry(QtCore.QRect(145, 84+195*i, 418, 130))
            self.contents[i].setText(("%s번째 내용물") % str(i+1))
            self.contents[i].setWordWrap(True)
            self.contents[i].setAlignment(QtCore.Qt.AlignTop)
    #리뷰 이미지, 별점들, 체크박스 위치 및 text 세팅, 체크박스 숨김
            self.imgs[i].setGeometry(QtCore.QRect(10, 52+195*i, 130, 122))
            self.no_imgs[i].setGeometry(QtCore.QRect(10, 52+195*i, 130, 122))
            self.no_imgs[i].setPixmap(pixmap)

            self.reviewPoints[i].setGeometry(QtCore.QRect(144, 44+195*i, 51, 17))
            self.reviewPoints[i].setText("4.0")
            self.reviewStars[i].setText("★★★★★")
            self.reviews[i].setGeometry(QtCore.QRect(258, 44+195*i, 101, 16))
            self.reviews[i].setText("1,234")
            self.checkBoxes[i].setGeometry(13, 0+195*i, 130, 55)
            self.checkBoxes[i].hide()
            self.LandmarksName[i].setGeometry(QtCore.QRect(145, 64+195*i, 418, 16))
    #리뷰 내용들 처음엔 안보이게, 버튼도 비활성화
        for i in range(0,5,1):
            self.names[i].hide()
            self.contents[i].hide()
            self.reviews[i].hide()
            self.reviewPoints[i].hide()
            self.reviewStars[i].hide()
            self.imgs[i].hide()
            self.no_imgs[i].hide()
            self.LandmarksName[i].hide()
        self.optimize.hide()
        self.deleteButton.hide()
        self.changeButton.hide()
        self.PsContents.hide()

    #별점은 중대사항: 디폴트 지정에 맞춰 별 갯수 노출 세팅
        for i in range(0,5,1):
            a = float(self.reviewPoints[i].text().replace(',','')) * 14.12
            self.reviewStars[i].setGeometry(QtCore.QRect(175, 44+195*i, 1+int(a), 15))
        
        
#메뉴바에 about 눌렀을 때 이벤트: 팀 정보창 열림
    def aboutOpen(self):
    #창 크기 지정
        self.Dialog.resize(400, 300)
    #강의명, 팀명, "팀원: "적힌 라벨 정의 및 위치 세팅
        self.lectureName = QtWidgets.QLabel(self.Dialog)
        self.lectureName.setGeometry(QtCore.QRect(10, 10, 231, 16))
        self.teamName = QtWidgets.QLabel(self.Dialog)
        self.teamName.setGeometry(QtCore.QRect(10, 30, 64, 15))
        self.label = QtWidgets.QLabel(self.Dialog)
        self.label.setGeometry(QtCore.QRect(60, 130, 64, 15))
    #우리 팀장님이랑 팀원들 이름 적힌 라벨 정의 및 위치 세팅
        self.teamLeader = QtWidgets.QLabel(self.Dialog)
        self.teamLeader.setGeometry(QtCore.QRect(10, 70, 381, 71))
        self.teamMem = QtWidgets.QLabel(self.Dialog)
        self.teamMem.setGeometry(QtCore.QRect(100, 130, 231, 81))
    #닫기 버튼 정의 및 위치 세팅    
        self.CloseButton = QtWidgets.QPushButton(self.Dialog)
        self.CloseButton.setGeometry(QtCore.QRect(280, 240, 93, 28))
    #about창 text들 세팅, 닫기 버튼 클릭시 닫히게
        self.aboutSetTexts(self.Dialog)
        self.CloseButton.clicked.connect(self.Dialog.close)
    #정의 끝났으니 창 열기
        self.Dialog.show()


#about 창에 text들 채워줌
    def aboutSetTexts(self, Dialog):
    #폰트 지정
        font = QtGui.QFont()
        font.setFamily("굴림")
    #강의명, 팀명은 글자 크기 8
        font.setPointSize(8)
        self.lectureName.setFont(font)
        self.teamName.setFont(font)
    #우리 팀장님은 글자 크기 10
        font.setPointSize(10)
        self.teamLeader.setFont(font)
    #세팅되는 text들
        Dialog.setWindowTitle("About")
        self.lectureName.setText("23-1학기 오픈소스 기초프로젝트")
        self.teamName.setText("3팀 0차0차")
        self.teamLeader.setText("<html><head/><body><p align=\"center\">★팀장: 2022041062 최상영 - 크롤링 및 총괄 담당★</p></body></html>")
        self.label.setText("팀원:")
        self.teamMem.setText("<html><head/><body><p>2020039070 전종영 - 크롤링 담당</p><p>2022041081 홍준석 - API 담당</p><p>2022041056 윤정아 - GUI 담당</p><p><br/></p></body></html>")
        self.CloseButton.setText("닫기")


#searchButton 눌렀을 때 이벤트: 크롤링, API로 나온 내용들 로딩
    def SearchClicked(self):
    #새 스레드 만들어서 시작: 메인 스레드는 그대로라 로딩중 응답없음이 안 뜸
        actionSearch = Search_loading(parent=self)
        actionSearch.start()

    #새 스레드에서 작업 완료되기 전까지 띄울 로딩 안내문
        self.SearchLoading.setStyleSheet("background-color: #FFFFFF")
        self.SearchLoading.show()
        while not self.SearchEnd:
            self.SearchLoading.setText("내용을 불러오고 있습니다.\n잠시만 기다려 주세요.")
            QtTest.QTest.qWait(1000)
            self.SearchLoading.setText("내용을 불러오고 있습니다.\n잠시만 기다려 주세요..")
            QtTest.QTest.qWait(1000)
            self.SearchLoading.setText("내용을 불러오고 있습니다.\n잠시만 기다려 주세요...")
            QtTest.QTest.qWait(1000)
    #검색 끝났으면 SearchEnd를 false로 바꾸고 로딩안내문 숨김
        if (self.errorHappened == True):
            self.ErrorOpen()
            for i in range(0, 5, 1):
                self.names[i].hide()
                self.contents[i].hide()
                self.reviews[i].hide()
                self.reviewPoints[i].hide()
                self.reviewStars[i].hide()
                self.imgs[i].hide()
                self.no_imgs[i].hide()
                self.LandmarksName[i].hide()
            self.optimize.hide()
            self.deleteButton.hide()
            self.changeButton.hide()
            self.PsContents.hide()
            self.errorHappened = False
        else:
            for i in range(0, 5, 1):
                self.names[i].show()
                self.contents[i].show()
                self.reviews[i].show()
                self.reviewPoints[i].show()
                self.reviewStars[i].show()
                self.LandmarksName[i].show()
                self.imgs[i].show()
                if self.saveUrls[i] != "no_image.png":
                    self.imgs[i].setUrl(QUrl("%s" % self.saveUrls[i]))
                else:
                    abs_save_Urls = os.path.abspath(self.saveUrls[i])
                    abs_save_Urls = abs_save_Urls.replace('\\', '/')
                    self.imgs[i].setUrl(QtCore.QUrl(abs_save_Urls))
                    self.imgs[i].show()
            self.optimize.show()
            self.deleteButton.show()
            self.changeButton.show()
            self.PsContents.show()
            abs_map_path = os.path.abspath(self.map_path)
            abs_map_path = abs_map_path.replace('\\', '/')
            self.Map.setUrl(QtCore.QUrl(abs_map_path))
            self.Map.show()
            if self.isOptimizeAble == True:
                self.optimize.setEnabled(True)
            else:
                self.optimize.setEnabled(False)
        self.SearchEnd = False
        self.SearchLoading.hide()



#deleteButton 눌렀을 때 이벤트: 버튼들이랑 체크박스 나타남
    def deleteClicked(self):
        self.deleteButton.hide()
        self.cancelBtn.show()
        self.trashCan.show()
    #체크박스들 나타나고 리뷰들 제목을 옆으로 좀 옮김
        for i in range(0,5,1):
            self.checkBoxes[i].show()
            self.names[i].setGeometry(QtCore.QRect(35, 8+195*i, 475, 31))


#cancelBtn 눌렀을 때 이벤트: 체크박스 안보이게 원상복귀, 체크상태 해제
    def removeEnd(self):
        self.deleteButton.show()
        self.trashCan.hide()
        self.cancelBtn.hide()
    #체크박스 숨김, 체크상태 해제, 리뷰 제목들 위치 돌아옴
        for i in range(0,5,1):
            self.checkBoxes[i].hide()
            self.checkBoxes[i].setChecked(False)
            self.names[i].setGeometry(QtCore.QRect(10, 8+195*i, 535, 31))
        
        
#trashCan 눌렀을 때 이벤트: index_list에 체크된 아이템 추가, 다시 돌림
    def removeItems(self):
        self.deleteButton.show()
        self.trashCan.hide()
        self.cancelBtn.hide()
    #버튼 숨기기
        self.deleteButton.setEnabled(False)
        self.SearchButton.setEnabled(False)
        self.changeButton.setEnabled(False)
        self.optimize.setEnabled(False)

        ###################### 일부 장소는 주제를 바꿔서 탐색할수도 있게 해도 괜찮을 듯, 고려 필요.
        for i in range(0,5,1):
            if (self.checkBoxes[i].isChecked()):
                self.index_list.append(i)
            self.checkBoxes[i].hide()
            self.checkBoxes[i].setChecked(False)
            self.names[i].setGeometry(QtCore.QRect(10, 8+195*i, 535, 31))

            # self.process_call(topic,index_list,1)
            # 새 스레드 만들어서 시작: 메인 스레드는 그대로라 로딩중 응답없음이 안 뜸

        actionSearch = Remove_loading(parent=self)
        actionSearch.start()

        # 새 스레드에서 작업 완료되기 전까지 띄울 로딩 안내문
        self.SearchLoading.show()
        while not self.SearchEnd:
            self.SearchLoading.setText("내용을 불러오고 있습니다.\n잠시만 기다려 주세요.")
            QtTest.QTest.qWait(1000)
            self.SearchLoading.setText("내용을 불러오고 있습니다.\n잠시만 기다려 주세요..")
            QtTest.QTest.qWait(1000)
            self.SearchLoading.setText("내용을 불러오고 있습니다.\n잠시만 기다려 주세요...")
            QtTest.QTest.qWait(1000)

        # 검색 끝났으면 SearchEnd를 false로 바꾸고 로딩안내문 숨김
        self.SearchEnd = False
        self.SearchLoading.hide()

        # 리무브 함수 진행 중 에러
        if (self.errorHappened == True):
            self.ErrorOpen()
            for i in range(0, 5, 1):
                self.names[i].hide()
                self.contents[i].hide()
                self.reviews[i].hide()
                self.reviewPoints[i].hide()
                self.reviewStars[i].hide()
                self.imgs[i].hide()
                self.no_imgs[i].hide()
                self.LandmarksName[i].hide()
            self.optimize.hide()
            self.deleteButton.hide()
            self.changeButton.hide()
            self.PsContents.hide()
            self.errorHappened = False
            self.map_path = "map.html"
            abs_map_path = os.path.abspath(self.map_path)
            abs_map_path = abs_map_path.replace('\\', '/')
            self.Map.setUrl(QtCore.QUrl(abs_map_path))
            self.Map.show()
            return
        else:
            for i in range(0, 5, 1):
                self.imgs[i].setUrl(QUrl("%s" % self.saveUrls[i]))
            abs_map_path = os.path.abspath(self.map_path)
            abs_map_path = abs_map_path.replace('\\', '/')
            self.Map.setUrl(QtCore.QUrl(abs_map_path))
            self.Map.show()
            self.deleteButton.setEnabled(True)
            self.SearchButton.setEnabled(True)
            self.changeButton.setEnabled(True)
            self.optimize.setEnabled(True)



#ChangeBtn 눌렀을 때 초기화
    def changeOption(self):
        self.fir_num = 0
    #change창 크기 지정, 왼쪽에 나타나게 함
        self.changeOpened = True
        self.changeOnce = bool(True)
        self.Form.resize(392, 500)
        self.Form.move(500, 200)
        
    #시작하면 나오는 1~10번 리뷰들 제목 있는 버튼들
        self.LabelBtns = [QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),]
    #라벨버튼 눌렀을 때 나오는 1~10번 제목 라벨들
        self.changeLabels = [QtWidgets.QLabel(self.Form),QtWidgets.QLabel(self.Form),QtWidgets.QLabel(self.Form),QtWidgets.QLabel(self.Form),QtWidgets.QLabel(self.Form)]
    #라벨버튼 눌렀을 때 나오는 이동버튼
        self.changeBtns = [QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form)]
    #1~5번중 선택했을 때 'n번 선택됨' 띄우는 disabled된 버튼
        self.disableLabelBtns = [QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form)]
        
        for i in range(0,5,1):
        #각 changeLables, disalbeLabelBtns, LabelBtns 위치 지정 및 글자 내용 세팅
            self.changeLabels[i].setGeometry(QtCore.QRect(20,70+70*i,350,22))
            self.changeLabels[i].setAlignment(QtCore.Qt.AlignCenter)    
            self.disableLabelBtns[i].setGeometry(QtCore.QRect(20,70+70*i,350,25))
            self.disableLabelBtns[i].setDisabled(True)
            self.LabelBtns[i].setGeometry(QtCore.QRect(20,70+70*i,350,23))
                     
        for i in range(0,6,1):
        #changeBtn 위치 지정, 글자 내용 세팅
        #얘만 따로 뺀 이유는 얘만 총 6개라서
            self.changeBtns[i].setGeometry(QtCore.QRect(150, 35+70*i, 90, 23))
            
    #for문 썼더니 맨 뒤에 꺼만 돼서 각각 나눠놨어요
    #lambda 써야 인수 안쪽 함수에 인수 넣는 게 되더라고요
        self.LabelBtns[0].clicked.connect(lambda: self.LabelSelect(0))    
        self.LabelBtns[1].clicked.connect(lambda: self.LabelSelect(1))
        self.LabelBtns[2].clicked.connect(lambda: self.LabelSelect(2))
        self.LabelBtns[3].clicked.connect(lambda: self.LabelSelect(3))
        self.LabelBtns[4].clicked.connect(lambda: self.LabelSelect(4))    
   
    #취소버튼 정의, 크기 및 글자 지정, 숨김, 이벤트 연결
        self.cancelChangeBtn = QtWidgets.QPushButton(self.Form)
        self.cancelChangeBtn.setGeometry(QtCore.QRect(332, 10, 50, 28)) 
        self.cancelChangeBtn.clicked.connect(self.cancelChange)

        self.changeBtns[0].clicked.connect(lambda: self.changeSelect(self.fir_num,0))
        self.changeBtns[1].clicked.connect(lambda: self.changeSelect(self.fir_num,1))
        self.changeBtns[2].clicked.connect(lambda: self.changeSelect(self.fir_num,2))
        self.changeBtns[3].clicked.connect(lambda: self.changeSelect(self.fir_num,3))
        self.changeBtns[4].clicked.connect(lambda: self.changeSelect(self.fir_num,4))
        self.changeBtns[5].clicked.connect(lambda: self.changeSelect(self.fir_num,5))
        
#ChangeBtn 눌렀을 때 이벤트: 리뷰들 위치 교환할 창 열림
    def changeOpen(self):
        self.changeOnce = True
    #change창 크기 지정, 왼쪽에 나타나게 함
        if self.changeOpened ==False:
            self.changeOption()
        self.Form.resize(392, 500)
        self.Form.move(500, 200)
        
        for i in range(0,5,1):
        #각 changeLables, disalbeLabelBtns, LabelBtns 위치 지정 및 글자 내용 세팅
            self.changeLabels[i].hide()    
            self.disableLabelBtns[i].setText("선택됨")
            self.disableLabelBtns[i].hide()
            self.LabelBtns[i].setGeometry(QtCore.QRect(20,70+70*i,350,23))
            self.LabelBtns[i].setText(self.names[i].text())
        for i in range(0,6,1):
        #changeBtn 위치 지정, 글자 내용 세팅
        #얘만 따로 뺀 이유는 얘만 총 6개라서
            self.changeBtns[i].setText("이동")
            self.changeBtns[i].hide()
  
    #취소버튼 정의, 크기 및 글자 지정, 숨김, 이벤트 연결
        self.cancelChangeBtn.setText("취소")
        self.cancelChangeBtn.hide()
        
    #창 제목 지정하고서 열기
        self.Form.setWindowTitle("옮기기")
        self.Form.show()

    #창 닫아도 cancelChange 돌게 하는 소멸자 같은거
        self.Form.finished['int'].connect(self.cancelChange)


#위치 교환 창에서 1~10번 제목버튼 눌렀을 때 이벤트: 라벨로 전환되고 이동 버튼들 나옴
    def LabelSelect(self,num):
    #눌린 번호 위치의 비활성화 버튼이 나타남
        self.fir_num = num
        self.disableLabelBtns[num].show()
    #취소 눌렀다가 다시 실행해도 글자 안 겹치게 LabelBtns 글자 없앰.. 근데 두 번째 실행부턴 LabelBtns가 안 사라져요
        for i in range(0,5,1):            
            self.LabelBtns[i].hide()
            self.LabelBtns[i].setText("")
            self.changeBtns[i].show()
            self.changeLabels[i].setText(self.names[i].text())
            self.changeLabels[i].show()
            self.cancelChangeBtn.show()
    #changeBtns는 혼자만 원소 하나 더 있어서 따로 처리
        self.changeBtns[5].show()
    
    #눌린 버튼 위아래에는 이동 버튼 안 나타나게
        self.changeBtns[num].hide()
        self.changeBtns[num+1].hide()
    #역시 for문으로는 맨 뒤에꺼만 돼서 개별처리
        print("num: %d"%(num))
        
        
#cancelChangeBtn 눌렀을 때 이벤트: 누르면 다시 버튼으로 돌아감
    def cancelChange(self):
        for i in range(0,5,1):
            self.disableLabelBtns[i].hide()
            self.changeBtns[i].hide()
            self.changeLabels[i].hide()
            self.cancelChangeBtn.hide()
        #제목 버튼 눌렀을 때 text 지워버려서 다시 채워줌
            self.changeLabels[i].setText(self.names[i].text())
            self.LabelBtns[i].setText(self.names[i].text())
            self.LabelBtns[i].show()
        self.changeBtns[5].hide()


#첫번째 지정된 리뷰 자리를 두번째 지정된 리뷰 자리로 끌어올리고 창 닫기
    def changeSelect(self,first_num,second_num):
        if (self.changeOnce == True):
    #이게 생각해보니까 아래에서 위로 가는 거랑 위에서 아래로 가는 거랑 따로 생각해야 하더라고요
            if first_num < second_num:
                second_num-=1
            
        #pop할 내용 임시 저장
            print("first_num:%d, second_num: %d"%(first_num,second_num))
            self.temps = [self.names.pop(first_num),self.contents.pop(first_num),self.imgs.pop(first_num),self.reviewPoints.pop(first_num),self.reviews.pop(first_num),self.point_list.pop(first_num),self.LandmarksName.pop(first_num),self.place_names_list.pop(first_num)]
        
            self.names.insert(second_num,self.temps.pop(0))
            self.contents.insert(second_num,self.temps.pop(0))
            self.imgs.insert(second_num,self.temps.pop(0))
            self.reviewPoints.insert(second_num,self.temps.pop(0))
            self.reviews.insert(second_num,self.temps.pop(0))
            self.point_list.insert(second_num,self.temps.pop(0))
            self.LandmarksName.insert(second_num,self.temps.pop(0))
            self.place_names_list.insert(second_num,self.temps.pop(0))

            for i in range(0,5,1):
                self.changeLabels[i].clear()
                self.disableLabelBtns[i].hide()
                self.changeBtns[i].hide()
                self.changeLabels[i].hide()
                self.cancelChangeBtn.hide()
                self.LabelBtns[i].show() 
            self.changeBtns[5].hide()
            self.Form.close()
        
        #단순히 insert만 해서는 내용 갱신이 안 돼서 다시 setText, setUrl, 위치 변경
            for i in range(0,5,1):
                self.names[i].setText(self.names[i].text())
                self.contents[i].setText(self.contents[i].text())
                self.imgs[i].setUrl(QtCore.QUrl(self.imgs[i].url().toString()))
                self.reviewPoints[i].setText(self.reviewPoints[i].text())
                self.reviews[i].setText(self.reviews[i].text())
                self.LandmarksName[i].setText(self.LandmarksName[i].text())

                self.names[i].setGeometry(QtCore.QRect(10, 8+195*i, 535, 31))
                self.contents[i].setGeometry(QtCore.QRect(145, 84+195*i, 418, 130))
                self.imgs[i].setGeometry(QtCore.QRect(10, 42+195*i, 130, 122))
                self.reviewPoints[i].setGeometry(QtCore.QRect(144, 44+195*i, 51, 17))
                self.reviews[i].setGeometry(QtCore.QRect(258, 44+195*i, 101, 16))
                self.LandmarksName[i].setGeometry(QtCore.QRect(145, 64+195*i, 418, 16))

            #바뀐 별점에 따라 별 갯수 노출도 변화
                a = float(self.reviewPoints[i].text().replace(',','')) * 14.12
                self.reviewStars[i].setGeometry(QtCore.QRect(175, 44+195*i, 1+int(a), 15))

            # 맵 다시 띄우기
            mapchecker, opti_checker = map.MainFunc(self.point_list,self.place_names_list)
            if mapchecker == "-99":
                self.errorHappened = True
                self.map_path = "map.html"
            else:
                self.map_path = 'route.html'
            abs_map_path = os.path.abspath(self.map_path)
            abs_map_path = abs_map_path.replace('\\', '/')
            self.Map.setUrl(QtCore.QUrl(abs_map_path))
            self.Map.show()

            if opti_checker == -1:
                self.optimize.setEnabled(False)
            elif opti_checker == 0:
                self.optimize.setEnabled(True)

            # 체인지 함수에서 에러
            if (self.errorHappened == True):
                self.ErrorOpen()
                for i in range(0, 5, 1):
                    self.names[i].hide()
                    self.contents[i].hide()
                    self.reviews[i].hide()
                    self.reviewPoints[i].hide()
                    self.reviewStars[i].hide()
                    self.imgs[i].hide()
                    self.no_imgs[i].hide()
                    self.LandmarksName[i].hide()
                self.optimize.hide()
                self.deleteButton.hide()
                self.changeButton.hide()
                self.PsContents.hide()
                self.errorHappened = False
            self.changeOnce = False
            



#ChatGPT에게 검색창에 나온 내용으로 검색 요청하기
    def process_call(self, process_topic, index_list=[], recall=0):
        global except_list
        global topic
        topic = process_topic ## 변수 낭비일수도 있는데, 귀찮아서 추가함.
        n = 5
        eng_list, kor_name, kor_introduce, ps = [], [], [], ''

        def search_error_index(process_topic, error_count):  #### 서치 데이터 -1 관련 함수
            global except_list
            nonlocal search_list
            nonlocal eng_list
            nonlocal kor_name
            nonlocal kor_introduce

            minus1_index = []
            for _ in range(error_count):  # -1인 인덱스들 확인, 위치 저장
                minus1_index.append(search_list.index([-1]))
                search_list.pop(search_list.index([-1]))

            temp_eng_list, temp_kor_name, temp_kor_introduce, trash = chatgpt.gpt(process_topic, error_count, except_list)  # 에러 개수만큼 탐색, temp에 저장
            except_list.extend(temp_eng_list)  # 새로 탐색한것도 exceptlist에 추가해둠
            temp_search_list = search.search(temp_eng_list)  # search 데이터 temp에 저장
            # 일단 바깥의 사용용 데이터들 전부 새 데이터로 교체
            j = 0
            for i in minus1_index:
                eng_list[i] = temp_eng_list[j]
                kor_name[i] = temp_kor_name[j]
                kor_introduce[i] = temp_kor_introduce[j]
                search_list.insert(i, temp_search_list[j])
                j += 1
            error_count = search_list.count([-1])  # 다 교체는 해둔 뒤, error_count 재 체크
            if error_count == 0:  # 해결 완료시엔 끝
                return [0, 0]
            else:  # 아직도 비해결 시에는, 에러메시지인 1과 오류수 보냄
                return [1, error_count]

        ## 내용 검색 관련 조건문
        if recall == 1:  # 중복 제외후,  재검색하는 케이스 # index_list는 원래 부분에서 삭제하고, 교체할 부분을 나타냄
            n = len(index_list)  # 같은 주제 재탐색하는, 중복제외 필요시 상황 ( 검색버튼 다시누른 케이스가 아니라, 삭제후 재탐색으로 들어온 케이스)
            temp = chatgpt.gpt(process_topic, n, except_list)
            if temp == [-99]: ## 에러 발생시
                self.errorHappened = True
                return
            eng_list, kor_name, kor_introduce, ps = temp
            except_list.extend(eng_list)

            search_list = search.search(eng_list)
            if search_list == [-99]: ## 에러 발생시
                self.errorHappened = True
                return
            error_count = search_list.count([-1])

            if error_count != 0:  # 폐업점 등으로 일부 재탐색 필요시
                chk, next_error_counter = search_error_index(process_topic, error_count)
                while chk != 0:  # 한번 끝난 후에도 해결이 안됐다면 재진입, 해결될때까지 재진입할것
                    chk, next_error_counter = search_error_index(process_topic, next_error_counter)
        else:
            except_list.clear()
            self.point_list.clear()
            self.place_names_list.clear()
            temp = chatgpt.gpt(process_topic, n)
            if temp == [-99]: ## 에러 발생시
                self.errorHappened = True
                return
            eng_list, kor_name, kor_introduce, ps = temp
            except_list.extend(eng_list)

            search_list = search.search(eng_list)
            if search_list == [-99]: ## 에러 발생시
                self.errorHappened = True
                return
            error_count = search_list.count([-1])

            if error_count != 0:  # 폐업점 등으로 일부 재탐색 필요시
                chk, next_error_counter = search_error_index(process_topic, error_count)
                while chk != 0:  # 한번 끝난 후에도 해결이 안됐다면 재진입, 해결될때까지 재진입할것
                    chk, next_error_counter = search_error_index(process_topic, next_error_counter)

        ## 내용 지정 관련 조건문
        if recall == 0: # 다 바꿔야하는 경우
            for i in range(n):  #### 내용 지정부
                self.names[i].setText(kor_name[i])
                self.contents[i].setText(kor_introduce[i])

                # a = float(self.reviewPoints[0].text()) * 14.1
                # self.reviewStars[0].setGeometry(QtCore.QRect(175, 44 + 175 * 0, 2 + int(a), 15))

                if search_list[i][0] == 0:  # 0, 즉 장소일때
                    self.reviewPoints[i].setText(str("%.1f"%search_list[i][2]))
                    self.reviewStars[i].setGeometry(QtCore.QRect(175, 44 + 195 * i, 1 + int(search_list[i][2]*14.12), 15))
                    self.reviews[i].setText(str(format(search_list[i][3], ',')))
                    self.LandmarksName[i].setText(str(""))
                    self.point_list.append((search_list[i][5],search_list[i][6]))
                    self.place_names_list.append(search_list[i][1])
                    if search_list[i][4] != 'No Image':
                        self.saveUrls[i] = search_list[i][4]  # saveUrl에 넣어두고 다 끝나면 메인 스레드에서 setUrl
                    else:  # 이미지 없을땐
                        self.saveUrls[i] = "no_image.png"

                else:  # 1, 즉 지역일때
                    ########### 리뷰 대신, 추천지역 관련 변수 추가로 요구됨 (search_list[i][2][1])
                    self.reviewPoints[i].setText(str("%.1f"%search_list[i][2][1]))
                    self.reviewStars[i].setGeometry(QtCore.QRect(175, 44 + 195 * i, 1 + int(search_list[i][2][1]*14.12), 15))
                    self.reviews[i].setText(str(format(search_list[i][2][2], ',')))
                    self.LandmarksName[i].setText(str("(주변 인기 관광지 " + search_list[i][2][0] + " 의 평점)"))
                    self.point_list.append((search_list[i][4],search_list[i][5]))
                    self.place_names_list.append(search_list[i][2][0])
                    if search_list[i][3] != 'No Image':
                        self.saveUrls[i] = search_list[i][3]  # saveUrl에 넣어두고 다 끝나면 메인 스레드에서 setUrl
                    else:  # 이미지 없을땐
                        self.saveUrls[i] = "no_image.png"
            self.PsContents.setText(ps)

        else: # 일부 인덱스만 교체해주면 되는 경우(리콜된 경우)
            for i,index in enumerate(index_list):
                self.names[index].setText(kor_name[i])
                self.contents[index].setText(kor_introduce[i])

                if search_list[i][0] == 0:  # 0, 즉 장소일때
                    self.reviewPoints[index].setText(str("%.1f"%(search_list[i][2])))
                    self.reviewStars[index].setGeometry(QtCore.QRect(175, 44 + 195 * index, 1 + int(search_list[i][2]*14.12), 15))
                    self.reviews[index].setText(str(format(search_list[i][3], ',')))
                    self.LandmarksName[index].setText(str(""))
                    self.point_list[index] = (search_list[i][5],search_list[i][6])
                    self.place_names_list[index] = search_list[i][1]
                    if search_list[i][4] != 'No Image':
                        self.saveUrls[index] = search_list[i][4]  # saveUrl에 넣어두고 다 끝나면 메인 스레드에서 setUrl
                    else:  # 이미지 없을땐
                        self.saveUrls[index] = "no_image.png"

                else:  # 1, 즉 지역일때
                    # 리뷰 대신, 추천지역 관련 변수 추가로 요구됨 (search_list[i][2][1])
                    self.reviewPoints[index].setText(str("%.1f"%(search_list[i][2][1])))
                    self.reviewStars[index].setGeometry(QtCore.QRect(175, 44 + 195 * index, 1 + int(search_list[i][2][1]*14.12), 15))
                    self.reviews[index].setText(str(format(search_list[i][2][2], ',')))
                    self.LandmarksName[index].setText(str("(주변 인기 관광지 " + search_list[i][2][0] + "의 평점)"))
                    self.point_list[index] = (search_list[i][4],search_list[i][5])
                    self.place_names_list[index] = search_list[i][2][0]
                    if search_list[i][3] != 'No Image':
                        self.saveUrls[index] = search_list[i][3]  # saveUrl에 넣어두고 다 끝나면 메인 스레드에서 setUrl
                    else:  # 이미지 없을땐
                        self.saveUrls[index] = "no_image.png"

        # map 함수 호출
        # 좌표 데이터 가지고 map함수 call 부분 필요
        self.optimize.setEnabled(False)
        mapchecker, opti_checker = map.MainFunc(self.point_list,self.place_names_list)

        if opti_checker == 0:
            self.isOptimizeAble = True
        else:
            self.isOptimizeAble = False

        if mapchecker == "-99":
            self.map_path = "map.html"
            self.errorHappened = True
        else:
            self.map_path = 'route.html'




    # [0 ,'검색한 장소=검색한 결과의 장소','평점','리뷰 수','사진링크','lat','lng']
    # [1 ,'검색한 장소',('검색한 결과의 장소','평점','리뷰 수'),'사진링크','lat','lng']
    # result_list=[0 or 1,'검색한 장소=검색한 결과의 장소','평점','리뷰 수','사진링크', '좌표(lat)', '좌표(lng)']


#에러창 오픈 이벤트
    def ErrorOpen(self):
        self.ErrorDialog.setObjectName("Dialog")
        self.ErrorDialog.resize(400, 300)
        self.ErrorDialog.setMinimumSize(QtCore.QSize(400, 300))
        self.ErrorDialog.setMaximumSize(QtCore.QSize(400, 300))
        self.centralwidget = QtWidgets.QWidget(self.ErrorDialog)

        self.label = QtWidgets.QLabel(self.ErrorDialog)
        self.label.setGeometry(QtCore.QRect(70, 80, 64, 91))

        font = QtGui.QFont()
        font.setPointSize(60)
        self.label.setFont(font)

        self.label_2 = QtWidgets.QLabel(self.ErrorDialog)
        self.label_2.setGeometry(QtCore.QRect(70, 100, 271, 51))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)

        self.pushButton = QtWidgets.QPushButton(self.ErrorDialog)
        self.pushButton.setGeometry(QtCore.QRect(150, 200, 93, 28))
        self.pushButton.clicked.connect(self.ErrorDialog.close)


        self.ErrorDialog.setWindowTitle("Error!")
        self.label.setText("!")
        self.label_2.setText("오류가 발생했습니다.\n다시 시도해 주세요.")
        self.pushButton.setText("확인")
        self.ErrorDialog.show()

    def optimize_func(self):

        mapchecker, waypoint_array = map.MainFunc(self.point_list, self.place_names_list, 1)


        if mapchecker == "-99":
            self.errorHappened = True # 에러창이랑 연결 만들어줘야됨 따로.
            self.map_path = "map.html"
        else:
            self.map_path = 'route.html'

        abs_map_path = os.path.abspath(self.map_path)
        abs_map_path = abs_map_path.replace('\\', '/')
        self.Map.setUrl(QtCore.QUrl(abs_map_path))
        self.Map.show()
        # 옵티마이저 함수에서 에러
        if (self.errorHappened == True):
            self.ErrorOpen()
            for i in range(0, 5, 1):
                self.names[i].hide()
                self.contents[i].hide()
                self.reviews[i].hide()
                self.reviewPoints[i].hide()
                self.reviewStars[i].hide()
                self.imgs[i].hide()
                self.no_imgs[i].hide()
                self.LandmarksName[i].hide()
            self.optimize.hide()
            self.deleteButton.hide()
            self.changeButton.hide()
            self.PsContents.hide()
            self.errorHappened = False
            return

        ## 받아온거 바탕으로 리스트 교환하기(재정렬)
        temp = []
        for i in waypoint_array:
            temp.append(self.names[i])
        self.names = temp[:]
        temp.clear()
        for i in waypoint_array:
            temp.append(self.contents[i])
        self.contents = temp[:]
        temp.clear()
        for i in waypoint_array:
            temp.append(self.imgs[i])
        self.imgs = temp[:]
        temp.clear()
        for i in waypoint_array:
            temp.append(self.reviewPoints[i])
        self.reviewPoints = temp[:]
        temp.clear()
        for i in waypoint_array:
            temp.append(self.reviews[i])
        self.reviews = temp[:]
        temp.clear()
        for i in waypoint_array:
            temp.append(self.point_list[i])
        self.point_list = temp[:]
        temp.clear()
        for i in waypoint_array:
            temp.append(self.LandmarksName[i])
        self.LandmarksName = temp[:]
        temp.clear()
        for i in waypoint_array:
            temp.append(self.place_names_list[i])
        self.place_names_list = temp[:]
        temp.clear()

        # 단순히 insert만 해서는 내용 갱신이 안 돼서 다시 setText, setUrl, 위치 변경
        for i in range(0, 5, 1):
            self.names[i].setText(self.names[i].text())
            self.contents[i].setText(self.contents[i].text())
            self.imgs[i].setUrl(QtCore.QUrl(self.imgs[i].url().toString()))
            self.reviewPoints[i].setText(self.reviewPoints[i].text())
            self.reviews[i].setText(self.reviews[i].text())
            self.LandmarksName[i].setText(self.LandmarksName[i].text())

            self.names[i].setGeometry(QtCore.QRect(10, 8 + 195 * i, 535, 31))
            self.contents[i].setGeometry(QtCore.QRect(145, 84 + 195 * i, 418, 130))
            self.imgs[i].setGeometry(QtCore.QRect(10, 42 + 195 * i, 130, 122))
            self.reviewPoints[i].setGeometry(QtCore.QRect(144, 44 + 195 * i, 51, 17))
            self.reviews[i].setGeometry(QtCore.QRect(258, 44 + 195 * i, 101, 16))
            self.LandmarksName[i].setGeometry(QtCore.QRect(145, 64 + 195 * i, 418, 16))

            # 바뀐 별점에 따라 별 갯수 노출도 변화
            a = float(self.reviewPoints[i].text().replace(',', '')) * 14.12
            self.reviewStars[i].setGeometry(QtCore.QRect(175, 44 + 195 * i, 1 + int(a), 15))
        if self.changeOpened == True:
            self.cancelChange()



#서치 로딩될 때 돌아가는 서브 스레드
class Search_loading(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        #버튼들 비활성화
        self.parent.deleteButton.setEnabled(False)
        self.parent.SearchButton.setEnabled(False)
        self.parent.changeButton.setEnabled(False)
        self.parent.optimize.setEnabled(False)

        # 검색하는 함수들 여기에 연결해주시면 됩니다
        # 메인윈도우 클래스꺼는 self.parent.붙여서 돌리시면 됩니다!
        self.parent.text = self.parent.SearchEdit.text()
        self.parent.process_call(self.parent.text)
        
        # 다 끝나고 버튼 활성화, 스레드 끝내주기
        self.parent.deleteButton.setEnabled(True)
        self.parent.SearchButton.setEnabled(True)
        self.parent.changeButton.setEnabled(True)
        self.parent.optimize.setEnabled(True)
        self.parent.SearchEnd = True
        self.quit()

#일부 항목 삭제, 제외 후 재검색시 돌아가는 서브 스레드
class Remove_loading(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        # 검색하는 함수들 여기에 연결해주시면 됩니다
        # 메인윈도우 클래스꺼는 self.parent.붙여서 돌리시면 됩니다!
        global topic
        self.parent.process_call(topic, self.parent.index_list, 1)

        # 다 끝나고 스레드 끝내주기
        self.parent.SearchEnd = True
        self.parent.index_list.clear()
        self.quit()



if __name__ == "__main__":
    import sys

    topic = ''
    except_list = []


    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
