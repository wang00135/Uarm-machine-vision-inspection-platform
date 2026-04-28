# encoding: utf-8
import logging
import time
import os
from tools.config import config


def get_logging_save_folder():
    """获取日志文件的保存目录"""
    if not os.path.exists(config.LOG_SAVE_FLODER):
        os.makedirs(config.LOG_SAVE_FLODER)
    return config.LOG_SAVE_FLODER


def get_loggine_level(key, default="info"):
    """
    从全局配置中获取日志等级
    :param key:
    :param default: 日志等级默认 info
    :return: 日志等级
    """
    level_cfg = config.LOG_LEVEL_STDOUT
    if level_cfg == "debug":
        level_ret = logging.DEBUG
    elif level_cfg == "info":
        level_ret = logging.INFO
    elif level_cfg == "warning":
        level_ret = logging.WARNING
    elif level_cfg == "error":
        level_ret = logging.ERROR
    else:
        level_ret = logging.INFO
    return level_ret


level_stdout = config.LOG_LEVEL_STDOUT
level_file = config.LOG_LEVEL_FILE

logging_folder_path = get_logging_save_folder()
logName = os.path.join(logging_folder_path, '%s.log' % time.strftime('%Y-%m-%d'))  # 文件的命名

log_colors_config = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red',
}


class Log:
    def __init__(self, logName=logName):
        from logging.handlers import RotatingFileHandler  # 按文件大小滚动备份
        import colorlog  # 控制台日志输入颜色
        self.logName = logName
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.formatter = colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s',
            log_colors=log_colors_config)  # 日志输出格式

        if config.LOG_FLAGE:
            # 创建一个FileHandler，用于写到本地
            fh = RotatingFileHandler(filename=self.logName, mode='a', maxBytes=1024 * 1024 * 5, backupCount=5,
                                     encoding='utf-8')  # 使用RotatingFileHandler类，滚动备份日志
            fh.setLevel(get_loggine_level(level_file))
            fh.setFormatter(self.formatter)
            self.logger.addHandler(fh)
        
        # 创建一个StreamHandler,用于输出到控制台
        ch = colorlog.StreamHandler()
        ch.setLevel(get_loggine_level(level_stdout))
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)
        self.handle_logs()
    
    def get_file_sorted(self, file_path):
        """最后修改时间顺序升序排列 os.path.getmtime()->获取文件最后修改时间"""
        dir_list = os.listdir(file_path)
        if not dir_list:
            return
        else:
            dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
            return dir_list
    
    def TimeStampToTime(self, timestamp):
        """格式化时间"""
        timeStruct = time.localtime(timestamp)
        return str(time.strftime('%Y-%m-%d', timeStruct))
    
    def handle_logs(self):
        import datetime
        """处理日志过期天数和文件数量"""
        dirPath = logging_folder_path  # 拼接删除目录完整路径
        file_list = self.get_file_sorted(dirPath)  # 返回按修改时间排序的文件list
        if file_list:  # 目录下没有日志文件
            for i in file_list:
                file_path = os.path.join(dirPath, i)  # 拼接文件的完整路径
                t_list = self.TimeStampToTime(os.path.getctime(file_path)).split('-')
                now_list = self.TimeStampToTime(time.time()).split('-')
                t = datetime.datetime(int(t_list[0]), int(t_list[1]),
                                      int(t_list[2]))  # 将时间转换成datetime.datetime 类型
                now = datetime.datetime(int(now_list[0]), int(now_list[1]), int(now_list[2]))
                if (now - t).days > 6:  # 创建时间大于6天的文件删除
                    self.delete_logs(file_path)
            if len(file_list) > 4:  # 限制目录下记录文件数量
                file_list = file_list[0:-4]
                for i in file_list:
                    file_path = os.path.join(dirPath, i)
                    print(file_path)
                    self.delete_logs(file_path)
    
    def delete_logs(self, file_path):
        try:
            os.remove(file_path)
        except PermissionError as e:
            log.warning('删除日志文件失败：{}'.format(e))

log = Log().logger

if __name__ == "__main__":
    log.info("——测试info——")
    log.warning("----测试警告----")
    log.error("----测试错误----")
