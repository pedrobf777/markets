#!/usr/bin/env python

import csv
from datetime import datetime
from jinja2 import Template

from betfair import get_betfair_chances


markets = {
    'au': {
        'url': 'https://www.betfair.com.au/sports/politics/australian-politics/2215338/federal-election-winner/nonsport/2.100757409',  # noqa
        'name': 'Australian Federal Election',
    },
    'usa': {
        'url': 'https://www.betfair.com.au/sports/politics/2016-us-presidential-election/8887484/next-president/nonsport/1.107373419',  # noqa
        'name': 'Next US President'
    }
}


def election():
    template = Template(open('template.html').read())
    for key, market in markets.items():
        runners = get_betfair_chances(market['url'])
        rendered = template.render(
            market=market['name'],
            runners=runners,
            markets=markets,
            market_url=market['url'])

        with open('out/{}.html'.format(key), 'w') as f:
            f.write(rendered)

        with open('out/history.csv', 'a') as f:
            now = datetime.now()
            writer = csv.writer(f)
            for runner in runners:
                writer.writerow([now, key, runner[0], runner[1]])

if __name__ == '__main__':
    election()
