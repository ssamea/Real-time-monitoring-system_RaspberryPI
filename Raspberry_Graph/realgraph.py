from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import time
import random
from firebase import firebase

firebase = firebase.FirebaseApplication("https://graduate-work-462b3.firebaseio.com/", None)

result = firebase.get('Distribution_DB/Kpu', None)

fig = plt.figure(figsize=(7,7)) #figure(도표) 생성

ax = plt.subplot(221, xlim=(0, 20), ylim=(0, 10))
ax1 = plt.subplot(222, xlim=(0, 20), ylim=(0, 10))
ax2 = plt.subplot(223, xlim=(0, 20), ylim=(0, 10))
ax3 = plt.subplot(224, xlim=(0, 20), ylim=(0, 10))

ax.set_title('TIP')
ax1.set_title('Olive')
ax2.set_title('Sanyung')
ax3.set_title('Edong')

ax.set_ylabel('the number of persons'); 
ax1.set_ylabel('the number of persons'); 
ax2.set_ylabel('the number of persons'); 
ax3.set_ylabel('the number of persons');

max_points = 10
max1_points = 10
max2_points = 10
max3_points = 10

line, = ax.plot([], [], lw=1, c='blue', marker='d',ms=2)
line1, = ax1.plot([], [], lw=1, c='red', marker='d',ms=2)
line2, = ax2.plot([], [], lw=1, c='green', marker='d',ms=2)
line3, = ax3.plot([], [], lw=1, c='yellow', marker='d',ms=2)

line, = ax.plot(np.arange(max_points), 
                np.ones(max_points, dtype=np.float)*np.nan, lw=1, c='blue',ms=1)
line1, = ax1.plot(np.arange(max1_points), 
                np.ones(max1_points, dtype=np.float)*np.nan, lw=1, c='red',ms=1)
line2, = ax2.plot(np.arange(max2_points), 
                np.ones(max2_points, dtype=np.float)*np.nan, lw=1, c='green',ms=1)
line3, = ax3.plot(np.arange(max3_points), 
                np.ones(max3_points, dtype=np.float)*np.nan, lw=1, c='yellow',ms=1)

def init():
	return line
def init1():
	return line1
def init2():
	return line2
def init3():
	return line3

def animate(i):
	y = firebase.get('Distribution_DB/Kpu/people_number', None)
	old_y = line.get_ydata()
	new_y = np.r_[old_y[1:], y]
	line.set_ydata(new_y)

	return line
def animate1(i):
	y1 = firebase.get('Distribution_DB/Olive/people_number', None)
	#y1 = random.randint(0,10)
	old_y1 = line1.get_ydata()
	new_y1 = np.r_[old_y1[1:], y1]
	line1.set_ydata(new_y1)

	return line1

def animate2(i):
	y2 = firebase.get('Distribution_DB/Sanyung/people_number', None)
	#y2 = random.randint(0,10)
	old_y2 = line2.get_ydata()
	new_y2 = np.r_[old_y2[1:], y2]
	line2.set_ydata(new_y2)

	return line2
	
def animate3(i):
	y3 = firebase.get('Distribution_DB/Edong/people_number', None)
	#y3 = random.randint(0,10)
	old_y3 = line3.get_ydata()
	new_y3 = np.r_[old_y3[1:], y3]
	line3.set_ydata(new_y3)

	return line3

anim = animation.FuncAnimation(fig, animate , init_func= init ,frames=50,interval=200, blit=False)
anim1 = animation.FuncAnimation(fig, animate1 , init_func= init2 ,frames=50,interval=200, blit=False)
anim2 = animation.FuncAnimation(fig, animate2 , init_func= init2 ,frames=50,interval=200, blit=False)
anim3 = animation.FuncAnimation(fig, animate3 , init_func= init3 ,frames=50,interval=200, blit=False)


plt.tight_layout()
plt.show()


