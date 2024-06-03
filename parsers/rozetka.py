from bs4 import BeautifulSoup
import re

from .abstract import AbstractParser


class RozetkaParser(AbstractParser):
    SEARCH_PAGE_URL = "https://rozetka.com.ua/ua/search/?text="

    def prepare_link(self):
        product_name = self.product_name.replace(' ', '+')
        return self.SEARCH_PAGE_URL + product_name

    def parse_page(self):
        """Parses Rozetka page"""

        soup = BeautifulSoup(self.driver.page_source, "html5lib")

        try:
            item_wrapper = soup.find(class_='goods-tile')

            if item_wrapper is not None:
                title = item_wrapper.find(class_='goods-tile__title')
                print("title:", title.get_text())

                link = item_wrapper.find(class_='product-link')
                print(link.attrs.get('href', ''))

                price_tag = item_wrapper.find(class_='goods-tile__price-value')
                if price_tag is not None:
                    print("Current price", price_tag.get_text())
                    old_price = price_tag.find_previous_sibling('goods-tile__price--old')
                    if old_price is not None and old_price.get_text() != "":
                        print("slaaay, there is a discount, old price is", old_price.get_text())

                if item_wrapper.find(string=re.compile('Немає в наявності')) is not None:
                    print('Item is unavailable')
            else:
                print('No main wrapper found, outdated logic')
        except AttributeError:
            print("error during parsing")

