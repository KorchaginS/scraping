import requests
import json
from bs4 import BeautifulSoup
import os

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}

def get_data_file(headers):

    resultList = []
    page = 0
    while True:
        url = f'https://s3.landingfolio.com/inspiration?page={page}&sortBy=free-first'
        r = requests.get(url=url, headers=headers)
        empty = True
        data = r.json()

        for item in data:
            if 'colors' in item:
                empty = False
                dataDict = {}
                dataDict['title'] = item.get('title').strip()
                dataDict['url'] = item.get('url')

                response = requests.get(url=f'https://s3.landingfolio.com/inspiration/post/{item.get("slug")}', headers=headers)
                cardData = response.json()
                dataDict['description'] = cardData.get('description')
                images = []
                screenshots = item.get('screenshots')
                for imgItem in screenshots:
                    imagesInItem = imgItem.get('images')
                    images.append(f'https://landingfoliocom.imgix.net/{imagesInItem.get("desktop")}?&q=75&auto=format&w=750')
                    images.append(f'https://landingfoliocom.imgix.net/{imagesInItem.get("mobile")}?&q=75&auto=format&w=750')
                dataDict['images'] = images
                resultList.append(dataDict)



        if empty:
            with open('result.json', 'w', encoding='utf-8') as file:
                json.dump(resultList, file, indent=4, ensure_ascii=False)
            break
        print(f'[+] Страница {page} обработана')
        page += 1

def download_images():

    with open('result.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    items_len = len(data)
    c = 1

    for item in data[:10]:
        item_name = item.get('title')
        item_imgs = item.get('images')

        if not os.path.exists(f'data/{item_name}'):
            os.mkdir(f'data/{item_name}')

        count = 0
        for img in item_imgs:
            r = requests.get(url=img)

            with open(f'data/{item_name}/{count}.png', 'wb') as file:
                file.write(r.content)
            count += 1
        print(f'[+] Download {c}/{items_len}')
        c += 1

    return '[INFO] Work finished!'

def main():
    #print(get_data_file(headers= headers))
    print(download_images())

if __name__ == '__main__':
    main()