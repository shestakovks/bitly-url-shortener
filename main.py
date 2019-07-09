from dotenv import load_dotenv
from urllib.parse import urlparse
import argparse
import os
import requests

load_dotenv()


def is_bitlink(token, link):
    parsed_link = urlparse(link)
    link = parsed_link.netloc + parsed_link.path
    headers = {
        'Authorization': f'Bearer {token}',
    }
    r = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{link}',
        headers=headers
    )
    return r.ok


def shorten_link(token, link):
    headers = {
        'Authorization': f'Bearer {token}',
    }
    data = {
        'long_url': link,
    }
    r = requests.post(
        'https://api-ssl.bitly.com/v4/bitlinks',
        headers=headers,
        json=data
    )
    if r.ok:
        return r.json()['link']
    return None


def get_link_clicks(token, short_link):
    parsed_link = urlparse(short_link)
    short_link = parsed_link.netloc + parsed_link.path
    headers = {
        'Authorization': f'Bearer {token}',
    }
    data = {
        'unit': 'day',
        'units': -1,
    }
    r = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{short_link}/clicks',
        headers=headers,
        params=data
    )
    if r.ok:
        return sum(item['clicks'] for item in r.json()['link_clicks'])
    return None


if __name__ == '__main__':
    user_token = os.getenv("TOKEN")

    description_string = '''This script does two things:
    a) show amount of clicks if short link is given
    b) shorten the link if full url is given'''

    parser = argparse.ArgumentParser(
        description=description_string,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('link', help='Link to process')
    args = parser.parse_args()
    user_link = args.link

    link_is_bitlink = is_bitlink(user_token, user_link)

    if link_is_bitlink:
        result = get_link_clicks(user_token, user_link)
    else:
        result = shorten_link(user_token, user_link)

    if result is None:
        print('Something went wrong :(')
    elif link_is_bitlink:
        print(f'Number of clicks: {result}')
    else:
        print(f'Short link: {result}')
