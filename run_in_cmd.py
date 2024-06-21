import argparse

from run import CaseRunner

parser = argparse.ArgumentParser("run test case in cmd")
parser.add_argument("-pn", dest="product_name", type=str, help="product name")
parser.add_argument("-b", dest="branch", type=str, help="branch")
parser.add_argument("-s", dest="sn", type=str, help="sn", default="")
parser.add_argument("-f", dest="case_file", type=str, help="case file")
parser.add_argument("-n", dest="case_name", type=str, help="case name")
parser.add_argument("-t", dest="times", type=int, default=1, help="run times")

args = parser.parse_args()

CaseRunner(args.case_file).run_one(args.case_name, times=args.times, product_name=args.product_name,
                                   branch=args.branch,
                                   sn=args.sn)
