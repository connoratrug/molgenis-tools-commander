from pathlib import Path

import mdev.arguments as arg_parser
from mdev import io
from mdev.executor import execute


# =========
# Arguments
# =========

def arguments(subparsers):
    p_run = subparsers.add_parser('run',
                                  help='Run an mdev script')
    p_run.set_defaults(write_to_history=False)
    p_run.add_argument('script',
                       type=str,
                       help='The .mdev script to run')
    p_run.add_argument('--ignore-errors', '-i',
                       action='store_true',
                       help='Let the script continue when one or more commands throw an error')


# =======
# Methods
# =======

def run(args):
    script = Path().home().joinpath('.mdev', 'scripts', args.script)

    lines = list()
    try:
        with open(script) as file:
            lines = [line.rstrip('\n') for line in file]
    except OSError as e:
        io.error('Error reading script: %s' % str(e))

    exit_on_error = not args.ignore_errors
    for line in lines:
        sub_args = arg_parser.parse_arg_string(line.split(' '))
        if sub_args.command == 'run':
            io.error("Can't use the run command in a script: %s" % line)
            if exit_on_error:
                exit(1)
            else:
                continue

        execute(sub_args, exit_on_error, line)
