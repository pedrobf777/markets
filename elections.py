#!/usr/bin/env python

import csv
from datetime import datetime
from jinja2 import Template

from betfair import get_betfair_chances


markets = {
    'usa': {
        'url': 'https://www.betfair.com.au/sports/politics/2016-us-presidential-election/8887484/next-president/nonsport/1.107373419',  # noqa
        'name': 'Next US President'
    },
    'tour': {
        'url': 'https://www.betfair.com.au/sports/cycling/tour-de-france-2016/7979859/winner/outright_winner/1.119710618',
        'name': 'Tour de France'
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
            market_url=market['url'],
            updated=datetime.now().strftime('%Y-%m-%d %H:%M'))

        with open('out/{}.html'.format(key), 'w') as f:
            f.write(rendered)

        with open('out/history.csv', 'a') as f:
            now = datetime.now()
            writer = csv.writer(f)
            for runner in runners:
                writer.writerow([now, key, runner[0], runner[1]])

if __name__ == '__main__':
    election()
