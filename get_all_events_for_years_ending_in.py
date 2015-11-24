#!/usr/bin/env python2.6
# encoding: utf-8

import histopy
import datetime
import random
import json
import calendar
import re
import collections
import os
import sys
import argparse

def _to_int(input):
    bc = re.compile(' BC\Z')
    bce = re.compile(' BCE\Z')
    slash = re.compile('/')
    if (bc.search(input)):
        return int(input[0:-3])
    if (bce.search(input)):
        return int(input[0:-4])
    if (slash.search(input)):
        return int(input.split('/')[0])
    return int(input)

def _filter(input, year_endings):
    return {k:v for (k,v) in input.iteritems() if _to_int(k) % 10 in year_endings}

def _map(input, month, day):
    return {'{num:02d}'.format(num=day) + ' ' + calendar.month_name[month] + ' ' + key: value for key, value in input.items()}

parser = argparse.ArgumentParser(description='Fetch events from Wikipedia for years ending in given endings for the given month.')
parser.add_argument('--month', dest='month', type=int, default=1)
parser.add_argument('--year_endings', nargs='+', dest='year_endings', type=int, default=[5, 0])

args = vars(parser.parse_args())
month = args['month']
year_endings = args['year_endings']
print 'Events should be for years ending in {}'.format(year_endings)

year = 2015
all_events = {}
all_deaths = {} 
all_births = {}

# fix 30/31 not taken in consideration
days_in_month = calendar.monthrange(year, month)[1] + 1

for day in range(1, days_in_month):
    today = datetime.datetime(year, month, day)
    today_in_history = histopy.load_history(today)
    
    events = histopy.load_events(today_in_history)
    all_events.update(_map(_filter(events, year_endings), month, day))
    
    deaths = histopy.load_deaths(today_in_history)
    all_deaths.update(_map(_filter(deaths, year_endings), month, day))
    
    births = histopy.load_births(today_in_history)
    all_births.update(_map(_filter(births, year_endings), month, day))

if not os.path.exists('./output'):
    os.makedirs('./output')

f = open('output/' + calendar.month_name[month] + '_events.json', 'w')
json.dump(collections.OrderedDict(sorted(all_events.items())), f)
print 'Found {} events for month of {}'.format(len(all_events), calendar.month_name[month])

f = open('output/' + calendar.month_name[month] + '_deaths.json', 'w')
json.dump(collections.OrderedDict(sorted(all_deaths.items())), f)
print 'Found {} deaths for month of {}'.format(len(all_deaths), calendar.month_name[month])

f = open('output/' + calendar.month_name[month] + '_births.json', 'w')
json.dump(collections.OrderedDict(sorted(all_births.items())), f)
print 'Found {} births for month of {}'.format(len(all_births), calendar.month_name[month])

