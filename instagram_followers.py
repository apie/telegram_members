#!/usr/bin/env python3
# Fetch number of followers for an account. Save in db and compare to previous number. If it has changed: return exit code 1.

import requests
import datetime
import os
import sys
from lxml import html
from pydblite import Base

from telegram_members import save_in_db

STATUS_PAGE_BASE = 'https://bibliogram.snopyta.org/u/'

def fetch_number_of_followers(account: str) -> str:
  page = requests.get(STATUS_PAGE_BASE+account, timeout=8).text
  doc = html.fromstring(page)
  try:
      followed_by = doc.xpath('//div[@class="profile-counter"][text()="Followed by"]/span/text()')[0]
  except IndexError:
      raise Exception('Not an account')
  return followed_by.strip()+' followers'

def main(account):
  nr = fetch_number_of_followers(account)
  return save_in_db(account, nr)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception('Provide name of the account')
    if not main(sys.argv[1]):
        sys.exit(1)

