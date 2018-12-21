import argparse
from src.test import main as test
from src.validate import main as validate
from src.convert import main as convert


def main(args):
    if args.tool == 'test':
        test(args)
        exit(0)
    if args.tool == 'validate':
        validate(args)
        exit(0)
    if args.tool == 'convert':
        convert(args)
        exit(0)
    print('No such tool \'{}\''.format(args.tool))
    exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='StatsD Exporter Tools')
    parser.add_argument('tool', help='Tool to use')
    parser.add_argument('-r', '--regex', help='Regex pattern')
    parser.add_argument('-g', '--glob', help='Glob pattern')
    parser.add_argument('--infile', help='File of Metrics')
    parser.add_argument('--outfile', help='File to Write')
    parser.add_argument('--rules', help='Rules yaml file')
    parser.add_argument('--key', help='Rules dict key')
    parser.add_argument('--prepend', help='Namespace prepend for convert tool')
    args = parser.parse_args()
    main(args)
