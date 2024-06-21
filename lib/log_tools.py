import logging
from logging import handlers
from pathlib import Path

import colorlog

from lib.settings import Setting


class ColorLogTool:
    """
    Logging utility, supports outputting color logs to the console.
    """
    __instances = {}

    def __init__(self, log_file=None, level=logging.INFO):
        Setting.LOG_PATH.mkdir(parents=True, exist_ok=True)
        log_file = log_file or 'test.log'

        self.logger = logging.getLogger(str(log_file))
        # base level
        self.logger.setLevel(logging.DEBUG)
        log_colors = {
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        }

        fmt = "%(asctime)s [%(levelname)s] %(funcName)s %(filename)s:%(lineno)s %(message)s"
        console_fmt = f'%(log_color)s{fmt}'

        # 到这步会创建日志文件
        file_handler = logging.handlers.RotatingFileHandler(
            filename=Setting.LOG_PATH.joinpath(log_file),
            mode='a',
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding='utf-8'
        )
        console_handler = logging.StreamHandler()

        self.file_formatter = logging.Formatter(fmt)
        console_formatter = colorlog.ColoredFormatter(
            fmt=console_fmt, log_colors=log_colors)

        file_handler.setFormatter(self.file_formatter)
        console_handler.setFormatter(console_formatter)

        console_handler.setLevel(level)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def __new__(cls, *args, **kwargs):
        log_file_value = str(args[0] if args != () else kwargs.get("log_file", "test.log"))
        instance = cls.__instances.get(log_file_value, None)
        if instance is None:
            instance = super().__new__(cls)
            cls.__instances[log_file_value] = instance
        # print(instance, cls.__instances)
        return instance


def add_handler_to_case(instance):
    """
    Adding separate logs for each case
    Args:
        instance:

    Returns:

    """
    instance.log_dir.mkdir(parents=True, exist_ok=True)
    log_file = instance.case_log
    case_handler = logging.handlers.RotatingFileHandler(
        filename=log_file,
        mode='a',
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    case_handler.setFormatter(log.file_formatter)
    log.logger.addHandler(case_handler)
    instance.run()
    log.logger.removeHandler(case_handler)


def rename_log_dir(instance):
    """
    rename log dir according test result
    Args:
        instance:

    Returns:

    """
    log_dir_appendix = instance.log_dir_appendix
    log_dir = instance.log_dir
    if log_dir_appendix != "":
        log_dir.rename(Path(f"{log_dir}{log_dir_appendix}"))


def save_test_result(result, sn):
    """
    save test result to result file
    """
    result_file = Setting.PROJECT_ROOT.joinpath(f"result_{sn}.txt")
    if Setting.result_new is False:
        result_file.unlink(missing_ok=True)
    with open(result_file, "a", encoding="utf-8", errors="replace") as f:
        f.write(f"{result}\n")

    Setting.result_new = True


log = ColorLogTool()

if __name__ == '__main__':
    log.logger.critical('critical')
    log.logger.error('error')
    log.logger.warning('warning')
    log.logger.info('info')
    log.logger.debug('debug')
