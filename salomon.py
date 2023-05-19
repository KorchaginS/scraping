import requests
import re
from bs4 import BeautifulSoup
import json
import time
from proxy import proxyCon
from selenium import webdriver
from selenium.webdriver.chrome.service import  Service

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}

def main():

    s = Service(executable_path='C:\chromedriver\chromedriver')

    driver = webdriver.Chrome(
        executable_path= 'C:\chromedriver\chromedriver'
    )
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{
        'source': '''
            delete cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            delete cdc_adoQpoasnfa76pfcZLmcfl_Object;
            delete cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
        '''
    })
    driver.maximize_window()

    driver.get('https://www.salomon.com/en-us/shop/men/shoes.html')
    time.sleep(4)
    driver.close()
    result = []
    r = requests.get(url=f'https://www.salomon.com/en-us/shop/men/shoes.html', headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    cards = soup.find_all(class_='product-tile_body')

    for card in cards:
        dict = {}
        a = card.find('a')
        dict['Name'] = a.get_text()
        dict['Link'] = a.get('href')
        dict['Price'] = getPrice(dict['Link'])
        result.append(dict)
        time.sleep(2)

    time.sleep(3)
    pageCount = 0
    for page in range(1000):
        r = requests.get(url=f'https://www.salomon.com/en-us/shop/men/shoes.html?p={page}', headers=headers)
        print(f'Вычисляем количество страниц. Проверено:{page} ')
        time.sleep(3)
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
            resDict['Price'] = getPrice(resDict['Link'])
            result.append(resDict)
        time.sleep(3)
    with open('salomon_result.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)


def getPrice(url):
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    try:
        price = soup.find('div', class_='product-information_row').find('span').get_text().replace('$', '')
    except:
        price = soup.find('div', class_='product-sidebar-price').find('span').get_text().replace('$', '')
    return price

if __name__ == '__main__':
    main()