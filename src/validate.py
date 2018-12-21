""" Tests all rules against against the metrics file and shows unmatched metrics and progress """

import yaml
from src.test import match_regex, match_glob, resolve_home


ITERATIONS = 0
MATCHED = 0


def match(rules, line):
    global MATCHED
    for rule in rules:
        if rule.get('match_type') == 'regex':
            result = match_regex(rule['match'], line) is not None
        else:
            result = match_glob(rule['match'], line) is not None
        if result:
            MATCHED += 1
            return True
    return False


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
    if not getattr(args, 'rules'):
        print('--rules file required')
        return False
    if not getattr(args, 'key'):
        print('--key required')
        return False
    return True


def main(args):
    if not validate_args(args):
        exit(1)
    global ITERATIONS
    with open(resolve_home(args.rules), 'r') as f:
        rules = yaml.load(f.read())[args.key]
    with open(resolve_home(args.infile), 'r') as f:
        filtered = filter_metrics(f.read())
    for line in filtered:
        ITERATIONS += 1
        if not match(rules, line) and (MATCHED + 40) > ITERATIONS:
                print('No match found for {}'.format(line))
    print('Matched {}/{}; Percent Complete {}%'.format(MATCHED, ITERATIONS, round((MATCHED/ITERATIONS)*100)))
