import sqlite3


def create_db():
    con = sqlite3.connect("parsing.db")
    cur = con.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS Products(id INTEGER PRIMARY KEY, name VARCHAR(100) NOT NULL)')
    cur.execute('''CREATE TABLE IF NOT EXISTS WebSiteProducts(
                       id INTEGER PRIMARY KEY,
                       product_id INTEGER NOT NULL,
                       website VARCHAR(100),
                       FOREIGN KEY (product_id)
                       REFERENCES Products(id))''')
    cur.execute('''CREATE TABLE IF NOT EXISTS ParsingResults( 
                       id INTEGER PRIMARY KEY,
                       website_product_id INTEGER NOT NULL,
                       price REAL NOT NULL, old_price REAL, 
                       is_available BOOLEAN NOT NULL,
                       link VARCHAR(250),
                       date TEXT,
                       FOREIGN KEY (website_product_id)
                       REFERENCES WebSiteProducts(id))''')

    con.commit()
    con.close()


