from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import matplotlib.pyplot as plt

from parsers import BiParser, RozetkaParser, ComfyParser, AlloParser


def parse_from_name(product_name):
    options = webdriver.ChromeOptions()
    options.add_argument("headless=True")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    results = []

    results.append(RozetkaParser(product_name, driver).parse_template())
    results.append(BiParser(product_name, driver).parse_template())
    results.append(ComfyParser(product_name, driver).parse_template())
    results.append(AlloParser(product_name, driver).parse_template())

    driver.quit()
    process_results(results)


def process_results(results):
    print(results)
    filtered_data = [item for item in results if item is not None]
    df = pd.DataFrame.from_records(filtered_data)
    print(df)
    print(df['price'])
    print(df['price'].min())

    # df.plot(kind='hist', x='website', y='price')
    # plt.show()


def get_name():
    product_name = input('Enter product name: ')
    parse_from_name(product_name)


get_name()
