import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from datetime import datetime
import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

price = ["4500원", "5500원", "4000원", "4500원", "5000원", "4000원", "4500원", "5000원", "4500원", "4500원", "4000원", "4500원"] #음식 가격 넣을 리스트
menu = ["제육덮밥", "돈까스김치볶음밥", "잔치국수", "돈까스카레덮밥", "떡국", "양파돈까스", "김치볶음밥", "등심돈까스", "치즈돈까스", "카레덮밥", "김치수제비", "함박스테이크"]#메뉴 넣을 리스트

cred = credentials.Certificate('myKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://graduate-work-462b3.firebaseio.com/'
})


class PicButton(QAbstractButton):   #버튼에 사진첨부하기 위한 클래스

    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()

class MyWindow(QWidget): #GUI창 설정

    def __init__(self):

        super().__init__()

        self.setGeometry(800, 200, 600, 630)    #크기설정 (x좌표,y좌표,너비,높이)

        self.btn1 = PicButton(QPixmap('../Olive/img1.jpg')) #버튼이미지를 가져올 경로
        self.btn1.setMaximumHeight(100) #버튼의 최대높이
        self.btn1.setMaximumWidth(100) #버튼의 최대너비

        self.Pbtn1 = QPushButton(menu[0]) #버튼의 이름
        self.Pbtn1.clicked.connect(self.btn1_clicked) #버튼을 눌렀을 때 불러올 함수

        self.btn2 = PicButton(QPixmap('../Olive/img2.jpg'))
        self.btn2.setMaximumHeight(100)
        self.btn2.setMaximumWidth(100)

        self.Pbtn2 = QPushButton(menu[1])
        self.Pbtn2.clicked.connect(self.btn2_clicked)

        self.btn3 = PicButton(QPixmap('../Olive/img3.jpg'))
        self.btn3.setMaximumHeight(100)
        self.btn3.setMaximumWidth(100)

        self.Pbtn3 = QPushButton(menu[2])
        self.Pbtn3.clicked.connect(self.btn3_clicked)

        self.btn4 = PicButton(QPixmap('../Olive/img4.jpg'))
        self.btn4.setMaximumHeight(100)
        self.btn4.setMaximumWidth(100)

        self.Pbtn4 = QPushButton(menu[3])
        self.Pbtn4.clicked.connect(self.btn4_clicked)

        self.btn5 = PicButton(QPixmap('../Olive/img5.jpg'))
        self.btn5.setMaximumHeight(100)
        self.btn5.setMaximumWidth(100)

        self.Pbtn5 = QPushButton(menu[4])
        self.Pbtn5.clicked.connect(self.btn5_clicked)

        self.btn6 = PicButton(QPixmap('../Olive/img6.jpg'))
        self.btn6.setMaximumHeight(100)
        self.btn6.setMaximumWidth(100)

        self.Pbtn6 = QPushButton(menu[5])
        self.Pbtn6.clicked.connect(self.btn6_clicked)

        self.btn7 = PicButton(QPixmap('../Olive/img7.jpg'))
        self.btn7.setMaximumHeight(100)
        self.btn7.setMaximumWidth(100)

        self.Pbtn7 = QPushButton(menu[6])
        self.Pbtn7.clicked.connect(self.btn7_clicked)

        self.btn8 = PicButton(QPixmap('../Olive/img8.jpg'))
        self.btn8.setMaximumHeight(100)
        self.btn8.setMaximumWidth(100)

        self.Pbtn8 = QPushButton(menu[7])
        self.Pbtn8.clicked.connect(self.btn8_clicked)

        self.btn9 = PicButton(QPixmap('../Olive/img9.jpg'))
        self.btn9.setMaximumHeight(100)
        self.btn9.setMaximumWidth(100)

        self.Pbtn9 = QPushButton(menu[8])
        self.Pbtn9.clicked.connect(self.btn9_clicked)

        self.btn10 = PicButton(QPixmap('../Olive/img10.jpg'))
        self.btn10.setMaximumHeight(100)
        self.btn10.setMaximumWidth(100)

        self.Pbtn10 = QPushButton(menu[9])
        self.Pbtn10.clicked.connect(self.btn10_clicked)

        self.btn11 = PicButton(QPixmap('../Olive/img11.jpg'))
        self.btn11.setMaximumHeight(100)
        self.btn11.setMaximumWidth(100)

        self.Pbtn11 = QPushButton(menu[10])
        self.Pbtn11.clicked.connect(self.btn11_clicked)

        self.btn12 = PicButton(QPixmap('../Olive/img12.jpg'))
        self.btn12.setMaximumHeight(100)
        self.btn12.setMaximumWidth(100)

        self.Pbtn12 = QPushButton(menu[11])
        self.Pbtn12.clicked.connect(self.btn12_clicked)

        self.Obtn1 = QPushButton("주문하기")
        self.Obtn1.setMaximumHeight(150)
        self.Obtn1.clicked.connect(self.btn_order)

        self.Obtn2 = QPushButton("취소하기")
        self.Obtn2.setMaximumHeight(150)
        self.Obtn2.clicked.connect(self.btn_refresh)

        layout1 = QGridLayout() #GUI 컨텐츠들을 배치할 레이아웃 설정

        layout1.addWidget(self.btn1, 0, 0) #버튼추가
        layout1.addWidget(self.btn2, 0, 1)
        layout1.addWidget(self.btn3, 0, 2)
        layout1.addWidget(self.btn4, 0, 3)

        layout1.addWidget(self.Pbtn1,1, 0)
        layout1.addWidget(self.Pbtn2, 1, 1)
        layout1.addWidget(self.Pbtn3, 1, 2)
        layout1.addWidget(self.Pbtn4, 1, 3)

        layout1.addWidget(self.btn5, 2, 0)
        layout1.addWidget(self.btn6, 2, 1)
        layout1.addWidget(self.btn7, 2, 2)
        layout1.addWidget(self.btn8, 2, 3)

        layout1.addWidget(self.Pbtn5, 3, 0)
        layout1.addWidget(self.Pbtn6, 3, 1)
        layout1.addWidget(self.Pbtn7, 3, 2)
        layout1.addWidget(self.Pbtn8, 3, 3)

        layout1.addWidget(self.btn9, 4, 0)
        layout1.addWidget(self.btn10, 4, 1)
        layout1.addWidget(self.btn11, 4, 2)
        layout1.addWidget(self.btn12, 4, 3)

        layout1.addWidget(self.Pbtn9, 5, 0)
        layout1.addWidget(self.Pbtn10, 5, 1)
        layout1.addWidget(self.Pbtn11, 5, 2)
        layout1.addWidget(self.Pbtn12, 5, 3)

        groupbox= QGroupBox("주문정보") #그룹박스 추가

        self.tableWidget = QTableWidget(4, 2) #테이블 생성
        self.tableWidget.setHorizontalHeaderLabels(["음식이름", "가격"])#식당이름까지 DB로 보냄
        self.tableWidget.setMaximumHeight(160) #테이블의 높이
        self.tableWidget.setMaximumWidth(250) #테이블의 너비
        self.tableWidget.horizontalHeader().setStretchLastSection(True) #글자가 넘어갔을때 글자가 ...으로 나오지 않도록 설정

        layout2 = QHBoxLayout() #레이아웃 추가
        layout2.addWidget(self.tableWidget) #테이블및 버튼추가
        layout2.addWidget(self.Obtn1)
        layout2.addWidget(self.Obtn2)

        groupbox.setLayout(layout2)

        layout3 = QHBoxLayout()
        layout3.addWidget(groupbox)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout3)

        self.setLayout(layout) #레이아웃 합침

    def btn1_clicked(self):
        print("클릭됨")

        if(self.tableWidget.item(0,0) is None):#비어있으면 첫번째줄에 넣기
            self.tableWidget.setItem(0, 0, QTableWidgetItem(self.Pbtn1.text()))  # 버튼이름
            self.tableWidget.setItem(0, 1, QTableWidgetItem(price[0]))  # 가격

        elif(self.tableWidget.item(1,0) is None and self.tableWidget.item(0,0) is not None): #첫번째 줄이 비어있지 않으면
            self.tableWidget.setItem(1, 0, QTableWidgetItem(self.Pbtn1.text()))  # 버튼이름
            self.tableWidget.setItem(1, 1, QTableWidgetItem(price[0]))  # 가격

        elif(self.tableWidget.item(1, 0) is not None and self.tableWidget.item(0,0) is not None
             and self.tableWidget.item(2,0) is None): #첫번째줄과 두번째줄이 모두 비어있지 않으면
            self.tableWidget.setItem(2, 0, QTableWidgetItem(self.Pbtn1.text()))  # 버튼이름
            self.tableWidget.setItem(2, 1, QTableWidgetItem(price[0]))  # 가격


        elif(self.tableWidget.item(2, 0) is not None and self.tableWidget.item(1, 0) is not None and
             self.tableWidget.item(0,0) is not None and self.tableWidget.item(3,0) is None): #첫번째줄과 두번쨰줄 세번쨰줄이 모두 비어있지 않으면
            self.tableWidget.setItem(3, 0, QTableWidgetItem(self.Pbtn1.text()))  # 버튼이름
            self.tableWidget.setItem(3, 1, QTableWidgetItem(price[0]))  # 가격



    def btn2_clicked(self):
        print("클릭됨")


        if (self.tableWidget.item(0, 0) is None):  # 비어있으면 첫번째줄에 넣기
            self.tableWidget.setItem(0, 0, QTableWidgetItem(self.Pbtn2.text()))  # 버튼이름
            self.tableWidget.setItem(0, 1, QTableWidgetItem(price[1]))  # 가격


        elif (self.tableWidget.item(1, 0) is None and self.tableWidget.item(0, 0) is not None):  # 첫번째 줄이 비어있지 않으면
            self.tableWidget.setItem(1, 0, QTableWidgetItem(self.Pbtn2.text()))  # 버튼이름
            self.tableWidget.setItem(1, 1, QTableWidgetItem(price[1]))  # 가격

        elif (self.tableWidget.item(1, 0) is not None and self.tableWidget.item(0, 0) is not None
              and self.tableWidget.item(2, 0) is None):  # 첫번째줄과 두번째줄이 모두 비어있지 않으면
            self.tableWidget.setItem(2, 0, QTableWidgetItem(self.Pbtn2.text()))  # 버튼이름
            self.tableWidget.setItem(2, 1, QTableWidgetItem(price[1]))  # 가격

        elif (self.tableWidget.item(2, 0) is not None and self.tableWidget.item(1, 0) is not None and
              self.tableWidget.item(0, 0) is not None and self.tableWidget.item(3,
                                                                                0) is None):  # 첫번째줄과 두번쨰줄 세번쨰줄이 모두 비어있지 않으면
            self.tableWidget.setItem(3, 0, QTableWidgetItem(self.Pbtn2.text()))  # 버튼이름
            self.tableWidget.setItem(3, 1, QTableWidgetItem(price[1]))  # 가격


    def btn3_clicked(self):
        print("클릭됨")

        if (self.tableWidget.item(0, 0) is None):  # 비어있으면 첫번째줄에 넣기
            self.tableWidget.setItem(0, 0, QTableWidgetItem(self.Pbtn3.text()))  # 버튼이름
            self.tableWidget.setItem(0, 1, QTableWidgetItem(price[2]))  # 가격


        elif (self.tableWidget.item(1, 0) is None and self.tableWidget.item(0, 0) is not None):  # 첫번째 줄이 비어있지 않으면
            self.tableWidget.setItem(1, 0, QTableWidgetItem(self.Pbtn3.text()))  # 버튼이름
            self.tableWidget.setItem(1, 1, QTableWidgetItem(price[2]))  # 가격

        elif (self.tableWidget.item(1, 0) is not None and self.tableWidget.item(0, 0) is not None
              and self.tableWidget.item(2, 0) is None):  # 첫번째줄과 두번째줄이 모두 비어있지 않으면
            self.tableWidget.setItem(2, 0, QTableWidgetItem(self.Pbtn3.text()))  # 버튼이름
            self.tableWidget.setItem(2, 1, QTableWidgetItem(price[2]))  # 가격


        elif (self.tableWidget.item(2, 0) is not None and self.tableWidget.item(1, 0) is not None and
              self.tableWidget.item(0, 0) is not None and self.tableWidget.item(3,
                                                                                0) is None):  # 첫번째줄과 두번쨰줄 세번쨰줄이 모두 비어있지 않으면
            self.tableWidget.setItem(3, 0, QTableWidgetItem(self.Pbtn3.text()))  # 버튼이름
            self.tableWidget.setItem(3, 1, QTableWidgetItem(price[2]))  # 가격

    def btn4_clicked(self):
        print("클릭됨")


        if (self.tableWidget.item(0, 0) is None):  # 비어있으면 첫번째줄에 넣기
            self.tableWidget.setItem(0, 0, QTableWidgetItem(self.Pbtn4.text()))  # 버튼이름
            self.tableWidget.setItem(0, 1, QTableWidgetItem(price[3]))  # 가격

        elif (self.tableWidget.item(1, 0) is None and self.tableWidget.item(0, 0) is not None):  # 첫번째 줄이 비어있지 않으면
            self.tableWidget.setItem(1, 0, QTableWidgetItem(self.Pbtn4.text()))  # 버튼이름
            self.tableWidget.setItem(1, 1, QTableWidgetItem(price[3]))  # 가격

        elif (self.tableWidget.item(1, 0) is not None and self.tableWidget.item(0, 0) is not None
              and self.tableWidget.item(2, 0) is None):  # 첫번째줄과 두번째줄이 모두 비어있지 않으면
            self.tableWidget.setItem(2, 0, QTableWidgetItem(self.Pbtn4.text()))  # 버튼이름
            self.tableWidget.setItem(2, 1, QTableWidgetItem(price[3]))  # 가격

        elif (self.tableWidget.item(2, 0) is not None and self.tableWidget.item(1, 0) is not None and
              self.tableWidget.item(0, 0) is not None and self.tableWidget.item(3,
                                                                                0) is None):  # 첫번째줄과 두번쨰줄 세번쨰줄이 모두 비어있지 않으면
            self.tableWidget.setItem(3, 0, QTableWidgetItem(self.Pbtn4.text()))  # 버튼이름
            self.tableWidget.setItem(3, 1, QTableWidgetItem(price[3]))  # 가격

    def btn5_clicked(self):
        print("클릭됨")

        if (self.tableWidget.item(0, 0) is None):  # 비어있으면 첫번째줄에 넣기
            self.tableWidget.setItem(0, 0, QTableWidgetItem(self.Pbtn5.text()))  # 버튼이름
            self.tableWidget.setItem(0, 1, QTableWidgetItem(price[4]))  # 가격

        elif (self.tableWidget.item(1, 0) is None and self.tableWidget.item(0, 0) is not None):  # 첫번째 줄이 비어있지 않으면
            self.tableWidget.setItem(1, 0, QTableWidgetItem(self.Pbtn5.text()))  # 버튼이름
            self.tableWidget.setItem(1, 1, QTableWidgetItem(price[4]))  # 가격

        elif (self.tableWidget.item(1, 0) is not None and self.tableWidget.item(0, 0) is not None
              and self.tableWidget.item(2, 0) is None):  # 첫번째줄과 두번째줄이 모두 비어있지 않으면
            self.tableWidget.setItem(2, 0, QTableWidgetItem(self.Pbtn5.text()))  # 버튼이름
            self.tableWidget.setItem(2, 1, QTableWidgetItem(price[4]))  # 가격

        elif (self.tableWidget.item(2, 0) is not None and self.tableWidget.item(1, 0) is not None and
              self.tableWidget.item(0, 0) is not None and self.tableWidget.item(3,
                                                                                0) is None):  # 첫번째줄과 두번쨰줄 세번쨰줄이 모두 비어있지 않으면
            self.tableWidget.setItem(3, 0, QTableWidgetItem(self.Pbtn5.text()))  # 버튼이름
            self.tableWidget.setItem(3, 1, QTableWidgetItem(price[4]))  # 가격

    def btn6_clicked(self):
        print("클릭됨")

        if (self.tableWidget.item(0, 0) is None):  # 비어있으면 첫번째줄에 넣기
            self.tableWidget.setItem(0, 0, QTableWidgetItem(self.Pbtn6.text()))  # 버튼이름
            self.tableWidget.setItem(0, 1, QTableWidgetItem(price[5]))  # 가격

        elif (self.tableWidget.item(1, 0) is None and self.tableWidget.item(0, 0) is not None):  # 첫번째 줄이 비어있지 않으면
            self.tableWidget.setItem(1, 0, QTableWidgetItem(self.Pbtn6.text()))  # 버튼이름
            self.tableWidget.setItem(1, 1, QTableWidgetItem(price[5]))  # 가격

        elif (self.tableWidget.item(1, 0) is not None and self.tableWidget.item(0, 0) is not None
              and self.tableWidget.item(2, 0) is None):  # 첫번째줄과 두번째줄이 모두 비어있지 않으면
            self.tableWidget.setItem(2, 0, QTableWidgetItem(self.Pbtn6.text()))  # 버튼이름
            self.tableWidget.setItem(2, 1, QTableWidgetItem(price[5]))  # 가격

        elif (self.tableWidget.item(2, 0) is not None and self.tableWidget.item(1, 0) is not None and
              self.tableWidget.item(0, 0) is not None and self.tableWidget.item(3,
                                                                                0) is None):  # 첫번째줄과 두번쨰줄 세번쨰줄이 모두 비어있지 않으면
            self.tableWidget.setItem(3, 0, QTableWidgetItem(self.Pbtn6.text()))  # 버튼이름
            self.tableWidget.setItem(3, 1, QTableWidgetItem(price[5]))  # 가격

    def btn7_clicked(self):
        print("클릭됨")

        if (self.tableWidget.item(0, 0) is None):  # 비어있으면 첫번째줄에 넣기
            self.tableWidget.setItem(0, 0, QTableWidgetItem(self.Pbtn7.text()))  # 버튼이름
            self.tableWidget.setItem(0, 1, QTableWidgetItem(price[6]))  # 가격

        elif (self.tableWidget.item(1, 0) is None and self.tableWidget.item(0, 0) is not None):  # 첫번째 줄이 비어있지 않으면
            self.tableWidget.setItem(1, 0, QTableWidgetItem(self.Pbtn7.text()))  # 버튼이름
            self.tableWidget.setItem(1, 1, QTableWidgetItem(price[6]))  # 가격

        elif (self.tableWidget.item(1, 0) is not None and self.tableWidget.item(0, 0) is not None
              and self.tableWidget.item(2, 0) is None):  # 첫번째줄과 두번째줄이 모두 비어있지 않으면
            self.tableWidget.setItem(2, 0, QTableWidgetItem(self.Pbtn7.text()))  # 버튼이름
            self.tableWidget.setItem(2, 1, QTableWidgetItem(price[6]))  # 가격

        elif (self.tableWidget.item(2, 0) is not None and self.tableWidget.item(1, 0) is not None and
              self.tableWidget.item(0, 0) is not None and self.tableWidget.item(3,
                                                                                0) is None):  # 첫번째줄과 두번쨰줄 세번쨰줄이 모두 비어있지 않으면
            self.tableWidget.setItem(3, 0, QTableWidgetItem(self.Pbtn7.text()))  # 버튼이름
            self.tableWidget.setItem(3, 1, QTableWidgetItem(price[6]))  # 가격

    def btn8_clicked(self):
        print("클릭됨")

        if (self.tableWidget.item(0, 0) is None):  # 비어있으면 첫번째줄에 넣기
            self.tableWidget.setItem(0, 0, QTableWidgetItem(self.Pbtn8.text()))  # 버튼이름
            self.tableWidget.setItem(0, 1, QTableWidgetItem(price[7]))  # 가격

        elif (self.tableWidget.item(1, 0) is None and self.tableWidget.item(0, 0) is not None):  # 첫번째 줄이 비어있지 않으면
            self.tableWidget.setItem(1, 0, QTableWidgetItem(self.Pbtn8.text()))  # 버튼이름
            self.tableWidget.setItem(1, 1, QTableWidgetItem(price[7]))  # 가격

        elif (self.tableWidget.item(1, 0) is not None and self.tableWidget.item(0, 0) is not None
              and self.tableWidget.item(2, 0) is None):  # 첫번째줄과 두번째줄이 모두 비어있지 않으면
            self.tableWidget.setItem(2, 0, QTableWidgetItem(self.Pbtn8.text()))  # 버튼이름
            self.tableWidget.setItem(2, 1, QTableWidgetItem(price[7]))  # 가격

        elif (self.tableWidget.item(2, 0) is not None and self.tableWidget.item(1, 0) is not None and
              self.tableWidget.item(0, 0) is not None and self.tableWidget.item(3,
                                                                                0) is None):  # 첫번째줄과 두번쨰줄 세번쨰줄이 모두 비어있지 않으면
            self.tableWidget.setItem(3, 0, QTableWidgetItem(self.Pbtn8.text()))  # 버튼이름
            self.tableWidget.setItem(3, 1, QTableWidgetItem(price[7]))  # 가격

    def btn9_clicked(self):
        print("클릭됨")

        if (self.tableWidget.item(0, 0) is None):  # 비어있으면 첫번째줄에 넣기
            self.tableWidget.setItem(0, 0, QTableWidgetItem(self.Pbtn9.text()))  # 버튼이름
            self.tableWidget.setItem(0, 1, QTableWidgetItem(price[8]))  # 가격

        elif (self.tableWidget.item(1, 0) is None and self.tableWidget.item(0, 0) is not None):  # 첫번째 줄이 비어있지 않으면
            self.tableWidget.setItem(1, 0, QTableWidgetItem(self.Pbtn9.text()))  # 버튼이름
            self.tableWidget.setItem(1, 1, QTableWidgetItem(price[8]))  # 가격

        elif (self.tableWidget.item(1, 0) is not None and self.tableWidget.item(0, 0) is not None
              and self.tableWidget.item(2, 0) is None):  # 첫번째줄과 두번째줄이 모두 비어있지 않으면
            self.tableWidget.setItem(2, 0, QTableWidgetItem(self.Pbtn9.text()))  # 버튼이름
            self.tableWidget.setItem(2, 1, QTableWidgetItem(price[8]))  # 가격

        elif (self.tableWidget.item(2, 0) is not None and self.tableWidget.item(1, 0) is not None and
              self.tableWidget.item(0, 0) is not None and self.tableWidget.item(3,
                                                                                0) is None):  # 첫번째줄과 두번쨰줄 세번쨰줄이 모두 비어있지 않으면
            self.tableWidget.setItem(3, 0, QTableWidgetItem(self.Pbtn9.text()))  # 버튼이름
            self.tableWidget.setItem(3, 1, QTableWidgetItem(price[8]))  # 가격

    def btn10_clicked(self):
        print("클릭됨")

        if (self.tableWidget.item(0, 0) is None):  # 비어있으면 첫번째줄에 넣기
            self.tableWidget.setItem(0, 0, QTableWidgetItem(self.Pbtn10.text()))  # 버튼이름
            self.tableWidget.setItem(0, 1, QTableWidgetItem(price[9]))  # 가격

        elif (self.tableWidget.item(1, 0) is None and self.tableWidget.item(0, 0) is not None):  # 첫번째 줄이 비어있지 않으면
            self.tableWidget.setItem(1, 0, QTableWidgetItem(self.Pbtn10.text()))  # 버튼이름
            self.tableWidget.setItem(1, 1, QTableWidgetItem(price[9]))  # 가격

        elif (self.tableWidget.item(1, 0) is not None and self.tableWidget.item(0, 0) is not None
              and self.tableWidget.item(2, 0) is None):  # 첫번째줄과 두번째줄이 모두 비어있지 않으면
            self.tableWidget.setItem(2, 0, QTableWidgetItem(self.Pbtn10.text()))  # 버튼이름
            self.tableWidget.setItem(2, 1, QTableWidgetItem(price[9]))  # 가격

        elif (self.tableWidget.item(2, 0) is not None and self.tableWidget.item(1, 0) is not None and
              self.tableWidget.item(0, 0) is not None and self.tableWidget.item(3,
                                                                                0) is None):  # 첫번째줄과 두번쨰줄 세번쨰줄이 모두 비어있지 않으면
            self.tableWidget.setItem(3, 0, QTableWidgetItem(self.Pbtn10.text()))  # 버튼이름
            self.tableWidget.setItem(3, 1, QTableWidgetItem(price[9]))  # 가격

    def btn11_clicked(self):
        print("클릭됨")

        if (self.tableWidget.item(0, 0) is None):  # 비어있으면 첫번째줄에 넣기
            self.tableWidget.setItem(0, 0, QTableWidgetItem(self.Pbtn11.text()))  # 버튼이름
            self.tableWidget.setItem(0, 1, QTableWidgetItem(price[10]))  # 가격

        elif (self.tableWidget.item(1, 0) is None and self.tableWidget.item(0, 0) is not None):  # 첫번째 줄이 비어있지 않으면
            self.tableWidget.setItem(1, 0, QTableWidgetItem(self.Pbtn11.text()))  # 버튼이름
            self.tableWidget.setItem(1, 1, QTableWidgetItem(price[10]))  # 가격

        elif (self.tableWidget.item(1, 0) is not None and self.tableWidget.item(0, 0) is not None
              and self.tableWidget.item(2, 0) is None):  # 첫번째줄과 두번째줄이 모두 비어있지 않으면
            self.tableWidget.setItem(2, 0, QTableWidgetItem(self.Pbtn11.text()))  # 버튼이름
            self.tableWidget.setItem(2, 1, QTableWidgetItem(price[10]))  # 가격

        elif (self.tableWidget.item(2, 0) is not None and self.tableWidget.item(1, 0) is not None and
              self.tableWidget.item(0, 0) is not None and self.tableWidget.item(3,
                                                                                0) is None):  # 첫번째줄과 두번쨰줄 세번쨰줄이 모두 비어있지 않으면
            self.tableWidget.setItem(3, 0, QTableWidgetItem(self.Pbtn11.text()))  # 버튼이름
            self.tableWidget.setItem(3, 1, QTableWidgetItem(price[10]))  # 가격

    def btn12_clicked(self):
        print("클릭됨")

        if (self.tableWidget.item(0, 0) is None):  # 비어있으면 첫번째줄에 넣기
            self.tableWidget.setItem(0, 0, QTableWidgetItem(self.Pbtn12.text()))  # 버튼이름
            self.tableWidget.setItem(0, 1, QTableWidgetItem(price[11]))  # 가격

        elif (self.tableWidget.item(1, 0) is None and self.tableWidget.item(0, 0) is not None):  # 첫번째 줄이 비어있지 않으면
            self.tableWidget.setItem(1, 0, QTableWidgetItem(self.Pbtn12.text()))  # 버튼이름
            self.tableWidget.setItem(1, 1, QTableWidgetItem(price[11]))  # 가격

        elif (self.tableWidget.item(1, 0) is not None and self.tableWidget.item(0, 0) is not None
              and self.tableWidget.item(2, 0) is None):  # 첫번째줄과 두번째줄이 모두 비어있지 않으면
            self.tableWidget.setItem(2, 0, QTableWidgetItem(self.Pbtn12.text()))  # 버튼이름
            self.tableWidget.setItem(2, 1, QTableWidgetItem(price[11]))  # 가격

        elif (self.tableWidget.item(2, 0) is not None and self.tableWidget.item(1, 0) is not None and
              self.tableWidget.item(0, 0) is not None and self.tableWidget.item(3,
                                                                                0) is None):  # 첫번째줄과 두번쨰줄 세번쨰줄이 모두 비어있지 않으면
            self.tableWidget.setItem(3, 0, QTableWidgetItem(self.Pbtn12.text()))  # 버튼이름
            self.tableWidget.setItem(3, 1, QTableWidgetItem(price[11]))  # 가격

    def btn_refresh(self):
        print("취소됨")
        self.tableWidget.clearContents() #테이블의 안의 값만 비움

    def btn_order(self):
        print("주문됨")
        now = datetime.now()
        date_time = now.strftime("%Y/%m/%d, %H:%M")
        ordertime = re.findall("\d+", date_time)

        msgBox = QMessageBox() #메시지박스를 만들어서 실행
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("주문이 완료되었습니다..")
        msgBox.setWindowTitle("주문 현황")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.buttonClicked.connect(self.msgButtonClick)

        if (self.tableWidget.item(0, 0) is None): #첫번째 줄이 비어있으면
            print("비어있습니다.")
        elif (self.tableWidget.item(1, 0) is None and self.tableWidget.item(0, 0) is not None):  # 첫번째 줄이 비어있지 않으면

            db.reference('Restaurant_DB/Real_time/Olive').push({
                "order_food": self.tableWidget.item(0, 0).text(),
                "price": self.tableWidget.item(0, 1).text(),
                "pay_time": ''.join(ordertime),
                "restaurant_name": "Olive"
            })
        elif (self.tableWidget.item(1, 0) is not None and self.tableWidget.item(0, 0) is not None
              and self.tableWidget.item(2, 0) is None):

            db.reference('Restaurant_DB/Real_time/Olive').push({
                "order_food": self.tableWidget.item(0, 0).text(),
                "price": self.tableWidget.item(0, 1).text(),
                "pay_time": ''.join(ordertime),
                "restaurant_name": "Olive"
            })
            db.reference('Restaurant_DB/Real_time/Olive').push({
                "order_food": self.tableWidget.item(1, 0).text(),
                "price": self.tableWidget.item(1, 1).text(),
                "pay_time": ''.join(ordertime),
                "restaurant_name": "Olive"
            })
        elif (self.tableWidget.item(2, 0) is not None and self.tableWidget.item(1, 0) is not None and
              self.tableWidget.item(0, 0) is not None and self.tableWidget.item(3, 0) is None):

            db.reference('Restaurant_DB/Real_time/Olive').push({
                "order_food": self.tableWidget.item(0, 0).text(),
                "price": self.tableWidget.item(0, 1).text(),
                "pay_time": ''.join(ordertime),
                "restaurant_name": "Olive"
            })
            db.reference('Restaurant_DB/Real_time/Olive').push({
                "order_food":self.tableWidget.item(1,0).text(),
                "price":self.tableWidget.item(1,1).text(),
                "pay_time":''.join(ordertime),
                "restaurant_name":"Olive"
            })

            db.reference('Restaurant_DB/Real_time/Olive').push({
                "order_food": self.tableWidget.item(2, 0).text(),
                "price": self.tableWidget.item(2, 1).text(),
                "pay_time": ''.join(ordertime),
                "restaurant_name": "Olive"
            })

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')

    def msgButtonClick(i):
        print("정상작동 주문완료")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()