import tkinter as tk
import threading
import time
from pyautogui import size, keyDown, keyUp


class Ui:
    def __init__(self, endtime, black_color=False) -> None:
        # 基本变量
        self.endtime = endtime
        self.run = False
        self.finished = False
        self.black_color = black_color
        self.press_keys = ['shift', 'ctrl', 'alt', 'windows']

        # 窗口设置
        self.window = tk.Tk()
        self.window.attributes("-topmost", True)
        self.window.attributes("-fullscreen", True)
        self.window.protocol("WM_DELETE_WINDOW", lambda: None)
        self.window.title("番茄钟")

        # 设置框架，点击窗口变色用
        self.frame = tk.Frame(self.window, width=size()[0], height=size()[1])
        self.frame.bind(
            "<Button-1>", self.change_color)
        self.frame.pack()

        # 时间标签
        self.time = tk.StringVar()
        self.time.set("00:00")
        self.timelabel = tk.Label(
            self.frame, textvariable=self.time, font=("Consolas", 200))
        self.timelabel.bind("<Button-1>", self.change_color)
        # 将时间放在屏幕正中间
        self.timelabel.place(anchor="center", relx=0.5, rely=0.5)

        # 结束时间标签
        self.endtime_format = f'将在{time.strftime("%H:%M", time.localtime(endtime))}结束'
        self.endtime_label = tk.Label(
            self.frame, text=self.endtime_format, font=("Consolas", 20))
        self.endtime_label.bind("<Button-1>", self.change_color)
        self.endtime_label.place(anchor="center", relx=0.5, rely=0.65)

        # 按下功能键
        for key in self.press_keys:
            keyDown(key)

    def begin(self):
        self.run = True
        threading.Thread(target=self.autoChange).start()
        print('mainloop')
        self.window.mainloop()

    def autoChange(self):
        if self.finished:
            self.run = False
            self.window.destroy()
            for key in self.press_keys:
                keyUp(key)
            return

        if self.run:
            self.time.set(self.getTime())
            self.window.after(1000, self.autoChange)

    def keep_topmost_and_press_key(self):
        while True:
            time.sleep(0.3)
            self.window.attributes("-topmost", True)
            for key in self.press_keys:
                keyUp(key)
                keyDown(key)

    def getTime(self):
        time_left = self.endtime - time.time()
        if time_left < 0:
            self.finished = True
            return "00:00"
        else:
            minute = int(time_left / 60)
            second = int(time_left % 60)
            return f"{minute:02d}:{second:02d}"

    def change_color(self, event):
        self.black_color = not self.black_color
        if self.black_color:
            self.frame.configure(bg="#000000")
            self.timelabel.configure(fg="#FFFFFF", bg="#000000")
            self.endtime_label.configure(fg="#FFFFFF", bg="#000000")
        else:
            self.frame.configure(bg="#FFFFFF")
            self.timelabel.configure(fg="#000000", bg="#FFFFFF")
            self.endtime_label.configure(fg="#000000", bg="#FFFFFF")


if __name__ == "__main__":
    ui = Ui(time.time() + 1500)
    # ui = Ui(time.time() + 3)
    ui.begin()
