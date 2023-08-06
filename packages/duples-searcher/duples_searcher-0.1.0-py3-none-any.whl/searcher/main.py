# from optparse import OptionParser, OptionGroup
import argparse
from searcher.models import SPTVision, Omron
from searcher.version import __version__
import json


def main():
    parser = argparse.ArgumentParser(
        description='Search information about duplicates in files')
    parser.add_argument('-f', '--file', required=True,
                        help="File to read source from technical vision log")
    parser.add_argument('-t', '--type', required=True,
                        help="Type of source file: [Omron, SPTVision]")
    parser.add_argument('-o', '--out', action="store_true",
                        help="Print duplicates to console")
    parser.add_argument('-v', '--version', action="version",
                        version="%(prog)s " + __version__)
    parser.add_argument('--to-file', help="file to write")
    args = parser.parse_args()
    if args.type == "SPTVision":
        model = SPTVision()
    elif args.type == "Omron":
        model = Omron()
    else:
        raise ValueError("Unknown type of file")
    if args.file:
        model.get_data_from_file(args.file)
    model.search_duplicates()
    if args.out:
        print(json.dumps(model.duplicates, indent=4, sort_keys=True))
    if args.to_file:
        model.write_duplicates_to_file(args.to_file)


if __name__ == '__main__':
    main()
