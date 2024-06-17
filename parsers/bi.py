from bs4 import BeautifulSoup

from .abstract import AbstractParser
from .helpers import get_number_from_string


class BiParser(AbstractParser):
    DOMAIN = 'https://bi.ua'
    SEARCH_PAGE_URL = DOMAIN + '/ukr/gsearch/?search='

    def prepare_link(self):
        product_name = self.product_name.replace(' ', '%20')
        return self.SEARCH_PAGE_URL + product_name

    def check_redirect(self):
        return self.SEARCH_PAGE_URL not in self.driver.current_url

    def parse_search_page(self):
        price, old_price = '', ''
        soup = BeautifulSoup(self.driver.page_source, "html5lib")
    
        try:
            catalog = soup.find(class_='catalog')
            item_wrapper = catalog.find(class_='goodsItem')
    
            if item_wrapper is not None:
                link = item_wrapper.find(class_='goodsItemLink')
                price_tag = item_wrapper.find('p', class_='costIco')
    
                if price_tag is not None:
                    price = price_tag.get_text()
                    old_price_tag = price_tag.find_next_sibling(class_='old')
                    if old_price_tag is not None:
                        old_price = old_price_tag.get_text()

                is_available = item_wrapper.find(string='Повідомити про наявність') is None

                return {
                    'price': get_number_from_string(price),
                    'old_price': get_number_from_string(old_price),
                    'is_available': is_available,
                    'link': self.DOMAIN + link.attrs.get('href', ''),
                    'website': 'bi.ua',
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
            item_wrapper = soup.find(class_='mainWR')

            if item_wrapper is not None:
                title = item_wrapper.find('h1', itemprop='name')
                print("title:", title.get_text())

                price_tag = item_wrapper.find('p', itemprop='price')

                if price_tag is not None:
                    price = price_tag.get_text()
                    old_price_tag = price_tag.find_next_sibling(class_='old')
                    if old_price_tag is not None:
                        old_price = old_price_tag.get_text()

                is_available = item_wrapper.find(string='Повідомити про наявність') is None

                return {
                    'price': get_number_from_string(price),
                    'old_price': get_number_from_string(old_price),
                    'is_available': is_available,
                    'link': self.driver.current_url,
                    'website': 'bi.ua',
                }
            else:
                print('No main wrapper found, outdated logic')
                return None
        except AttributeError:
            print("error during parsing")
            return None

