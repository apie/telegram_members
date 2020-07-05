#!/usr/bin/env python3

import os
import sys
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

from pydblite import Base
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

def write_graph(channel):
    db = Base(os.path.join(SCRIPT_DIR, f'{channel}_members.db'))
    db.open()
    member_data = ((int(l['members'].split()[0]), l['time'].date()) for l in db)
    # Split the list of combinations in two lists, one for the y values and one for the x values
    y, x = list(zip(*member_data))
    fig = plt.figure()
    fig.autofmt_xdate()
    ax = fig.add_subplot(111)
    p = ax.plot(x, y, 'b')
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    ax.set_xlabel('Date')
    ax.set_ylabel('Members')
    fig.suptitle(f'Number of members for {channel} over time', fontsize=15)
    ax.set_title(f'Maximum: {max(y)}. Currently: {y[-1]}')
    print(y[-1])
    plt.xticks(rotation=45)
    fig.savefig(os.path.join(SCRIPT_DIR, f'{channel}.png'))

def main(channel):
    write_graph(channel)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception('Provide name of the channel')
    main(sys.argv[1])

