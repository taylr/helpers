#!/usr/bin/env python

import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='src_finder')
    parser.add_argument("regex_positional",  help='egrep regex (overrides -r)',        default='',                      nargs='?')
    parser.add_argument('-p', '--pattern',   help='filename pattern to match',         default='*')
    parser.add_argument('-r', '--regex',     help='egrep regex for in files')
    parser.add_argument('-x', '--exclude',   help='egrep exclude regex',               default='\.git|site-pack|\.pyc')
    parser.add_argument('-d', '--dir',       help='directory to find in',              default=os.getcwd())
    parser.add_argument('-t', '--type',      help='type to find',                      default='f')

    args = parser.parse_args()

    if not args.regex_positional and not args.regex and args.pattern=='*':
        parser.error("Must supply a regex or pattern")

    regex = args.regex_positional if args.regex_positional else args.regex
    print "positional: %s, option: %s --> %s" % (args.regex_positional, args.regex, regex)
    cmd = '/usr/bin/find %s -type %s -iname "%s" | /usr/bin/egrep -v "%s"' % (args.dir, args.type, args.pattern, args.exclude)
    if regex:
        cmd += ' | /usr/bin/xargs /usr/bin/egrep "%s"' % (regex)

    print "cmd: %s" % (cmd)
    #os.system(cmd)
