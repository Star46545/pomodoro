import shutil
import os
import json

startupPath = 'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp'


def getPath():
    return os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":
    if not os.path.exists(f'{startupPath}\\main_ui.pyw'):
        try:
            shutil.copy(f'{getPath()}\\main_ui.pyw',
                        f'{startupPath}\\main_ui.pyw')
        except IOError as err:
            print(f'发生了错误:IOError:{err}')
        except:
            print('发生了未知错误，你也许可以尝试使用管理员权限运行我(这不一定能解决问题！)')

    if not os.path.exists(f'{getPath()}\\config.json'):
        try:
            with open(f'{getPath()}\\config.json', 'w') as f:
                f.write(json.dumps({"time list": [0, 0, 0, 0, 25, 0],
                                    "black_theme": False,
                                    "time mode": 1
                                    }))
        except Exception as err:
            print('初始化配置文件发生错误！')

    if not os.path.exists(f'{getPath()}\\task.json'):
        try:
            with open(f'{getPath()}\\task.json', 'w') as f:
                f.write(json.dumps({"end time": 0,
                                    "black theme": False}))
        except Exception as err:
            print('初始化任务文件发生错误！')

    print('初始化结束')
    _ = input("按回车键退出")
