import argparse
from argparse import Namespace

from report_monaco.racing_cli import (build_report, driver, print_reports,
                                      read_files, sort_data, validate_path)


def run_parser(args: list = None) -> [Namespace]:
    parser = argparse.ArgumentParser(description="Race statistics")
    parser.add_argument('--files', dest="folder", help="File folder")
    parser.add_argument('--asc', dest="asc", action='store_const', const=False, help='From slow to faster')
    parser.add_argument('--desc', dest="asc", action='store_const', const=True, help='From faster to slow')
    parser.add_argument('--driver', dest="driver", help='driver name')
    return parser.parse_args(args, namespace=None)


def main() -> None:
    args = run_parser()
    if {None} in [{args.asc, args.driver}, {args.folder}]:
        raise ValueError('Please select --file dir --asc/--desc or --driver')
    folder_path = validate_path(args.folder)
    text = read_files(folder_path)
    rating_dict = build_report(text)
    if args.driver is not None:
        return print_reports(driver(rating_dict, args.driver))
    return print_reports(sort_data(rating_dict, args.asc))


if __name__ == '__main__':
    main()
