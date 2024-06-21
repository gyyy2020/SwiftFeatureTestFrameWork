from importlib import import_module

from lib.api import run_it, init_api, init_setting


class CaseRunner:
    """
    run testcase from file
    """

    def __init__(self, case_file):
        self.case_path = case_file

    @staticmethod
    def case_path_to_module(case_path) -> str:
        """
        Convert case path to module
        Args:
            case_path:

        Returns:

        """
        pass

    @property
    def case_path(self):
        return self._case_file

    @case_path.setter
    def case_path(self, value):
        self._case_file = self.case_path_to_module(value)

    @init_setting
    @init_api
    def run_one(self, case_name, **kwargs):
        """
        run one case
        Args:
            case_name:
            **kwargs:

        Returns:

        """
        test_suite = import_module(self.case_path)
        assert hasattr(test_suite, case_name)
        case = getattr(test_suite, case_name)
        run_it(case, **kwargs)


if __name__ == '__main__':
    cr = CaseRunner("testcase_template.py")
    cr.run_one("BasicTestcase")
    print(cr.case_path)
