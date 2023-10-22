#!/usr/bin/env python3
# Add measurement for a channel.

import datetime
import os
import sys
from pydblite import Base

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def save_in_db(channel, count, date):
    db = Base(os.path.join(SCRIPT_DIR, f'{channel}_members.db'))
    db.create('members', 'time', mode="open")
    try:
        variant = db[0]['members'].split()[1]
    except KeyError:
        variant = 'subscribers'
    value = f"{count} {variant}"
    already_present = [r for r in db if r['members'] == value]
    if not already_present:
        db.insert(members=value, time=date)
        db.commit()
        return True


if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise Exception('Provide name of the channel, a start date and a member count')
    channel = sys.argv[1]
    date = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d')
    count = sys.argv[3]
    save_in_db(channel, count, date)

