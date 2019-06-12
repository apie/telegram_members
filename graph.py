#!/usr/bin/env python3

import os
import sys
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from pydblite import Base
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

def write_graph(channel):
    db = Base(os.path.join(SCRIPT_DIR, '%s_members.db' % channel))
    db.open()
    member_data = ((int(l['members'].split()[0]), l['time'].date()) for l in db)
    # Split the list of combinations in two lists, one for the y values and one for the x values
    y, x = list(zip(*member_data))
    fig = plt.figure()
    fig.autofmt_xdate()
    ax = fig.add_subplot(111)
    p = ax.bar(list(x)[-10:], list(y)[-10:])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    ax.set_xlabel('Date')
    ax.set_ylabel('Members')
    ax.set_title('Number of members for {}'.format(channel))
    plt.xticks(rotation=45)
    fig.savefig('{}.png'.format(channel))

def main(channel):
    write_graph(channel)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception('Provide name of the channel')
    main(sys.argv[1])

