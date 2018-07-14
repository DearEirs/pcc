# 既要把日志输出到控制台， 还要写入日志文件
import logging

class Log:
    def __init__(self):
        # 创建一个logger
        self.logger = logging.getLogger()
        # 创建一个handler，用于写入日志文件
        self.fh = logging.FileHandler('logger.txt', mode='w')
        # 创建一个handler，用于输出到控制台
        self.ch = logging.StreamHandler()
        # 定义handler的输出格式
        self.formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")

        self.logger.setLevel(logging.INFO)  # Log等级总开关
        self.fh.setLevel(logging.ERROR)  # 输出到file的log等级的开关
        self.ch.setLevel(logging.ERROR)  # 输出到console的log等级的开关
        self.fh.setFormatter(self.formatter)
        self.ch.setFormatter(self.formatter)

        # 将logger添加到handler里面
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.ch)

    # 记录日志
    def recordLog(self, content):
        # self.logger.debug('this is a logger debug message')
        # self.logger.info('this is a logger info message')
        # self.logger.warning('this is a logger warning message')
        self.logger.error(content)
        #self.logger.critical('this is a logger critical message')