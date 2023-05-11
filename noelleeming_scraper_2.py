"""this script intend to scrape information of all products in the given url"""
import requests
import pandas as pd
# import time
import re
from bs4 import BeautifulSoup


def product_dict(product):
    title = ['skuCode', 'productName', 'price', 'productCategory', 'productBrand', 'position']
    product_info = [re.sub('.*?:|[},"]', '', info).strip() for info in product['data-product-info'].split(sep='",')]
    product_dict = {k: v for k, v in zip(title, product_info)}

    return product_dict


def check_connection(url):
    """check connection of given url"""
    try:
        r = requests.get(url)  # open the url
    except Exception as exc:
        print(exc)
        exit()

    if r.status_code != 200:
        print(r.status_code)
        exit()
    else:
        pass


def get_pages(url):
    r = requests.get(url)
    src = r.content
    soup = BeautifulSoup(src, 'lxml')

    next_button = soup.find('i', class_='arrow -right')
    total_page = next_button.parent.parent.previous_sibling.string

    return int(total_page)


def main():
    base_url = f'https://www.noelleeming.co.nz/shop/computers-tablets/tablets/c8001-ctablet-p1.html'
        # f'https://www.noelleeming.co.nz/shop/computers-tablets/tablets/c8001-ctablet-p1.html'
    check_connection(base_url)

    product_list = []
    file_name = 'noelleeming_scraper_2.csv'

    for i in range(1, get_pages(base_url) + 1):
        print('getting page ' + str(i))
        url = base_url.replace('-p1', f'-p{str(i)}')
        print(url)
        r = requests.get(url)
        src = r.content  # assign the content of responded html to src variable
        soup = BeautifulSoup(src, 'lxml')  # making a soup
        all_product = soup.find_all('div', class_='inner product-list__item')

        for product in all_product:
            product_data = product_dict(product)
            product_list.append(product_data)

    df = pd.DataFrame(product_list)
    df.to_csv(file_name, index=False)
    return print('Done!')


if __name__ == '__main__':
    # start_time = time.time()
    main()
    # print("--- %s seconds ---" % (time.time() - start_time))
