import time
import traceback
from abc import ABCMeta

from lib.log_tools import log, save_test_result, add_handler_to_case, rename_log_dir
from lib.settings import Setting


class BasicTestcase(metaclass=ABCMeta):
    """
    the very basic testcase template
    """

    def __init__(self, sn=""):
        self.__sign = "*" * 20
        self.case_name = self.__class__.__name__
        self.log_dir = Setting.LOG_PATH.joinpath(f"{self.case_name}{time.strftime('%Y%m%d%H%M%S')}")
        # may rename log dir according to result of test
        self.log_dir_appendix = ""
        self.case_log = self.log_dir.joinpath("case.log")

        from lib.api import api
        if api is None:
            self.sn = sn
        else:
            self.sn = api.sn
            api.case_log_dir = self.log_dir

    def set_up(self):
        log.logger.info(f"{self.__sign}{self.case_name} start{self.__sign}")

    def test_step(self):
        pass

    def tear_down(self):
        log.logger.info(f"{self.__sign}{self.case_name} end{self.__sign}")

    def run(self):
        self.log_dir.mkdir(parents=True, exist_ok=True)
        log.logger.info(f"{self.case_name} start run before setup")
        test_result = f"{self.case_name} none"
        try:
            self.set_up()
            self.test_step()
            test_result = f"{self.case_name} pass"
        except Exception:
            log.logger.error(traceback.format_exc())
            test_result = f"{self.case_name} fail"
        finally:
            self.tear_down()
            save_test_result(test_result, self.sn)
        log.logger.info(f"{self.case_name} finish run after teardown")

    def run_with_case_log(self):
        add_handler_to_case(self)
        rename_log_dir(self)


if __name__ == '__main__':
    btc = BasicTestcase()
    # btc.run()
    btc.run_with_case_log()
