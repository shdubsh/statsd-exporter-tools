""" Converts the output of `ls -R` on the graphite whisper directory to a file of usable metrics """

from src.test import resolve_home

def gen_block(raw, prepend):
    in_block = False
    block_data = []
    contains_files = False
    block_line = 0
    namespace = ''
    for line in raw.split('\n'):
        if line == '':
            in_block = False
            if contains_files:
                yield block_data
            contains_files = False
            block_line = 0
            block_data = []
            continue

        if line[-1] == ':':
            in_block = True
        if in_block:
            if block_line == 0:
                namespace = extract_namespace(prepend, line)
            else:
                if '.wsp' in line:
                    contains_files = True
                    block_data.append('.'.join([namespace, line.split('.')[0]]))
            block_line += 1


def extract_namespace(prepend, line):
    return '{}.'.format(prepend) + '.'.join(line[2:-1].split('/'))


def validate_args(args):
    if not getattr(args, 'infile'):
        print('--infile required')
        return False
    if not getattr(args, 'outfile'):
        print('--outfile required')
        return False
    if not getattr(args, 'prepend'):
        print('--prepend required')
        return False
    return True


def main(args):
    if not validate_args(args):
        exit(1)
    with open(resolve_home(args.outfile), 'w') as write:
        with open(resolve_home(args.infile), 'r') as read:
            for block in gen_block(read.read(), args.prepend):
                for metric in block:
                    write.write(metric + '\n')
