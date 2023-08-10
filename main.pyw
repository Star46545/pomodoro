import tkinter as tk
import main_ui
import time_box
import json
import time
import os
from threading import Thread
from tkinter import messagebox


def getPath():
    return os.path.dirname(os.path.abspath(__file__))


class Config:
    def __init__(self, path: str = None) -> None:
        if path is not None and os.path.exists(path) and os.path.isfile(path) and os.access(path, os.R_OK) and os.access(path, os.W_OK):
            self.path = path
            self.getConfig()
        else:
            self.path = f"{getPath()}\\config.json"
            self.config = {"black theme": False,
                           "time list": [0, 0, 0, 0, 25, 0],
                           "time mode": 1}

    def getConfig(self):
        with open(self.path, 'r') as f:
            self.config = json.loads(f.read())

    def saveConfig(self):
        with open(self.path, 'w') as f:
            f.write(json.dumps(self.config))


class Tools:
    def month_to_day(year, month):
        # 获取每个月的
        is_leap_year = (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
        days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if is_leap_year:
            days[1] = 29
        return sum(days[:month-1])


class Ui:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.black_theme = self.config.config["black theme"]
        self.timeList = self.config.config["time list"]
        self.canStart = True
        self.endtime = None
        self.Time = time_box.Time(
            self.timeList[0], self.timeList[1], self.timeList[2], self.timeList[3], self.timeList[4], self.timeList[5])

        self.tk = tk.Tk()
        self.tk.title("设置并启动番茄钟")

        # 选择结束于某时长
        self.radioButtonVariable = tk.IntVar()
        self.radioButtonVariable.set(self.config.config["time mode"])
        self.stopAt_radioButton = tk.Radiobutton(
            self.tk, text="结束于", variable=self.radioButtonVariable, value=0)
        self.stopAt_radioButton.grid(row=0, column=0)

        # 选择持续某时长
        self.keepLockFor_radioButton = tk.Radiobutton(
            self.tk, text="持续", variable=self.radioButtonVariable, value=1)
        self.keepLockFor_radioButton.grid(row=0, column=1)

        # 选择浅色模式或者暗色模式
        self.theme_radioButtonVariable = tk.IntVar()
        self.theme_radioButtonVariable.set(
            {False: 0, True: 1}[self.black_theme])
        self.theme_white = tk.Radiobutton(
            self.tk, text="浅色模式", variable=self.theme_radioButtonVariable, value=0)
        self.theme_white.grid(row=1, column=0)
        self.theme_black = tk.Radiobutton(
            self.tk, text="暗色模式", variable=self.theme_radioButtonVariable, value=1)
        self.theme_black.grid(row=1, column=1)

        # 时间控件，自制
        self.timeBox = time_box.TimeBox(self.tk, self.Time)
        self.timeBox.grid(row=2, column=0, columnspan=2)

        self.start_button = tk.Button(self.tk, text="开始", padx=25, command=lambda: [
                                      self.set_theme_type(), self.set_duration(), self.saveConfig(), self.start()])
        self.start_button.grid(row=3, column=0, columnspan=12)

        self.changeEdge()
        # radio button被按下的时候，改变界限
        self.radioButtonVariable.trace("w", lambda *args: self.changeEdge())

    def set_theme_type(self):
        # 由于在上面的代码中，radio button的浅色的值为0，深色的值为1，所以可以用列表来快速设置
        self.config.config["black theme"] = [
            False, True][self.theme_radioButtonVariable.get()]

    def set_duration(self):
        # 设置持续时长
        try:
            self.timeBox.getTime()
            self.config.config["time list"] = self.Time.timeList
            self.canStart = True
        except ValueError:
            self.canStart = False
            return

        try:
            self.duration = self.Time.getTimestamp(
                self.radioButtonVariable.get() + 1)
        except ValueError:
            messagebox.showerror("错误", "时间不可用，请调整")
            self.canStart = False
            return

        if self.canStart:
            timestamp = self.duration
            if self.radioButtonVariable.get() == 0:
                if time.time() < timestamp:
                    self.endtime = timestamp
                else:
                    messagebox.showerror("错误", "结束时间早于现在")
                    return
            else:
                self.endtime = int(time.time()) + timestamp

    def saveConfig(self):
        if self.canStart:
            self.config.saveConfig()
            with open(f"{getPath()}\\task.json", 'w') as f:
                taskData = {"end time": self.endtime,
                            "black theme": self.config.config["black theme"],
                            }
                f.write(json.dumps(taskData))

    def start(self):
        if self.canStart:
            print(time.localtime(self.endtime))
            # lock_ui = main_ui.Ui(endtime, self.config.config["black theme"])
            # lock_ui.begin()
            self.tk.destroy()
            main_ui.Ui(self.endtime, self.config.config["black theme"]).begin()

    def changeEdge(self):
        self.config.config["time mode"] = self.radioButtonVariable.get()
        if self.radioButtonVariable.get() == 0:
            self.timeBox.setEdge(time.localtime(time.time())[
                                 :6], [None, 12, 31, 23, 59, 59])
        else:
            self.timeBox.setEdge([0, 0, 0, 0, 0, 0], [
                                 None, 12, 31, 23, 59, 59])


if __name__ == "__main__":
    config = Config(f'{getPath()}\\config.json')
    ui = Ui(config)
    ui.tk.mainloop()
