from contextlib import contextmanager
from functools import wraps

from lib.basic_test_tools import BasicTestTools
from lib.log_tools import log, add_handler_to_case, rename_log_dir
from lib.settings import Setting

api = None


class Api(Setting):
    def __init__(self, sn=""):
        log.logger.info(f"The plane has taken off: {sn}")
        self.sn = sn
        self.tools = BasicTestTools(sn=sn)


def init_api(func):
    """
    init api for case test
    Args:
        func:

    Returns:

    """

    @wraps(func)
    def new_api(*args, **kwargs):
        sn = kwargs.get("sn", "")
        global api
        api = Api(sn)
        log.logger.info(f"init api: {sn}")
        r = func(*args, **kwargs)
        return r

    return new_api


def update_setting(**kwargs):
    log.logger.info(f"update setting to {kwargs}")
    for k, v in kwargs.items():
        setattr(Setting, k, v)


def init_setting(func):
    """
    init test setting
    Args:
        func:

    Returns:

    """

    @wraps(func)
    def set_env(*args, **kwargs):
        setting_keys = Setting.__dict__.keys()
        env_kwargs = {k: v for k, v in kwargs.items() if k in setting_keys}
        case_kwargs = {k: v for k, v in kwargs.items() if k not in setting_keys}
        if len(env_kwargs) > 0:
            update_setting(**env_kwargs)
        r = func(*args, **case_kwargs)
        return r

    return set_env


@contextmanager
def fixed_setting(**kwargs):
    """
    Fixed test setup for testing
    Args:
        **kwargs:

    Returns:

    """
    update_setting(**kwargs)
    try:
        yield
    finally:
        log.logger.info(f"{kwargs} end")


def run_it(case, times=1, **kwargs):
    for i in range(1, times + 1):
        log.logger.info(f"{case} run {i} times")
        instance = case(**kwargs)
        add_handler_to_case(instance)
        rename_log_dir(instance)
        log.logger.info(f"{case} {i} run end")


@init_api
@init_setting
def run_with_api(case):
    run_it(case)
