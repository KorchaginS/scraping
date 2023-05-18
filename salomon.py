import requests
import re
from bs4 import BeautifulSoup
import json

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

def main():

    result = []
    r = requests.get(url=f'https://www.salomon.com/en-us/shop/men/shoes.html', headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    cards = soup.find_all(class_='product-tile_body')

    for card in cards:
        dict = {}
        a = card.find('a')
        dict['Name'] = a.get_text()
        dict['Link'] = a.get('href')
        result.append(dict)


    pageCount = 0
    for page in range(1000):
        r = requests.get(url=f'https://www.salomon.com/en-us/shop/men/shoes.html?p={page}', headers=headers)
        print(f'Вычисляем количество страниц. Проверено:{page} ')
        if r.url != f'https://www.salomon.com/en-us/shop/men/shoes.html?p={page}':
            pageCount = page - 1
            break

    if pageCount == 0: return

    for page in range(2, pageCount + 1):
        print(f'Обрабатывается страница {page}')
        r = requests.get(url=f'https://www.salomon.com/en-us/shop/men/shoes.html?p={page}&is_scroll=1', headers=headers)

        inputList = []
        linskList = []

        [inputList.append(m.start()) for m in re.finditer('content=', r.text)]
        [linskList.append(m.start()) for m in re.finditer('href=', r.text)]

        count = 0
        names = []
        links = []

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
                        word = word.replace('content=','')
                        word = word.replace('&#x20;', ' ')
                        word = word.replace(';', ' ')
                        word = word.replace('\\n', '').replace('\"', '').replace('\\', '')
                        names.append(word)
                        break
            elif count == 7:
                count = 0

        for elem in linskList:
            link = ''
            position = elem
            while True:
                    if r.text[position] != ' ':
                        link += r.text[position]
                        position += 1
                    else:
                        link = link.replace('href=', '')
                        link = link.replace('\\n', '').replace('\"', '').replace('\\', '')
                        if 'product' in link and not link in links:
                            links.append(link)
                        break


        for position in range(len(names)):
            resDict = {}
            resDict['Name'] = names[position]
            resDict['Link'] = links[position]
            result.append(resDict)

    with open('salomon_result.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)




if __name__ == '__main__':
    main()