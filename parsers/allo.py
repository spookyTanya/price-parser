# lamp%20квіти

from bs4 import BeautifulSoup

from .abstract import AbstractParser
from .helpers import get_number_from_string


class AlloParser(AbstractParser):
    SEARCH_PAGE_URL = "https://allo.ua/ua/catalogsearch/result"

    def prepare_link(self):
        product_name = self.product_name.replace(' ', '+')
        return self.SEARCH_PAGE_URL + '/?q=' + product_name

    def check_redirect(self):
        return self.SEARCH_PAGE_URL not in self.driver.current_url

    def parse_search_page(self):
        price, old_price = '', ''
        soup = BeautifulSoup(self.driver.page_source, "html5lib")

        try:
            item_wrapper = soup.find(class_='products-layout__container')

            if item_wrapper is not None:
                title = item_wrapper.find(class_='product-card__title')
                # compare title with product name?

                price_tag = item_wrapper.find(class_='v-pb__cur')
                if price_tag is not None:
                    price = price_tag.find(class_='sum').get_text()
                    old_price_tag = item_wrapper.find(class_='v-pb__old')
                    if old_price_tag is not None:
                        old_price = old_price_tag.find(class_='sum').get_text()

                is_available = item_wrapper.find(string='Немає в наявності') is None

                return {
                    'price': get_number_from_string(price),
                    'old_price': get_number_from_string(old_price),
                    'is_available': is_available,
                    'link': title.attrs.get('href', ''),
                    'website': 'allo.ua',
                }
            else:
                print('No main wrapper found, outdated logic')
                return None
        except AttributeError:
            print("error during parsing")

        return None

    def parse_detail_page(self):
        price, old_price = '', ''
        soup = BeautifulSoup(self.driver.page_source, "html5lib")

        try:
            item_wrapper = soup.find(class_='product-view')

            if item_wrapper is not None:
                title = item_wrapper.find(itemprop='name')

                price_tag = item_wrapper.find(itemprop='offers')
                if price_tag is not None:
                    price = price_tag.find(class_='sum').get_text()
                    old_price_tag = item_wrapper.find(class_='p-trade-price__old')
                    if old_price_tag is not None:
                        old_price = old_price_tag.find(class_='sum').get_text()

                is_available = item_wrapper.find(string='Немає в наявності') is None

                return {
                    'price': get_number_from_string(price),
                    'old_price': get_number_from_string(old_price),
                    'is_available': is_available,
                    'link': title.attrs.get('href', ''),
                    'website': 'allo.ua',
                }
            else:
                print('No main wrapper found, outdated logic')
                return None
        except AttributeError:
            print("error during parsing")

        return None

