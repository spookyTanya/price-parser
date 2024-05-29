from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions
from websites.rozetka import search_rozetka
from websites.bi import search_bi


def parse_from_name(product_name):
    options = ChromeOptions()
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    search_rozetka(product_name, driver)
    search_bi(product_name, driver)

    driver.quit()


parse_from_name("lego квіти")
