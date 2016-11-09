#!/usr/bin/env python

import csv
from datetime import datetime
from jinja2 import Template

from betfair import get_betfair_chances


BETTING_MARKETS = {
    'afl17': {
        'url': 'https://www.betfair.com.au/sports/australian-rules/afl-2017/10164109/premiers-2017/undifferentiated/1.127270933',
        'name': 'AFL Premiers 2017'
    }
}


def markets():
    template = Template(open('template.html').read())
    for key, market in BETTING_MARKETS.items():
        runners = get_betfair_chances(market['url'])
        rendered = template.render(
            market=market['name'],
            runners=runners,
            markets=BETTING_MARKETS,
            market_url=market['url'],
            updated=datetime.now().strftime('%Y-%m-%d %H:%M%z'))

        with open('out/{}.html'.format(key), 'w') as f:
            f.write(rendered)

        with open('out/history.csv', 'a') as f:
            now = datetime.now()
            writer = csv.writer(f)
            for runner in runners:
                writer.writerow([now, key, runner[0], runner[1]])

if __name__ == '__main__':
    markets()
