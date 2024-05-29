from bs4 import BeautifulSoup

domain = 'https://bi.ua'
search_page = domain + '/ukr/gsearch/?search='


def prepare_link(product_name):
    product_name = product_name.replace(' ', '%20')
    return search_page+product_name


def parse_html_from_bi(page_source):
    """Parses bi page"""

    print('parsing BI')
    soup = BeautifulSoup(page_source, "html5lib")

    try:
        catalog = soup.find(class_='catalog')
        item_wrapper = catalog.find(class_='goodsItem')

        if item_wrapper is not None:
            title = item_wrapper.find(class_='itemDes')
            print("title:", title.get_text())

            link = item_wrapper.find(class_='goodsItemLink')
            print(domain + link.attrs.get('href', ''))

            price_tag = item_wrapper.find('p', class_='costIco')

            if price_tag is not None:
                print("Current price", price_tag.get_text())
                old_price = price_tag.find_next_sibling(class_='old')
                if old_price is not None and old_price.get_text() != "":
                    print("slaaay, there is a discount, old price is", old_price.get_text())
            else:
                if item_wrapper.find(string='Повідомити про наявність') is not None:
                    print('Item is unavailable')
        else:
            print('No main wrapper found, outdated logic')
    except AttributeError:
        print("error during parsing")


def search_bi(product_name, driver):
    url = prepare_link(product_name)
    driver.get(url)

    parse_html_from_bi(driver.page_source)
