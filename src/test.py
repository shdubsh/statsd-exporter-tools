""" Tests a rule against the metrics file """
import re
import os


def match_glob(pattern, line):
    groups = []
    pattern_segments = pattern.split('.')
    line_segments = line.split('.')
    if len(pattern_segments) != len(line_segments):
        return None
    for index, pattern in enumerate(pattern_segments):
        if pattern == '*':
            groups.append(line_segments[index])
            continue
        else:
            if pattern != line_segments[index]:
                return None
    return groups


def match_regex(pattern, line):
    pattern = re.compile(pattern)
    matched = re.match(pattern, line)
    if matched:
        return list(matched.groups())
    return None


def filter_metrics(raw):
    output = []
    for line in raw.split('\n'):
        line = line.strip()
        if line[-6:] != '.count':
            continue
        output.append(line[0:-6])
    return output


def validate_args(args):
    if not getattr(args, 'infile'):
        print('--infile required')
        return False
    if not getattr(args, 'regex') and not getattr(args, 'glob'):
        print('--regex or --glob required')
        return False
    return True


def resolve_home(path):
    if path[0] == '~':
        return path.replace('~', os.getenv('HOME'))
    else:
        return path


def main(args):
    if not validate_args(args):
        exit(1)
    with open(resolve_home(args.infile), 'r') as f:
        filtered = filter_metrics(f.read())
    if args.regex:
        for line in filtered:
            groups = match_regex(args.regex, line)
            if groups is not None:
                print(line)
                print('Labels: {}'.format(groups))
    else:
        for line in filtered:
            groups = match_glob(args.glob, line)
            if groups is not None:
                print(line)
                print('Labels: {}'.format(groups))
