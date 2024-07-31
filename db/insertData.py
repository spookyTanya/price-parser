import sqlite3
from datetime import datetime


def add_product(product_name: str) -> int:
    con = sqlite3.connect("parsing.db")
    cur = con.cursor()

    query = 'INSERT INTO Products (name) VALUES (?)'
    cur.execute(query, (product_name,))

    con.commit()
    con.close()
    return cur.lastrowid


def add_website_product(website_product: tuple) -> int:
    con = sqlite3.connect("parsing.db")
    cur = con.cursor()

    query = 'INSERT INTO WebSiteProducts (product_id, website) VALUES (?, ?)'
    cur.execute(query, website_product)

    con.commit()
    con.close()
    return cur.lastrowid


def add_statistic(website_product_id: int, statistics: dict):
    con = sqlite3.connect("parsing.db")
    cur = con.cursor()

    query = ('INSERT INTO ParsingResults (website_product_id, price, old_price, is_available, link, date) VALUES (?, '
             '?, ?, ?, ?, ?)')

    data = (
        website_product_id,
        statistics.get('price'),
        statistics.get('old_price'),
        statistics.get('is_available'),
        statistics.get('link'),
        datetime.now().date().isoformat(),
    )

    cur.execute(query, data)

    con.commit()
    con.close()
