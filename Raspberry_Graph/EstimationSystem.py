from tkinter import *
import tkinter.ttk
import numpy as np
from time import sleep
from firebase import firebase
from tkinter import ttk
import sys
import threading
import random
import time
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import animation

firebase = firebase.FirebaseApplication("https://graduate-work-462b3.firebaseio.com/", None)

ref1 = firebase.get('Waiting_time_DB/TIP/Waiting_time', None)
ref2 = firebase.get('Waiting_time_DB/Olive/Waiting_time', None)
ref3 = firebase.get('Waiting_time_DB/Sanyung/Waiting_time', None)
ref4 = firebase.get('Waiting_time_DB/JongHap/Waiting_time', None)

result = firebase.get('Distribution_DB/Kpu', None)
LARGE_FONT = ("Verdana", 12)

fig = plt.figure()  # figure(도표) 생성

ax = plt.subplot(111, xlim=(0, 10), ylim=(0, 15)) # 그래프 생성

ax.set_title('Distribution Data')

ax.set_ylabel('PeopleNumber');

defaultcolor = '#%02x%02x%02x' % (240, 240, 237)

#그래프 표시 최대치 설정
max_points = 10
max1_points = 10
max2_points = 10
max3_points = 10

line, = ax.plot([], [], lw=1, c='blue', marker='d', ms=2,label='TIP')
line1, = ax.plot([], [], lw=1, c='red', marker='d', ms=2,label='Olive')
line2, = ax.plot([], [], lw=1, c='green', marker='d', ms=2,label='Sanyung')
line3, = ax.plot([], [], lw=1, c='cyan', marker='d', ms=2,label='JongHap')
plt.legend(loc='upper left')

line, = ax.plot(np.arange(max_points),
                np.ones(max_points, dtype=np.float) * np.nan, lw=1, c='blue', ms=1)
line1, = ax.plot(np.arange(max1_points),
                  np.ones(max1_points, dtype=np.float) * np.nan, lw=1, c='red', ms=1)
line2, = ax.plot(np.arange(max2_points),
                  np.ones(max2_points, dtype=np.float) * np.nan, lw=1, c='green', ms=1)
line3, = ax.plot(np.arange(max3_points),
                  np.ones(max3_points, dtype=np.float) * np.nan, lw=1, c='cyan', ms=1)

lines=[line,line1,line2,line3]

def init():
    return lines

def animate(i):
    y = firebase.get('Distribution_DB/TIP/people_number', None)
    old_y = line.get_ydata()
    new_y = np.r_[old_y[1:], y]
    line.set_ydata(new_y)

    y1 = firebase.get('Distribution_DB/Olive/people_number', None)
    old_y1 = line1.get_ydata()
    new_y1 = np.r_[old_y1[1:], y1]
    line1.set_ydata(new_y1)

    y2 = firebase.get('Distribution_DB/Sanyung/people_number', None)
    old_y2 = line2.get_ydata()
    new_y2 = np.r_[old_y2[1:], y2]
    line2.set_ydata(new_y2)

    y3 = firebase.get('Distribution_DB/JongHap/people_number', None)
    old_y3 = line3.get_ydata()
    new_y3 = np.r_[old_y3[1:], y3]
    line3.set_ydata(new_y3)

    return lines


root=tkinter.Tk()
root.title("ReealTime Estimated System")
root.geometry("1024x500")
root.resizable(False, False)

#frame 설정
left_frame = Frame(root, width=200, height=400, bg=defaultcolor)
left_frame.grid(row=1, column=0, padx=10, pady=5)
right_frame = Frame(root, width=650, height=400, bg=defaultcolor)
right_frame.grid(row=1, column=1, padx=10, pady=5)

style = ttk.Style(right_frame)
# set ttk theme to "clam" which support the fieldbackground option
style.theme_use("clam")
style.configure("Treeview", background="white",
                fieldbackground="white", foreground="white",rowheight=40)

lbl = tkinter.Label(right_frame, text="WaitingTime",font=LARGE_FONT)
lbl.pack()

"""
toplabel=Label(top_frame ,text="Distribution and WaitingTime",font=LARGE_FONT)
toplabel.pack()
"""

# 표에 삽입될 데이터
treelist=[("TIP", ref1), ("Olive", ref2), ("Sanyung", ref3), ("JongHap", ref4)]

#  표 생성하기. colums는 컬럼 이름, displaycolums는 실행될 때 보여지는 순서다.
treeview = tkinter.ttk.Treeview(right_frame, columns=["one", "two"], displaycolumns=["one", "two"])
treeview.pack()

# 각 컬럼 설정. 컬럼 이름, 컬럼 넓이, 정렬 등
treeview.column("#0", width=100, )
treeview.heading("#0", text="Index")

treeview.column("#1", width=100, anchor="center")
treeview.heading("one", text="Restaurant", anchor="center")

treeview.column("#2", width=100, anchor="center")
treeview.heading("two", text="Time(분)", anchor="center")


for i in range(len(treelist)):
    treeview.insert('', 'end', text=i+1, values=treelist[i], iid=str(i))

def ChangeTable():
    print("값변동")
    ref5 = firebase.get('Waiting_time_DB/TIP/Waiting_time', None)
    ref6 = firebase.get('Waiting_time_DB/Olive/Waiting_time', None)
    ref7 = firebase.get('Waiting_time_DB/Sanyung/Waiting_time', None)
    ref8 = firebase.get('Waiting_time_DB/JongHap/Waiting_time', None)

    treelist = [("TIP", ref5), ("Olive", ref6), ("Sanyung", ref7), ("JongHap", ref8)]
    for i in range(len(treelist)):
        treeview.item(str(i),values=treelist[i])

#프레임 표시부분
canvas = FigureCanvasTkAgg(fig, master=left_frame)  #
canvas.get_tk_widget().grid(column=0, row=1)
anim=animation.FuncAnimation(fig, animate, init_func=init, frames=50, interval=200, blit=False)

while(True):
    ChangeTable()
    root.update()
    time.sleep(0.5)

root.mainloop()
