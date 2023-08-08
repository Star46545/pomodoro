import tkinter as tk
import main_ui
import time_box
import json
import time


class Config:
    def __init__(self, path: str = None) -> None:
        if path is not None:
            self.path = path
            self.config = {}
        else:
            self.config = {"black theme": False,
                           "time list": [0, 0, 0, 0, 0, 0]}

    def getConfig(self):
        with open(self.path, 'r') as f:
            self.config = json.load(f.read())


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
        self.duration = self.config.config["time list"]
        self.canStart = True
        self.Time = time_box.Time(
            self.duration[0], self.duration[1], self.duration[2], self.duration[3], self.duration[4], self.duration[5])

        self.tk = tk.Tk()
        self.tk.title("设置并启动番茄钟")

        # 选择结束于某时长
        self.radioButtonVariable = tk.IntVar()
        self.stopAt_radioButton = tk.Radiobutton(
            self.tk, text="结束于", variable=self.radioButtonVariable, value=0)
        self.stopAt_radioButton.grid(row=0, column=0)
        self.stopAt_radioButton.select()

        # 选择持续某时长
        self.keepLockFor_radioButton = tk.Radiobutton(
            self.tk, text="持续", variable=self.radioButtonVariable, value=1)
        self.keepLockFor_radioButton.grid(row=0, column=1)

        # 选择浅色模式或者暗色模式
        self.theme_radioButtonVariable = tk.IntVar()
        self.theme_white = tk.Radiobutton(
            self.tk, text="浅色模式", variable=self.theme_radioButtonVariable, value=0)
        self.theme_white.select()
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

    def set_theme_type(self):
        # 由于在上面的代码中，radio button的浅色的值为0，深色的值为1，所以可以用列表来快速设置
        self.config.config["black theme"] = [
            False, True][self.theme_radioButtonVariable.get()]

    def set_duration(self):
        # 设置持续时长
        try:
            self.timeBox.setTime()
            self.config.config["time list"] = self.Time.timeList
            self.canStart = True
        except ValueError:
            self.canStart = False
            return

        self.duration = self.Time.getTimestamp(
            self.radioButtonVariable.get() + 1)

    def saveConfig(self):
        with open("config.json", 'w') as f:
            f.write(json.dumps(self.config.config))

    def start(self):
        if self.canStart:
            timestamp = self.duration
            if self.radioButtonVariable.get() == 0:
                endtime = timestamp
            else:
                endtime = int(time.time()) + timestamp

            lock_ui = main_ui.Ui(endtime, self.config.config["black theme"])
            lock_ui.window.begin()


if __name__ == "__main__":
    config = Config()
    ui = Ui(config)
    ui.tk.mainloop()
