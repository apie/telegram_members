#!/usr/bin/env python3

import os
import sys
from pydblite import Base
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

def dolist(channel):
    db = Base(os.path.join(SCRIPT_DIR, '%s_members.db' % channel))
    db.open()
    for l in db:
        print('%s %s' % (l['members'], l['time']))

def main(channel):
    dolist(channel)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception('Provide name of the channel')
    main(sys.argv[1])

