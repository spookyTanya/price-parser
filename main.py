from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from parsers import BiParser, RozetkaParser


def parse_from_name(product_name):
    options = webdriver.ChromeOptions()
    options.headless = True

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    RozetkaParser(product_name, driver).parse_template()
    BiParser(product_name, driver).parse_template()

    driver.quit()


parse_from_name("lego квіти")
