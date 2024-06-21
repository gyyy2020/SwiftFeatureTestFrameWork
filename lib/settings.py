from pathlib import Path


class Setting:
    PROJECT_ROOT = Path(__file__).parent.parent
    CASE_PATH = PROJECT_ROOT.joinpath('case')
    SOURCE_PATH = PROJECT_ROOT.joinpath('source')
    LIB_PATH = PROJECT_ROOT.joinpath('lib')

    LOG_PATH = PROJECT_ROOT.joinpath('log')
    REPORT_PATH = PROJECT_ROOT.joinpath('report')
    case_log_dir = LOG_PATH

    result_new = False

    product_name = ""
    branch = ""


if __name__ == '__main__':
    print(Setting.LOG_PATH)
