#!/usr/bin/env python

import argparse
import os

_DEFAULT_EXCLUDE_PATTERNS = [
    # OS
    r'.DS_Store',
    # configuration
    r'\.idea',
    r'\.git',
    # image formats
    r'\.png',
    r'\.je?pg',
    r'\.gif',
    # node / js vendor files
    r'node_modules',
    r'bower_components',
    # processed and minified files
    r'\.cache\/'
    r'\/dist\/',
    r'\.min\.',
    r'\.pyc',
    r'webpack-build',
    # test
    r'test.*\.xml',
]

_DEFAULT_PATTERN_FILE_NAME = '.find-helper'


def _load_exclude_patterns(fname=None):
    """load .find-helper or use the default excludes"""
    print('exclude path exists?  {} {}'.format(fname, os.path.exists(fname)))
    if fname is None or not os.path.exists(fname):
        for path_prefix in ('./', '~/'):
            path_to_try = os.path.abspath(os.path.expanduser(path_prefix + _DEFAULT_PATTERN_FILE_NAME))
            if os.path.exists(path_to_try):
                fname = path_to_try
                print('found config {}'.format(fname))
                break

    # load defauls if not found
    if not os.path.exists(fname):
        print('exclude path not found "{}"'.format(fname))
        return _DEFAULT_EXCLUDE_PATTERNS


    return [x.strip() for x in open(os.path.expanduser(fname), 'r') if x.strip()]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='find.py',
        description='egrep in files excluding paths specified by (properly escaped) regex in ~/.find-helper or ./.find-helper')
    parser.add_argument("regex_positional",  help='egrep regex (overrides -r)',        default='',                      nargs='?')
    parser.add_argument('-p', '--pattern',   help='filename pattern to match',         default=[],                                  action='append')
    parser.add_argument('-X', '--exclude-file',  help='exclude-file',                      default=_DEFAULT_PATTERN_FILE_NAME)
    parser.add_argument('-r', '--regex',     help='egrep regex for in files')
    parser.add_argument('-x', '--exclude',   help='egrep exclude regex',               default=[],                      nargs='?',  action='append')
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

    exclude_patterns = _load_exclude_patterns(args.exclude_file)
    if args.exclude:
        exclude_patterns.extend(args.exclude)

    # unique and sort the exclude patters
    if exclude_patterns:
        cmd += ' | /usr/bin/egrep -v "{}"'.format('|'.join(sorted(set(exclude_patterns))))

    if regex:
        cmd += ' | /usr/bin/xargs /usr/bin/egrep'
        if args.i:
            cmd += " -i"
        cmd += ' "{}"'.format(regex)

    print("cmd: {cmd_str}".format(cmd_str=cmd))
    os.system(cmd)
