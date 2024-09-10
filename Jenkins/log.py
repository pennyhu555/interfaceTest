import datetime, threading, shutil, os
def clear_log():
    shutil.rmtree("logs", True)
    os.mkdir("logs")

class MyLog:
    def info(self,msg):
        timestamp = datetime.datetime.utcnow()
        try:
            scenario_name = threading.current_thread().scenario_name
        except:
            scenario_name = "UnNamed Scenario"
        print(f"[{scenario_name}][{timestamp}]{msg}")
        with open(f"logs//logs_{scenario_name}.txt","a") as f:
            f.write(f"[{timestamp}]{msg}\n")


if __name__ == "__main__":
    clear_log()
    logger = MyLog()
    logger.info("随便打个日志")