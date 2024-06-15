from bs4 import BeautifulSoup
import re

from .abstract import AbstractParser
from .helpers import get_number_from_string


class RozetkaParser(AbstractParser):
    SEARCH_PAGE_URL = "https://rozetka.com.ua/ua/search/?text="

    def prepare_link(self):
        product_name = self.product_name.replace(' ', '+')
        return self.SEARCH_PAGE_URL + product_name

    def parse_page(self):
        """Parses Rozetka page"""

        price, old_price = '', ''
        soup = BeautifulSoup(self.driver.page_source, "html5lib")

        try:
            item_wrapper = soup.find(class_='goods-tile')

            if item_wrapper is not None:
                title = item_wrapper.find(class_='goods-tile__title')
                # compare title with product name?

                link = item_wrapper.find(class_='product-link').attrs.get('href', '')

                price_tag = item_wrapper.find(class_='goods-tile__price-value')
                if price_tag is not None:
                    price = price_tag.get_text()
                    old_price_tag = item_wrapper.find(class_='goods-tile__price--old')
                    if old_price_tag is not None:
                        old_price = old_price_tag.get_text()

                is_available = item_wrapper.find(string=re.compile('Немає в наявності')) is None

                return {
                    'price': get_number_from_string(price),
                    'old_price': get_number_from_string(old_price),
                    'is_available': is_available,
                    'link': link
                }
            else:
                print('No main wrapper found, outdated logic')
                return None
        except AttributeError:
            print("error during parsing")

        return None

