from bs4 import BeautifulSoup

from .abstract import AbstractParser
from .helpers import get_number_from_string


class BiParser(AbstractParser):
    DOMAIN = 'https://bi.ua'
    SEARCH_PAGE = DOMAIN + '/ukr/gsearch/?search='

    def prepare_link(self):
        product_name = self.product_name.replace(' ', '%20')
        return self.SEARCH_PAGE + product_name

    def parse_page(self):
        price, old_price = '', ''
        soup = BeautifulSoup(self.driver.page_source, "html5lib")
    
        try:
            catalog = soup.find(class_='catalog')
            item_wrapper = catalog.find(class_='goodsItem')
    
            if item_wrapper is not None:
                title = item_wrapper.find(class_='itemDes')
                print("title:", title.get_text())
    
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
                    'link': self.DOMAIN + link.attrs.get('href', '')
                }
            else:
                print('No main wrapper found, outdated logic')
                return None
        except AttributeError:
            print("error during parsing")
            return None

