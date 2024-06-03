from abc import ABC, abstractmethod


class AbstractParser(ABC):

    def __init__(self, product_name, driver):
        self.link = None
        self.product_name = product_name
        self.driver = driver

    def parse_template(self):
        self.link = self.prepare_link()
        self.get_page()
        self.parse_page()

    def get_page(self):
        self.driver.get(self.link)

    @abstractmethod
    def prepare_link(self):
        pass

    @abstractmethod
    def parse_page(self):
        pass
