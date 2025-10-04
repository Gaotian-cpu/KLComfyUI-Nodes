import os
import logging
from logging import Logger
import coloredlogs
import colorama


class Log:
    # 设置颜色
    coloredlogs.DEFAULT_FIELD_STYLES = {
        'asctime': {'color': 'green'}, 'hostname': {'color': 'magenta'},
        'levelname': {'color': 'green', 'bold': True},
        'request_id': {'color': 'yellow'},
        'name': {'color': 'blue'}, 'programname': {'color': 'cyan'},
        'threadName': {'color': 'yellow'}
    }
    colorama.init()
    __instances = {}

    @classmethod
    def get_logger(cls, name=os.path.abspath(__name__)) -> Logger:
        if name not in cls.__instances:
            # 日志文件夹路径
            # base_dir = os.getcwd()
            # while base_dir != '/':
            #     if '.idea' in os.listdir(base_dir):
            #         break
            #     base_dir = cls.get_parent_directory(base_dir)
            # base_dir = os.path.dirname(os.path.dirname(__file__))
            # log_dir = 'logs'
            # if not log_dir.startswith('/'):         # 日志文件夹
            #     log_dir = os.path.join(base_dir, log_dir)
            # # 递归生成
            # if not os.path.isdir(log_dir):
            #     os.makedirs(log_dir, mode=0o755)

            # log_file = os.path.join(log_dir, "app.log")
            logger = logging.getLogger(name)        # 设置日志格式
            # fmt = '%(asctime)s [%(levelname)s] [%(name)s] %(filename)s[line:%(lineno)d] [%(threadName)s] %(message)s'
            fmt = '%(asctime)s [%(levelname)s] [%(name)s] %(message)s'
            formatter = logging.Formatter(fmt)

            ch = logging.StreamHandler()
            ch.setLevel(Log.__get_log_level())
            ch.setFormatter(formatter)
            logger.addHandler(ch)

            coloredlogs.install(fmt=fmt, level=Log.__get_log_level(), logger=logger)

            # fh = TimedRotatingFileHandler(log_file, when='M', interval=1, backupCount=7, encoding='utf-8')
            # fh.setLevel(Log.__get_log_level())
            # fh.setFormatter(formatter)
            # logger.setLevel(Log.__get_log_level())
            # logger.addHandler(fh)
            cls.__instances[name] = logger

        return cls.__instances[name]

    @staticmethod  # 设置日志等级
    def __get_log_level():
        return logging.INFO

    @staticmethod
    def get_parent_directory(path: str):
        """
        获取目录或文件的父目录
        :param path: 文件或目录的路径
        :return: 结果或None
        """
        if path is None or path == '':
            return None

        if path.startswith('/'):
            return os.path.split(path)[0]
        else:
            abs_path = os.path.join(os.getcwd(), path)
            return os.path.split(abs_path)[0]


# if __name__ == '__main__':
#     logger = Log.get_logger('test')
#     logger.info('this is info')
#     logger.error('this is error')
