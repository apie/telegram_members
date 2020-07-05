#!/usr/bin/env python3
# Fetch number of subscribers for a channel. Save in db an compare to previous number. If it has changed: return exit code 1.

import requests
import datetime
import os
import sys
from lxml import html
from pydblite import Base

STATUS_PAGE_BASE = 'https://t.me/'
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def save_in_db(channel, count):
    db = Base(os.path.join(SCRIPT_DIR, f'{channel}_members.db'))
    db.create('members', 'time', mode="open")
    len_db = len(db)
    count_previous = db[len_db-1]['members'] if len_db else 0
    if count != count_previous:
        db.insert(members=count, time=datetime.datetime.now())
        db.commit()
        return True

def fetch_number_of_subscribers(channel):
  page = requests.get(STATUS_PAGE_BASE+channel, timeout=8).text
  doc = html.fromstring(page)
  try:
      div = doc.xpath("//div[@class='tgme_page_extra']")[0]
  except IndexError:
      raise Exception('Not a channel')
  return div.text_content()

def main(channel):
  nr = fetch_number_of_subscribers(channel)
  if 'members' not in nr:
      raise Exception('Not a channel')
  if save_in_db(channel, nr):
      return True

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception('Provide name of the channel')
    if not main(sys.argv[1]):
        sys.exit(1)

