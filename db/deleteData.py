import sqlite3


def delete_product(product_id: int):
    con = sqlite3.connect("parsing.db")
    cur = con.cursor()

    cur.execute('DELETE FROM Products where id = ?', [product_id])

    con.commit()
    con.close()

