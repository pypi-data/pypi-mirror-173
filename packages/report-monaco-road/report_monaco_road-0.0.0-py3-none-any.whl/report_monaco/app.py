import argparse
from argparse import Namespace
from typing import Optional

from report_monaco.racing_cli import (build_report, print_reports, read_files,
                                      sort_data, validate_path)


def run_parser(args: list = None) -> Optional[Namespace]:
    parser = argparse.ArgumentParser(description="Race statistics")
    parser.add_argument('--files', dest="folder", help="File folder")
    parser.add_argument('--asc', action='store_const', const='asc', help='From slow to faster', default=None)
    parser.add_argument('--desc', action='store_const', const='desc', help='From faster to slow', default=None)
    parser.add_argument('--driver', dest="driver", help='driver name')
    return parser.parse_args(args, namespace=None)


def command_line() -> None:
    args = run_parser()
    if {args.asc, args.desc, args.driver} == {None}:
        raise ValueError('Please select --file dir --asc/--desc or --driver')
    folder_path = validate_path(args.folder)
    text = read_files(folder_path)
    rating_dict = build_report(text)
    if {args.asc, args.desc} != {None}:
        return print_reports(sort_data(rating_dict, args.asc, None))
    return print_reports(sort_data(rating_dict, args.asc, args.driver))


if __name__ == '__main__':
    command_line()
