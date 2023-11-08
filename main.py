import requests
from bs4 import BeautifulSoup
import csv
from model import Product

def parser(url:str, max_item:int):
    create_csv()
    page = 1
    count_item = 0
    while max_item > count_item:
        list_products = []
        res = requests.get(f"{url}&PAGEN_1={page}")
        soup = BeautifulSoup(res.text, 'lxml')
        products = soup.find_all('div', class_='card-product')

        for product in products:
            if count_item >= max_item:
                break
            count_item += 1
            name = product.find('a', class_='card-product__name').text
            price = product.find('span', class_='b-price-def').text
            name_link = product.find('a', class_='card-product__name')
            link = f'https://komplekt-plus.ru{name_link["href"]}'
            list_products.append(Product(name=name, price=price, link=link))
        write_csv(list_products)
        page =+ 1

def create_csv():
    with open(f"santeh.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "price", "link"])

def write_csv(products:list):
    with open(f"santeh.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for product in products:
            writer.writerow([product.name, product.price, product.link])


if __name__ == "__main__":
    parser(url = 'https://komplekt-plus.ru/catalog/alyuminievye-sistemy/tatprof/mp-640-balkony-lodzhii-vitrazhi/?SORT_TO=36', max_item = 104)
