import requests
from bs4 import BeautifulSoup

from typing import List, Mapping
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import csv


def cmc_api():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'1',
    'limit':'5000',
    'convert':'USD'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '4162d11d-11c6-4c50-95d3-1d6a4c815919',
    }

    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        [print(x['name'], x['cmc_rank']) for x in data['data']]
        with open('hello.csv', 'w', encoding='UTF8', newline='') as f:
            # create the csv writer
            writer = csv.writer(f)
            writer.writerow(['name', 'rank'])
            for x in data['data']:
                # write a row to the csv file
                writer.writerow([x['name'], x['cmc_rank']])
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

def read_csv():
    currency_list = []
    with open('hello.csv', 'r') as f:
        csv_reader = csv.reader(f)
        for line in csv_reader:
            # process each line
            currency_list.append(line)
    return currency_list

def open_currency_urls():
    currency_lists = read_csv()
    coin_watchlists_numbers = []
    
    
    for coin in currency_lists:
        url = 'https://coinmarketcap.com/currencies/' + \
                coin[0].replace(' ', '-').replace('.', '-').replace('+', '').replace('/', '').replace('!', '') + '/'
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            mydivs = soup.find_all("div", {"class": "namePill"})
            if len(mydivs) == 0:
                print(coin, "cannot find watchlist dev" )
        except Exception as e:
            print('bs4 reading page exception: ', e)
        print(coin[0], coin[1])
        try:
            w_n = int(mydivs[2].text.split()[1].replace(',','').replace(' ',''))
            coin_watchlists_numbers.append([ coin[1],coin[0], w_n])
            print(coin[0], mydivs[2].text.split()[1].replace(',',''))
        except Exception as e:
            print('getting watchlists number exception', e)
        if int(coin[1])%100 == 0:
            with open('goodbuy.csv', 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                for x in coin_watchlists_numbers:
                    writer.writerow(x)

if __name__ == "__main__":
    open_currency_urls()