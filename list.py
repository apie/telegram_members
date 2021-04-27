#!/usr/bin/env python3
# List db contents. Provide channel name as argument.

import os
import sys
from pydblite import Base
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

def dolist(channel):
    db = Base(os.path.join(SCRIPT_DIR, f'{channel}_members.db'))
    db.open()
    for l in sorted(db, key=lambda x: x['time']):
        print(f"{l['members']} {str(l['time']).split('.')[0]}")

def main(channel):
    dolist(channel)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception('Provide name of the channel')
    main(sys.argv[1])

