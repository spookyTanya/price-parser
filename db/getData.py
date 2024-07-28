import sqlite3


def get_website_products(product_id: int) -> list:
    con = sqlite3.connect("parsing.db")
    cur = con.cursor()

    query = 'SELECT id, website FROM WebSiteProducts WHERE product_id=?'
    cur.execute(query, [product_id])

    row = cur.fetchall()
    con.close()
    return row


def get_products() -> list:
    con = sqlite3.connect("parsing.db")
    cur = con.cursor()

    query = 'SELECT * FROM Products'
    cur.execute(query)

    rows = cur.fetchall()
    con.close()
    return rows


def get_parsing_results(website_product_id: int) -> list:
    con = sqlite3.connect("parsing.db")
    cur = con.cursor()

    query = 'SELECT price, old_price, is_available, link, date FROM ParsingResults WHERE website_product_id=?'
    cur.execute(query, [website_product_id])

    rows = cur.fetchall()
    con.close()
    return rows

