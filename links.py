import os
import requests
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('TOKEN')


def collect_authorization_headers(token: str = TOKEN) -> dict:
    return {'Authorization': f'Bearer {token}'}


def convert_from_http_url(url: str) -> str:
    if url.startswith('http'):
        return url.split('//')[1]
    else:
        return url


def convert_to_http_url(url: str) -> str:
    if not url.startswith('http'):
        return 'http://' + url
    else:
        return url


def is_bitlink(url: str):
    url = convert_from_http_url(url)
    if url.startswith('bit.ly'):
        api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{url}'
        headers = collect_authorization_headers()
        resp = requests.get(api_url, headers=headers)
        if resp.ok:
            return True
        else:
            return False
    return False


def shorten_link(url: str) -> None:
    uri = 'bitlinks'
    api_url = f'https://api-ssl.bitly.com/v4/{uri}'
    headers = collect_authorization_headers()
    url = convert_to_http_url(url)
    payload = {
        'long_url': f'{url}'
    }
    try:
        resp = requests.post(api_url, headers=headers, json=payload)
        resp.raise_for_status()
        response = dict(resp.json())
        bitlink = response['link']
        return bitlink
    except requests.exceptions.HTTPError as ex:
        print(ex, 'Неправильная ссылка, попробуйте еще раз...', sep='\n')


def count_clicks(bitlink: str):
    bitlink = convert_from_http_url(bitlink)
    api_uri = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    headers = collect_authorization_headers()
    payload = {
        'unit': '',
        'units': '-1',
        'size': '',
        'unit_reference': '',
    }
    try:
        resp = requests.get(api_uri, headers=headers, params=payload)
        resp.raise_for_status()
        response = dict(resp.json())
        clicks = response['total_clicks']
        return clicks
    except requests.exceptions.HTTPError as ex:
        print(ex, 'Неправильная ссылка, попробуйте еще раз...', sep='\n')


def data_from_api(url: str) -> str:
    if is_bitlink(url):
        result = count_clicks(url)
    else:
        result = shorten_link(url)
    return result


def main() -> None:
    url = input()
    print(data_from_api(url))


if __name__ == '__main__':
    main()
