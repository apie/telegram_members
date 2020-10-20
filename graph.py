#!/usr/bin/env python3
# Write a graph of the number of members for a channel. Print latest value to stdout.

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
    member_data = ((int(l['members'].split()[0]), l['time'].date()) for l in sorted(db, key=lambda x: x['time']))
    variant = db[0]['members'].split()[1]
    # Split the list of combinations in two lists, one for the y values and one for the x values
    y, x = list(zip(*member_data))
    fig = plt.figure()
    fig.autofmt_xdate()
    ax = fig.add_subplot(111)
    p = ax.plot(x, y, 'b')
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    date_range = (max(x) - min(x)).days
    # Change X axis locators for large date ranges
    if date_range > 365:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.set_xlabel('Date')
    ax.set_ylabel(f'{variant.capitalize()}')
    fig.suptitle(f'Number of {variant} for {channel} over time', fontsize=15)
    ax.set_title(f'Maximum: {max(y)}. Currently: {y[-1]}')
    ax.set_ylim(bottom=0)
    print(y[-1])  # Print latest value to stdout
    plt.xticks(rotation=45)
    fig.savefig(os.path.join(SCRIPT_DIR, f'{channel}.png'))

def main(channel):
    write_graph(channel)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception('Provide name of the channel')
    main(sys.argv[1])

