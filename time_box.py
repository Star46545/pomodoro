import tkinter as tk
import time


class Time:
    def __init__(self, year: int = 0, month: int = 0, day: int = 0, hour: int = 0, minute: int = 0, second: int = 0) -> None:
        self.timeList = [year, month, day, hour, minute, second]
        self.days_in_every_month = [31, 28, 31,
                                    30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.timestamp = self.getTimestamp(2)

    def setTime(self, year: int, month: int, day: int, hour: int, minute: int, second: int) -> None:
        self.timeList = [year, month, day, hour, minute, second]

    def dayInYear(self) -> int:
        days = 0
        for year in range(self.timeList[0]):
            year += 1
            if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
                days += 366
            else:
                days += 365
        return days

    def dayInMonth(self) -> int:
        days = 0
        for month in range(self.timeList[1]):
            days += self.days_in_every_month[month]
        return days

    def date_isUseful(self) -> bool:
        useful = True
        # 月份小于1或大于12
        if self.timeList[1] > 12 or self.timeList[1] < 1:
            useful = False
        # 天数小于1或大于相应月份最大天数
        elif self.timeList[2] > self.days_in_every_month[self.timeList[1]-1] or self.timeList[2] < 1:
            useful = False
        # 小时小于0或大于23
        elif self.timeList[3] > 23 or self.timeList[3] < 0:
            useful = False
        # 分钟小于0或大于59
        elif self.timeList[4] > 59 or self.timeList[4] < 0:
            useful = False
        # 秒数小于0或大于59
        elif self.timeList[5] > 59 or self.timeList[5] < 0:
            useful = False
        return useful

    def time_isUseful(self) -> bool:
        useful = True
        # 月份小于0或大于12
        if self.timeList[1] > 12 or self.timeList[1] < 0:
            useful = False
        # 天数小于0或大于相应月份最大天数
        elif self.timeList[2] > self.days_in_every_month[self.timeList[1]-1] or self.timeList[2] < 0:
            useful = False
        # 小时小于0或大于23
        elif self.timeList[3] > 23 or self.timeList[3] < 0:
            useful = False
        # 分钟小于0或大于59
        elif self.timeList[4] > 59 or self.timeList[4] < 0:
            useful = False
        # 秒数小于0或大于59
        elif self.timeList[5] > 59 or self.timeList[5] < 0:
            useful = False
        return useful

    def getTimestamp(self, mode: int = 1) -> int:
        """将对象时间列表转为时间戳

        Args:
            mode (int, optional): 转换时时间列表是时长还是时间，1表示时长，2表示时间. Defaults to 1.

        Raises:
            ValueError: 时间列表中的时间数字不可用
            ValueError: 时间列表中的时间数字不可用
            TypeError: mode参数错误

        Returns:
            int: 时间参数错误
        """
        if mode == 1:
            if self.date_isUseful():
                timeString = ''
                for time_ in self.timeList:
                    timeString += f'{time_} '
                self.timestamp = time.mktime(
                    time.strptime(timeString, "%Y %m %d %H %M %S "))
            else:
                raise ValueError("时间不可用")
        elif mode == 2:
            if self.time_isUseful():
                self.timestamp = (self.dayInYear() + self.dayInMonth(
                ) + self.timeList[2])*24*60*60 + self.timeList[3]*60*60 + self.timeList[4] * 60 + self.timeList[5]
            else:
                raise ValueError("时间不可用")
            return self.timestamp
        else:
            raise TypeError("mode参数错误，用法请见文档。")


class adjustTimeButtonGroup(tk.Frame):
    def __init__(self, master, entry: tk.Entry, min_: int, max_: int,):
        super().__init__(master)
        self.min = min_
        self.max = max_
        self.addButton = tk.Button(
            self, text='▲', command=lambda: self.add(entry), width=1, height=1)
        self.subtractButton = tk.Button(
            self, text='▼', command=lambda: self.subtract(entry), width=1, height=1)
        self.addButton.grid(row=0, column=0)
        self.subtractButton.grid(row=0, column=1)

    def setEdge(self, min_, max_):
        self.min = min_
        self.max = max_

    def add(self, entry: tk.Entry):
        try:
            old = int(entry.get())
            if old < self.max:
                entry.delete(0, tk.END)
                entry.insert(0, str(old+1))
        except ValueError:
            pass

    def subtract(self, entry: tk.Entry):
        try:
            old = int(entry.get())
            if old > self.min:
                entry.delete(0, tk.END)
                entry.insert(0, str(old-1))
        except ValueError:
            pass


class TimeBox(tk.Frame):
    def __init__(self, master, time_: Time = Time()) -> None:
        super().__init__(master)
        self.time = time_

        # 设置entry
        self.timeInputEntry_year = tk.Entry(self, width=4)
        self.timeInputEntry_month = tk.Entry(self, width=2)
        self.timeInputEntry_day = tk.Entry(self, width=2)
        self.timeInputEntry_hour = tk.Entry(self, width=2)
        self.timeInputEntry_minute = tk.Entry(self, width=2)
        self.timeInputEntry_second = tk.Entry(self, width=2)

        # 输入默认的日期
        self.timeInputEntry_year.insert(0, str(self.time.timeList[0]))
        self.timeInputEntry_month.insert(0, str(self.time.timeList[1]))
        self.timeInputEntry_day.insert(0, str(self.time.timeList[2]))
        self.timeInputEntry_hour.insert(0, str(self.time.timeList[3]))
        self.timeInputEntry_minute.insert(0, str(self.time.timeList[4]))
        self.timeInputEntry_second.insert(0, str(self.time.timeList[5]))

        # 放在frame上
        self.timeInputEntry_year.grid(row=2, column=0, rowspan=2)
        self.timeInputEntry_month.grid(row=2, column=3, rowspan=2)
        self.timeInputEntry_day.grid(row=2, column=6, rowspan=2)
        self.timeInputEntry_hour.grid(row=2, column=9, rowspan=2)
        self.timeInputEntry_minute.grid(row=2, column=12, rowspan=2)
        self.timeInputEntry_second.grid(row=2, column=15, rowspan=2)

        self.timeInputEntry_year_adjustButton = adjustTimeButtonGroup(self,
                                                                      self.timeInputEntry_year, 0, 10000)
        self.timeInputEntry_month_adjustButton = adjustTimeButtonGroup(self,
                                                                       self.timeInputEntry_month, 1, 12)
        self.timeInputEntry_day_adjustButton = adjustTimeButtonGroup(self,
                                                                     self.timeInputEntry_day, 1, 31)
        self.timeInputEntry_hour_adjustButton = adjustTimeButtonGroup(self,
                                                                      self.timeInputEntry_hour, 0, 23)
        self.timeInputEntry_minute_adjustButton = adjustTimeButtonGroup(self,
                                                                        self.timeInputEntry_minute, 0, 59)
        self.timeInputEntry_second_adjustButton = adjustTimeButtonGroup(self,
                                                                        self.timeInputEntry_second, 0, 59)
        self.timeInputEntry_year_adjustButton.grid(row=2, column=2)
        self.timeInputEntry_month_adjustButton.grid(row=2, column=5)
        self.timeInputEntry_day_adjustButton.grid(row=2, column=8)
        self.timeInputEntry_hour_adjustButton.grid(row=2, column=11)
        self.timeInputEntry_minute_adjustButton.grid(row=2, column=14)
        self.timeInputEntry_second_adjustButton.grid(row=2, column=17)

        self.timeInputLabel_year = tk.Label(self, text="年")
        self.timeInputLabel_month = tk.Label(self, text="月")
        self.timeInputLabel_day = tk.Label(self, text="日")
        self.timeInputLabel_hour = tk.Label(self, text="时")
        self.timeInputLabel_minute = tk.Label(self, text="分")
        self.timeInputLabel_second = tk.Label(self, text="秒")
        self.timeInputLabel_year.grid(row=2, column=1)
        self.timeInputLabel_month.grid(row=2, column=4)
        self.timeInputLabel_day.grid(row=2, column=7)
        self.timeInputLabel_hour.grid(row=2, column=10)
        self.timeInputLabel_minute.grid(row=2, column=13)
        self.timeInputLabel_second.grid(row=2, column=16)

    def setTime(self):
        year = int(self.timeInputEntry_year.get())
        month = int(self.timeInputEntry_month.get())
        day = int(self.timeInputEntry_day.get())
        hour = int(self.timeInputEntry_hour.get())
        minute = int(self.timeInputEntry_minute.get())
        second = int(self.timeInputEntry_second.get())
        self.time.setTime(year, month, day, hour, minute, second)


if __name__ == "__main__":
    win = tk.Tk()
    win.title("TimeBox")
    win.geometry("500x300")
    timeBox = TimeBox(win, Time(2021, 12, 31, 23, 59, 59))
    timeBox.pack()
    win.mainloop()