import os

import requests
import bs4
from bs4 import BeautifulSoup
from triple_agent.constants.paths import (
    ALL_EVENTS_FOLDER,
)

SCL1_REPLAYS_URL = r"https://www.spypartyfans.com/calvin_is_cool.php?season=1"
SCL2_REPLAYS_URL = r"https://www.spypartyfans.com/calvin_is_cool.php?season=2"
SCL3_REPLAYS_URL = r"https://www.spypartyfans.com/calvin_is_cool.php?season=3"
BASE_SPF = r"https://www.spypartyfans.com"


def fetch_old_replays(url: str):
    soup = BeautifulSoup(requests.get(url).text, "lxml")

    for item in soup.body.contents:
        # Assume that each string is a header, and replay files that follow are under that info
        if isinstance(item, bs4.element.NavigableString) or (isinstance(item, bs4.element.Tag) and item.name == 'p'):
            try:
                item = item.text
            except AttributeError:
                pass

            event_num, division, week, players = map(str.strip, item.split(','))
            event = 'SCL' + event_num

            if week == 'hazard_promo_finals':
                division = week
                week = None

            if event:
                lowest_path = os.path.join(ALL_EVENTS_FOLDER, event)
                os.makedirs(lowest_path, exist_ok=True)

            if division:
                lowest_path = os.path.join(lowest_path, division)
                os.makedirs(lowest_path, exist_ok=True)

            if week:
                lowest_path = os.path.join(lowest_path, week)
                os.makedirs(lowest_path, exist_ok=True)


            print(event, division, week)
        if isinstance(item, bs4.element.Tag):
            if item.name == 'a' and item.attrs['href']:
                print(item.text)

                r = requests.get(BASE_SPF + item.attrs['href'])
                with open(os.path.join(lowest_path, item.text), 'wb') as outfile:
                    outfile.write(r.content)



if __name__ == "__main__":
    fetch_old_replays(SCL2_REPLAYS_URL)
    fetch_old_replays(SCL3_REPLAYS_URL)
