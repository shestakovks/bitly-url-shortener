from dotenv import load_dotenv
from urllib.parse import urlparse
import argparse
import os
import requests


def get_args():
    description_string = '''This script does two things:
    a) shows amount of clicks if short link is given
    b) shortens the link if full url is given'''

    parser = argparse.ArgumentParser(
        description=description_string,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('link', help='Link to process')
    args = parser.parse_args()
    return args


def is_bitlink(token, link):
    parsed_link = urlparse(link)
    link = parsed_link.netloc + parsed_link.path
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{link}',
        headers=headers
    )
    return response.ok


def shorten_link(token, link):
    headers = {
        'Authorization': f'Bearer {token}',
    }
    data = {
        'long_url': link,
    }
    response = requests.post(
        'https://api-ssl.bitly.com/v4/bitlinks',
        headers=headers,
        json=data
    )
    response.raise_for_status()
    return response.json()['link']


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
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{short_link}/clicks',
        headers=headers,
        params=data
    )
    response.raise_for_status()
    return sum(item['clicks'] for item in response.json()['link_clicks'])


if __name__ == '__main__':
    load_dotenv()

    user_token = os.getenv("TOKEN")
    args = get_args()
    user_link = args.link

    try:
        link_is_bitlink = is_bitlink(user_token, user_link)
        if link_is_bitlink:
            link_clicks = get_link_clicks(user_token, user_link)
            print(f'Number of clicks: {link_clicks}')
        else:
            short_link = shorten_link(user_token, user_link)
            print(f'Short link: {short_link}')
    except requests.exceptions.RequestException:
        print('Something went wrong :(')
