from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from parsers import BiParser, RozetkaParser, ComfyParser, AlloParser
import db
import charts


def parse_from_name(product_name):
    print("Starting parsing for product", product_name)

    options = webdriver.ChromeOptions()
    options.add_argument("headless=True")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    results = [
        RozetkaParser(product_name, driver).parse_template(),
        BiParser(product_name, driver).parse_template(),
        ComfyParser(product_name, driver).parse_template(),
        AlloParser(product_name, driver).parse_template()]

    driver.quit()
    filtered_data = [item for item in results if item is not None]
    return filtered_data


def process_new_product(products: list):
    product_name = input('Enter product name: ')

    found = any(product_name == tup[1] for tup in products)

    if found:
        print("Product with same name is already saved")
        return

    results = parse_from_name(product_name)

    prod_id = db.add_product(product_name)
    for item in results:
        website_product_id = db.add_website_product((prod_id, item.get('website')))
        db.add_statistic(website_product_id, item)

    charts.new_product_chart(results)


def process_existing_product(existing_product):
    product_name = existing_product[1]

    if db.get_parsing_results_by_product(existing_product[0]) is not None:
        print('This product was already parsed today')
        return

    results = parse_from_name(product_name)

    for item in results:
        website_product_id = db.get_website_product(existing_product[0], item.get('website'))
        db.add_statistic(website_product_id[0], item)

    old_stats = get_product_statistics(existing_product)
    charts.saved_product_chart(old_stats)


def get_product_statistics(existing_product):
    old_stats = []

    website_products = db.get_website_products(existing_product[0])
    for website_product in website_products:
        website_product_id = website_product[0]

        res = db.get_parsing_results(website_product_id)
        for item in res:
            transformed = {
                'price': item[0],
                'old_price': item[1],
                'is_available': item[2],
                'link': item[3],
                'date': item[4],
                'website': website_product[1],
            }
            old_stats.append(transformed)

    return old_stats

