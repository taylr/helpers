#!/usr/bin/env python

import argparse
import os

_EXCLUDE_PATTERNS = [
    r'\.git',
    r'site-pack',
    r'\.pyc',
    r'_generated',
    r'\.png',
    r'\.jpg',
    r'fixture',
    r'migration',
    r'js-coverage',
    r'node_modules',
    r'bower_components',
    r'vendor\/',
    r'\/dist\/',
    r'\.min\.',
    r'plato-reports',
    r'\.coverage',
    r'workspace\.xml',
    r'coverage\.xml',
    r'junit\.xml',
    r'\.ipynb',
    r'\/bin\/',
    r'test.*\.xml',
    r'\/tmp\/',
    r'\.json',
    r'fish\/static',
    r'\.inenv',
    r'\.db',
    r'webpack-build',
    r'\/bin\/',
    r'gdelt\/app\/static',
    r'\/app\/static'
]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='src_finder')
    parser.add_argument("regex_positional",  help='egrep regex (overrides -r)',        default='',                      nargs='?')
    parser.add_argument('-p', '--pattern',   help='filename pattern to match',         default=[],                                  action='append')
    parser.add_argument('-r', '--regex',     help='egrep regex for in files')
    parser.add_argument('-x', '--exclude',   help='egrep exclude regex',               default=_EXCLUDE_PATTERNS,       nargs='?',  action='append')
    parser.add_argument('-d', '--dir',       help='directory to find in',              default=os.getcwd())
    parser.add_argument('-t', '--type',      help='type to find',                      default='f')
    parser.add_argument('-i',                help='egrep case insensitive',                                                         action='store_true')

    args = parser.parse_args()

    if not args.regex_positional and not args.regex and args.pattern=='*':
        parser.error("Must supply a regex or pattern")

    regex = args.regex_positional if args.regex_positional else args.regex
    cmd = '/usr/bin/find {dir} -type {type}'.format(dir=args.dir, type=args.type)
    for i, p in enumerate(args.pattern):
        if i > 0:
            cmd += ' -o '
        cmd += ' -iname "{}"'.format(p)

    if args.exclude:
        cmd += ' | /usr/bin/egrep -v "{}"'.format('|'.join(args.exclude))
    if regex:
        cmd += ' | /usr/bin/xargs /usr/bin/egrep'
        if args.i:
            cmd += " -i"
        cmd += ' "{}"'.format(regex)

    print "cmd: {cmd_str}".format(cmd_str=cmd)
    os.system(cmd)
