import requests
import bs4 as bs
import urllib.request
import pandas


def main():
    url = "http://emmi.rs/konfigurator/proizvodi.10.html?go=true&Id=10&categoryId=214&limit=-1&offset=0"

    raw_html = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(raw_html, "lxml")
    items = soup.findAll('div', {'class': 'productListItem'})
    names = []
    prices = []
    for item in items:
        names.append(item.find('div', {'class': 'productListTitle'}).a.text.replace('č', 'c'))
        prices.append(item.find('div', {'class': 'productListPrice'}).span.text.replace('.', ''))

    print(names, '\n', prices)

    with open('emmi_gpus.csv', 'w') as f:
        f.write('Product Name,Price in RSD\n')
        for i in range(len(names)):
            f.write(names[i] + ',' + prices[i] + '\n')


if __name__ == '__main__':
    main()
