import json

from fake_useragent import UserAgent
import requests
import time
from random import random

result = []

ua = UserAgent()

headers = {
    'Accept':'application/json, text/plain, */*',
    'User-Agent':ua.random
}


def collectData(cat_type=2):
    offset = 0
    data = []
    counter = 0
    while True:
        counter += 1
        if counter > 10:
            break

        print(f"Обрабатывается страница {counter}")
        r = requests.get(f'https://cs.money/1.0/market/sell-orders?limit=60&offset={offset}&order=desc&sort=discount&type={cat_type}')
        if r.text.find('{"errors":[{"code":2}]}') != -1:
            break

        data = r.json()
        items = data.get('items')

        for i in items:

            if i['pricing']['discount'] > 0.1:
                result.append(
                    {
                     'full_name': i['asset']['names']['full'],
                     'discount': i['pricing']['discount'],
                     'item_price': i['pricing']['computed']
                    }
                )
                try:
                    result[-1]['3d'] = i['links']['3d']
                except:
                    result[-1]['3d'] =  ''

        offset += 60

    with open('CS_data.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)




def main():
    collectData()

if __name__ == '__main__':
    main()