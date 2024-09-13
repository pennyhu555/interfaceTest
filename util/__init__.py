import datetime, threading, shutil, os
from datetime import datetime, timezone, timedelta


def clear_log():
    shutil.rmtree("logs", True)
    os.mkdir("logs")


class MyLog:
    def __init__(self, log_level="INFO"):
        self.INFO = 1
        self.DEBUG = 2
        log_dict = {"INFO":self.INFO, "DEBUG":self.DEBUG}
        self.log_level = log_dict[log_level]

    def info(self, msg):
        msg = msg.replace(u'\xa0', u' ')  # 解决编码问题，gbk里没有\xa0，用空格替代
        timezone_offset = 8.0   # 将日志的时区设置为东八区
        tzinfo = timezone(timedelta(hours=timezone_offset))
        timestamp = datetime.now(tzinfo)
        try:
            scenario_name = threading.current_thread().scenario_name
        except:
            scenario_name = ""
        if self.log_level >= self.INFO:
            print(f"[{scenario_name}][{timestamp}]{msg}")
        with open(f"logs//logs_{scenario_name}.txt","a") as f:
            f.write(f"[{timestamp}]{msg}\n")

    def debug(self, msg):
        msg = msg.replace(u'\xa0', u' ')   # 解决编码问题，gbk里没有\xa0，用空格替代
        timezone_offset = 8.0   # 将日志的时区设置为东八区
        tzinfo = timezone(timedelta(hours=timezone_offset))
        timestamp = datetime.now(tzinfo)
        try:
            scenario_name = threading.current_thread().scenario_name
        except:
            scenario_name = ""
        if self.log_level >= self.DEBUG:
            print(f"[{scenario_name}][{timestamp}]{msg}")
        with open(f"logs//logs_{scenario_name}.txt", "a") as f:
            f.write(f"[{timestamp}]{msg}\n")


clear_log()
logger = MyLog()
