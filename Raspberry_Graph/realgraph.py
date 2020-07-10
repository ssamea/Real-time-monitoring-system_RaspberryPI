import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter.ttk
import tkinter as tk
from tkinter import ttk

from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
from firebase import firebase

firebase = firebase.FirebaseApplication("https://graduate-work-462b3.firebaseio.com/", None)

result = firebase.get('Distribution_DB/Kpu', None)
LARGE_FONT = ("Verdana", 12)
fig = plt.figure()  # figure(도표) 생성

ax = plt.subplot(221, xlim=(0, 10), ylim=(0, 15))
ax1 = plt.subplot(222, xlim=(0, 10), ylim=(0, 15))
ax2 = plt.subplot(223, xlim=(0, 10), ylim=(0, 15))
ax3 = plt.subplot(224, xlim=(0, 10), ylim=(0, 15))



ax.set_title('TIP')
ax1.set_title('Olive')
#ax2.set_title('Sanyung')
#ax3.set_title('JongHap')

#ax.set_ylabel('TIP');
#ax1.set_ylabel('Olive');
ax2.set_xlabel('Sanyung');
ax3.set_xlabel('JongHap');

max_points = 10
max1_points = 10
max2_points = 10
max3_points = 10

line, = ax.plot([], [], lw=1, c='blue', marker='d', ms=2)
line1, = ax1.plot([], [], lw=1, c='red', marker='d', ms=2)
line2, = ax2.plot([], [], lw=1, c='green', marker='d', ms=2)
line3, = ax3.plot([], [], lw=1, c='yellow', marker='d', ms=2)

line, = ax.plot(np.arange(max_points),
                np.ones(max_points, dtype=np.float) * np.nan, lw=1, c='blue', ms=1)
line1, = ax1.plot(np.arange(max1_points),
                  np.ones(max1_points, dtype=np.float) * np.nan, lw=1, c='red', ms=1)
line2, = ax2.plot(np.arange(max2_points),
                  np.ones(max2_points, dtype=np.float) * np.nan, lw=1, c='green', ms=1)
line3, = ax3.plot(np.arange(max3_points),
                  np.ones(max3_points, dtype=np.float) * np.nan, lw=1, c='yellow', ms=1)

lines=[line,line1,line2,line3]

def init():
    return lines

def animate(i):
    y = firebase.get('Distribution_DB/Tip/people_number', None)
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

class Realtime(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Estimation System")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne ,PageTwo, PageThree):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=("Sanyung"), font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="TIP",
                             command=lambda: controller.show_frame(PageThree))
        button1.pack(side='left')

        button2 = ttk.Button(self, text="JongHap",
                             command=lambda :controller.show_frame(PageOne))
        button2.pack(side='right')

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=("JongHap"), font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Sanyung",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack(side='left')

        button2 = ttk.Button(self, text="Olive",
                             command=lambda :controller.show_frame(PageTwo))
        button2.pack(side='right')

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=("Olive"), font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="JongHap",
                             command=lambda: controller.show_frame(PageOne))
        button1.pack(side='left')

        button2 = ttk.Button(self, text="Tip",
                             command=lambda: controller.show_frame(PageThree))
        button2.pack(side='right')

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=("Tip"), font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Olive",
                             command=lambda: controller.show_frame(PageTwo))
        button1.pack(side='left')

        button2 = ttk.Button(self, text="Sanyung",
                             command=lambda: controller.show_frame(StartPage))
        button2.pack(side='right')

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

app = Realtime()
anim = animation.FuncAnimation(fig, animate, init_func=init, frames=50, interval=200, blit=False)
app.mainloop()
