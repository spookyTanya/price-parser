from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

from parsers import BiParser, RozetkaParser


def parse_from_name(product_name):
    options = webdriver.ChromeOptions()
    options.headless = True

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    results = []

    results.append(RozetkaParser(product_name, driver).parse_template())
    results.append(BiParser(product_name, driver).parse_template())

    driver.quit()
    process_results(results)


def process_results(results):
    print(results)
    df = pd.DataFrame.from_records(results)
    print(df)
    print(df['price'])
    print(df['price'].min())


parse_from_name("lego квіти")
