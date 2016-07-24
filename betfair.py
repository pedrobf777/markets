#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup


def get_betfair_chances(url):
    chances = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    runners = soup.findAll(attrs={'class': 'runner'})

    for runner in runners:
        name = runner.find(attrs={'class': 'selection-name'}).text.strip()
        prices = runner.findAll(attrs={'class': 'default-price'})

        if len(prices) != 2:
            continue

        back = float(prices[0].text.strip().splitlines()[0])

        try:
            lay = float(prices[1].text.strip().splitlines()[0])
        except IndexError:
            lay = back
        except ValueError:
            lay = back

        chance = ((1 / back + 1 / lay) / 2) * 100

        if chance > 2.0:
            chances.append((name, chance))

    return chances
