#!/usr/bin/python
# -*- coding:utf-8-*-

#import os
import re
import codecs

count = 0
needle = u"®"
with codecs.open('/var/tmp/stage2.dmp', encoding='utf-8') as f:
    for line in f:
        count += 1
        #®
        if needle in line:
        # if re.match(r'\xae', unicode(line), re.UNICODE):
            print "Match at line %d: %s" % (count, repr(line))