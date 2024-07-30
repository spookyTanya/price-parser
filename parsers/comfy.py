from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from .abstract import AbstractParser
from .helpers import get_number_from_string


class ComfyParser(AbstractParser):
    SEARCH_PAGE_URL = 'https://comfy.ua/ua/search'

    def prepare_link(self) -> str:
        product_name = self.product_name.replace(' ', '+')
        return self.SEARCH_PAGE_URL + '/?q=' + product_name

    def check_redirect(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".common-template"))
            )
        except Exception as e:
            print("An error occurred:", e)
        finally:
            return self.SEARCH_PAGE_URL not in self.driver.current_url

    def parse_search_page(self):
        price, old_price = '', ''
        soup = BeautifulSoup(self.driver.page_source, "html5lib")

        try:
            catalog = soup.find(class_='products-catalog')
            item_wrapper = catalog.find(class_='products-list-item')

            if item_wrapper is not None:
                title = item_wrapper.find(class_='products-list-item__name')

                price_tag = item_wrapper.find(class_='products-list-item__actions-price-current')

                if price_tag is not None:
                    price = price_tag.get_text()
                    old_price_tag = price_tag.find_previous_sibling(class_='products-list-item__actions-price-old')
                    if old_price_tag is not None:
                        old_price = old_price_tag.get_text()

                is_available = item_wrapper.find(string='Товар закінчився') is None

                return {
                    'price': get_number_from_string(price),
                    'old_price': get_number_from_string(old_price),
                    'is_available': is_available,
                    'link': title.attrs.get('href', ''),
                    'website': 'comfy.ua',
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

        self.check_and_close_modal()

        try:
            item_wrapper = soup.find(class_='general-tab')

            if item_wrapper is not None:
                price_tag = item_wrapper.find(class_='price__current')

                if price_tag is not None:
                    price = price_tag.get_text()
                    old_price_tag = soup.find(class_='price__old-price')
                    if old_price_tag is not None:
                        old_price = old_price_tag.get_text()

                is_available = item_wrapper.find(string='Товар закінчився') is None

                return {
                    'price': get_number_from_string(price),
                    'old_price': get_number_from_string(old_price),
                    'is_available': is_available,
                    'link': self.driver.current_url,
                    'website': 'comfy.ua',
                }
            else:
                print('No main wrapper found, outdated logic')
                return None
        except AttributeError:
            print("error during parsing")
            return None

    def check_and_close_modal(self):
        soup = BeautifulSoup(self.driver.page_source, 'html5lib')

        modal = soup.find('div', class_='q-dialog')
        if modal is not None:
            modal.find(class_='br-recom__close-btn').click()
