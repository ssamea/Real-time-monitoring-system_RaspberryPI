import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datetime import datetime
import re
from firebase_admin import db
import math
import firebase_admin
from firebase_admin import credentials
from google.cloud import storage
import pyrebase

#인증
cred = credentials.Certificate('myKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://graduate-work-462b3.firebaseio.com/'
})

config = {
    "apiKey": "AIzaSyA8dTQrxY9oxS6azG6j3sChjtmvHdnr7Co",
    "authDomain": "graduate-work-462b3.firebaseapp.com",
    "databaseURL": "https://graduate-work-462b3.firebaseio.com",
    "projectId": "graduate-work-462b3",
    "storageBucket": "graduate-work-462b3.appspot.com",
    "messagingSenderId": "48451857603",
    "appId": "1:48451857603:web:808bdaad60b699d6b8c676",
    "measurementId": "G-JCEHY71WY4"
};
firebase= pyrebase.initialize_app(config)
storage=firebase.storage()
path_on_cloud ="food_img/Olive/"

name=[]
price=[]
food_img=[]

#firebase 데이터 값 가져오기
db_menu = db.reference("Menu_DB/Olive").get()

for R_key in db_menu:
    price.append(db.reference("Menu_DB/Olive/%s/price" %R_key).get())
    name.append(db.reference("Menu_DB/Olive/%s/menu_name" % R_key).get())


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

        self.setWindowTitle("Olive")
        self.setGeometry(800, 200, 600, 630)    #크기설정 (x좌표,y좌표,너비,높이)
        #메뉴 최대 갯수 지정
        self.btnnum = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']
        self.btnlist=[]
        self.Piclist=[]

        for i in range(0,len(name)):
            storage.child(path_on_cloud + str(i+1) + ".jpg").download("img" + str(i+1) + ".jpg", str(i+1) + ".jpg")
            self.Piclist.append(PicButton(QPixmap( self.btnnum[i] + '.jpg')))
            self.Piclist[i].setMaximumHeight(100)
            self.Piclist[i].setMaximumWidth(100)

            self.btnlist.append(QPushButton(name[i]))
            self.btnlist[i].clicked.connect(lambda state, button=self.btnlist[i] : self.btn_clicked(state,button))


        self.Obtn1 = QPushButton("주문하기")
        self.Obtn1.setMaximumHeight(150)
        self.Obtn1.clicked.connect(self.btn_order)

        self.Obtn2 = QPushButton("취소하기")
        self.Obtn2.setMaximumHeight(150)
        self.Obtn2.clicked.connect(self.btn_refresh)

        layout1 = QGridLayout() #GUI 컨텐츠들을 배치할 레이아웃 설정

        for i in range(0,len(name)):
            layout1.addWidget(self.Piclist[i],math.floor(i/4)*2,i%4)
            layout1.addWidget(self.btnlist[i], math.floor(i / 4) * 2+1, i % 4)

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

    def btn_clicked(self,state,button):
        print("클릭됨")

        a=button.text()
        k=name.index(a)

        if (self.tableWidget.item(0, 0) is None):  # 비어있으면 첫번째줄에 넣기
            self.tableWidget.setItem(0, 0, QTableWidgetItem(a))  # 버튼이름
            self.tableWidget.setItem(0, 1, QTableWidgetItem(str(price[k])))  # 가격

        elif (self.tableWidget.item(1, 0) is None and self.tableWidget.item(0, 0) is not None):  # 첫번째 줄이 비어있지 않으면
            self.tableWidget.setItem(1, 0, QTableWidgetItem(a))  # 버튼이름
            self.tableWidget.setItem(1, 1, QTableWidgetItem(str(price[k])))  # 가격

        elif (self.tableWidget.item(1, 0) is not None and self.tableWidget.item(0, 0) is not None
              and self.tableWidget.item(2, 0) is None):  # 첫번째줄과 두번째줄이 모두 비어있지 않으면
            self.tableWidget.setItem(2, 0, QTableWidgetItem(a))  # 버튼이름
            self.tableWidget.setItem(2, 1, QTableWidgetItem(str(price[k])))  # 가격


        elif (self.tableWidget.item(2, 0) is not None and self.tableWidget.item(1, 0) is not None and
              self.tableWidget.item(0, 0) is not None and self.tableWidget.item(3, 0) is None):  # 첫번째줄과 두번쨰줄 세번쨰줄이 모두 비어있지 않으면
            self.tableWidget.setItem(3, 0, QTableWidgetItem(a))  # 버튼이름
            self.tableWidget.setItem(3, 1, QTableWidgetItem(str(price[k])))  # 가격



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
                "price": self.tableWidget.item(0, 1).text()+"원",
                "pay_time": ''.join(ordertime),
                "restaurant_name": "Olive"
            })
        elif (self.tableWidget.item(1, 0) is not None and self.tableWidget.item(0, 0) is not None
              and self.tableWidget.item(2, 0) is None):

            db.reference('Restaurant_DB/Real_time/Olive').push({
                "order_food": self.tableWidget.item(0, 0).text(),
                "price": self.tableWidget.item(0, 1).text()+"원",
                "pay_time": ''.join(ordertime),
                "restaurant_name": "Olive"
            })
            db.reference('Restaurant_DB/Real_time/Olive').push({
                "order_food": self.tableWidget.item(1, 0).text(),
                "price": self.tableWidget.item(1, 1).text()+"원",
                "pay_time": ''.join(ordertime),
                "restaurant_name": "Olive"
            })
        elif (self.tableWidget.item(2, 0) is not None and self.tableWidget.item(1, 0) is not None and
              self.tableWidget.item(0, 0) is not None and self.tableWidget.item(3, 0) is None):

            db.reference('Restaurant_DB/Real_time/Olive').push({
                "order_food": self.tableWidget.item(0, 0).text(),
                "price": self.tableWidget.item(0, 1).text()+"원",
                "pay_time": ''.join(ordertime),
                "restaurant_name": "Olive"
            })
            db.reference('Restaurant_DB/Real_time/Olive').push({
                "order_food":self.tableWidget.item(1,0).text(),
                "price":self.tableWidget.item(1,1).text()+"원",
                "pay_time":''.join(ordertime),
                "restaurant_name":"Olive"
            })

            db.reference('Restaurant_DB/Real_time/Olive').push({
                "order_food": self.tableWidget.item(2, 0).text(),
                "price": self.tableWidget.item(2, 1).text()+"원",
                "pay_time": ''.join(ordertime),
                "restaurant_name": "Olive"
            })
        elif (self.tableWidget.item(2, 0) is not None and self.tableWidget.item(1, 0) is not None and
              self.tableWidget.item(0, 0) is not None and self.tableWidget.item(3, 0) is not None): #전부 차있으면

            db.reference('Restaurant_DB/Real_time/Olive').push({
                "order_food": self.tableWidget.item(0, 0).text(),
                "price": self.tableWidget.item(0, 1).text()+"원",
                "pay_time": ''.join(ordertime),
                "restaurant_name": "Olive"
            })
            db.reference('Restaurant_DB/Real_time/Olive').push({
                "order_food":self.tableWidget.item(1,0).text(),
                "price":self.tableWidget.item(1,1).text()+"원",
                "pay_time":''.join(ordertime),
                "restaurant_name":"Olive"
            })

            db.reference('Restaurant_DB/Real_time/Olive').push({
                "order_food": self.tableWidget.item(2, 0).text(),
                "price": self.tableWidget.item(2, 1).text()+"원",
                "pay_time": ''.join(ordertime),
                "restaurant_name": "Olive"
            })

            db.reference('Restaurant_DB/Real_time/Olive').push({
                "order_food": self.tableWidget.item(3, 0).text(),
                "price": self.tableWidget.item(3, 1).text() + "원",
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