import requests
from bs4 import BeautifulSoup

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

def main():
    r = requests.get(url=f'https://www.salomon.com/en-us/shop/product/acs-pro-advanced-lg8207.html#color=74236', headers=headers)
    pageCount = 0
    for page in range(1000):
        r = requests.get(url=f'https://www.salomon.com/en-us/shop/men/shoes.html?p={page}', headers=headers)
        print(f'Вычисляем количество страниц. Проверено:{page} ')
        if r.url != f'https://www.salomon.com/en-us/shop/men/shoes.html?p={page}':
            pageCount = page - 1
            break

    if pageCount == 0: return


    with open('salomon.html', 'w', encoding='utf-8') as file:
        file.write(r.text)


if __name__ == '__main__':
    main()