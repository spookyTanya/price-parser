from abc import ABC, abstractmethod
import random
import time


class AbstractParser(ABC):

    def __init__(self, product_name, driver):
        self.link = None
        self.product_name = product_name
        self.driver = driver

    def parse_template(self) -> dict:
        self.link = self.prepare_link()
        self.random_delay()
        self.get_page()
        print(self.driver.current_url)
        if self.check_redirect():
            return self.parse_detail_page()
        else:
            return self.parse_search_page()

    def get_page(self):
        self.driver.get(self.link)

    @staticmethod
    def random_delay():
        time.sleep(random.uniform(2, 5))

    @abstractmethod
    def prepare_link(self) -> str:
        pass

    @abstractmethod
    def parse_search_page(self):
        pass

    @abstractmethod
    def parse_detail_page(self):
        pass

    @abstractmethod
    def check_redirect(self) -> bool:
        pass
