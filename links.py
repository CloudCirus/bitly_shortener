import os
import requests
from urllib.parse import urlparse, urlunparse

from dotenv import load_dotenv


def convert_to_http_url(url: str) -> str:
    parsed_url = urlparse(url)
    if parsed_url.scheme:
        return url
    if parsed_url.netloc:
        return urlunparse(parsed_url._replace(scheme='http'))
    return urlunparse(parsed_url._replace(
        scheme='http',
        netloc=parsed_url.path,
        path=''
    ))


def convert_from_http_url(url: str) -> str:
    parsed_url = urlparse(url)
    if parsed_url.scheme:
        return f'{parsed_url.netloc}{parsed_url.params}'
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
        'long_url': f'{url}'
    }

    resp = requests.post(api_url, headers=headers, json=payload)
    resp.raise_for_status()
    response = dict(resp.json())
    bitlink = response['link']
    return bitlink


def count_clicks(bitlink: str, headers: dict) -> int:
    bitlink = convert_from_http_url(bitlink)
    api_uri = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    payload = {
        'units': '-1',
    }

    resp = requests.get(api_uri, headers=headers, params=payload)
    resp.raise_for_status()
    response = dict(resp.json())
    clicks = response['total_clicks']
    return clicks


def main() -> None:
    load_dotenv()
    token = os.getenv('BITLY_TOKEN')
    headers = {'Authorization': f'Bearer {token}'}

    url = input()
    try:
        if is_bitlink(url, headers=headers):
            result = count_clicks(url, headers=headers)
        else:
            result = shorten_link(url, headers=headers)
        if result or result == 0:
            print(result)
    except requests.exceptions.HTTPError as ex:
        print(ex, 'Неправильная ссылка, попробуйте еще раз...', sep='\n')


if __name__ == '__main__':
    main()
