import sys
import logging
from io import StringIO
from urllib.parse import quote

import requests

logging.basicConfig(stream=sys.stderr)
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
start = 'http://169.254.169.254/latest/meta-data/'

def crawl(url):
    response = requests.get(url)
    buf = StringIO(response.text)
    for tmp in buf:
        wrk = tmp.strip()
        if wrk.endswith('/'):
            next_url = f'{url}{wrk}'
            logger.debug(f'{next_url=}')
            crawl(next_url)
        else:
            current_url = f'{url}{wrk}'
            logger.debug(f'leaf={wrk}')
            get_leaf(current_url)


def get_leaf(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print('################################################################################')
            print(f'# {url}')
            print('################################################################################')
            buf = StringIO(response.text)
            for tmp in buf:
                wrk = tmp.strip()
                print(wrk)
            print()
        else:
            logger.warning(f'{url} returned {response.status_code}')
    except Exception as wtf:
        logger.error(wtf)

crawl(start)
