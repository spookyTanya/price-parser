from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from parsers import BiParser, RozetkaParser, ComfyParser, AlloParser


def parse_from_name(product_name):
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
    process_results(results)


def process_results(results):
    print(results)
    filtered_data = [item for item in results if item is not None]
    df = pd.DataFrame.from_records(filtered_data)
    print(df)
    print('min price = ', df['price'].min())

    df_melted = df.melt(id_vars=['website', 'is_available'], value_vars=['price', 'old_price'],
                        var_name='Price Type', value_name='Value')
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_melted[df_melted['is_available'] == True], x='website', y='Value', hue='Price Type', alpha=1.0)
    sns.barplot(data=df_melted[df_melted['is_available'] == False], x='website', y='Value', hue='Price Type', alpha=0.5)
    plt.xlabel('Website')
    plt.ylabel('Price')
    plt.title('Price and Old Price by Website')
    plt.show()



def get_name():
    product_name = input('Enter product name: ')
    parse_from_name(product_name)


get_name()
