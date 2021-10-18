import argparse
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def convert_to_http_url(url: str) -> str:
    parsed_url = urlparse(url)
    if parsed_url.scheme:
        return url
    return f'http://{url}'


def convert_from_http_url(url: str) -> str:
    parsed_url = urlparse(url)
    if parsed_url.scheme:
        return f'{parsed_url.netloc}{parsed_url.path}'
    return url


def is_bitlink(url: str, headers: dict) -> bool:
    url = convert_from_http_url(url)
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{url}'
    resp = requests.get(api_url, headers=headers)
    return resp.ok


def shorten_link(url: str, headers: dict) -> str:
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks'
    url = convert_to_http_url(url)
    payload = {
        'long_url': url
    }

    resp = requests.post(api_url, headers=headers, json=payload)
    resp.raise_for_status()
    response = resp.json()
    bitlink = response['link']
    return bitlink


def count_clicks(bitlink: str, headers: dict) -> int:
    bitlink = convert_from_http_url(bitlink)
    api_uri = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    payload = {
        'units': -1,
    }

    resp = requests.get(api_uri, headers=headers, params=payload)
    resp.raise_for_status()
    response = resp.json()
    total_clicks = response['total_clicks']
    return total_clicks


def main() -> None:
    load_dotenv()
    token = os.getenv('BITLY_TOKEN')
    headers = {'Authorization': f'Bearer {token}'}

    parser = argparse.ArgumentParser(
        description='Script convert url to bitlink or show all clicks for bitlink'
    )
    parser.add_argument('url', help='url or bitlink')

    try:
        args = parser.parse_args()
        url = args.url
        if is_bitlink(url, headers=headers):
            total_clicks = count_clicks(url, headers=headers)
            print('Clicks:', total_clicks)
        else:
            shorted_link = shorten_link(url, headers=headers)
            print('Shorten link:', shorted_link)
    except requests.exceptions.HTTPError:
        print('Wrong url, please try again,\nURL like: google.com or bitlink', sep='\n')


if __name__ == '__main__':
    main()
