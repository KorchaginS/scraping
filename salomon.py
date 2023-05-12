import requests
import re
from bs4 import BeautifulSoup
import json

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

def main():

    r = requests.get(url=f'https://www.salomon.com/en-us/shop/men/shoes.html?p=2&is_scroll=1', headers=headers)

    inputList = []

    [inputList.append(m.start()) for m in re.finditer('content=', r.text)]

    count = 0
    names = []

    for elem in inputList:
        count += 1
        if count == 1:
            word = ''
            position = elem
            while True:
                if r.text[position] != ' ':
                    word += r.text[position]
                    position += 1
                else:
                    names.append(word)
                    break
        elif count == 7:
            count = 0

    a = 0
    # r = requests.get(url=f'https://www.salomon.com/en-us/shop/product/acs-pro-advanced-lg8207.html#color=74236', headers=headers)
    # pageCount = 0
    # for page in range(1000):
    #     r = requests.get(url=f'https://www.salomon.com/en-us/shop/men/shoes.html?p={page}', headers=headers)
    #     print(f'Вычисляем количество страниц. Проверено:{page} ')
    #     if r.url != f'https://www.salomon.com/en-us/shop/men/shoes.html?p={page}':
    #         pageCount = page - 1
    #         break
    #
    # if pageCount == 0: return
    #
    #
    # with open('salomon.html', 'w', encoding='utf-8') as file:
    #     file.write(r.text)


if __name__ == '__main__':
    main()