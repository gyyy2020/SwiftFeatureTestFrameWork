from contextlib import contextmanager
from functools import wraps

from lib.platform import Platform


class Common(Platform):
    def __init__(self):
        super().__init__()

    def get_printk(self):
        pass

    def set_printk(self, value):
        pass

    def change_printk(self, printk):
        def outer(func):
            wraps(func)

            def inner(*args, **kwargs):
                old_printk = self.get_printk()
                self.set_printk(printk)
                r = func(*args, **kwargs)
                self.set_printk(old_printk)
                return r

            return inner

        return outer

    @contextmanager
    def fixed_printk(self, printk):
        if printk < 0:
            yield
            return
        old_printk = self.get_printk()
        self.set_printk(printk)
        try:
            yield
        finally:
            self.set_printk(old_printk)
