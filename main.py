import db
from processingHandlers import process_new_product, process_existing_product, get_product_statistics

products = []
product_ids = []


def get_product_id_from_input():
    try:
        product_id = int(input("Enter product id: "))
        if product_id in product_ids:
            return product_id
        else:
            print("Error: No product found by given id")
    except ValueError:
        print("Error: Non id value given")

    return None


def load_products():
    global products, product_ids
    products = db.get_products()
    product_ids = []
    for product in products:
        product_ids.append(product[0])


if __name__ == '__main__':
    db.create_db()
    load_products()

    while True:
        operation = input("What would you like to do?\n"
                          "a) Output saved products\n"
                          "b) Check prices for saved product\n"
                          "c) Show statistics for saved product\n"
                          "d) Create new product\n"
                          "e) Delete saved product\n"
                          "f) Quit\n"
                          "> ")

        match operation:
            case "a" | "A":
                for product in products:
                    print('Id: %d, Title: %s' % product)

            case "b" | "B":
                product_id = get_product_id_from_input()
                product = products[product_ids.index(product_id)]
                process_existing_product(product)

            case "c" | "C":
                product_id = get_product_id_from_input()
                product = products[product_ids.index(product_id)]
                stats = get_product_statistics(product)
                print(stats)

            case "d" | "D":
                process_new_product()
                load_products()

            case "e" | "E":
                product_id = get_product_id_from_input()
                db.delete_product(product_id)
                load_products()

            case "f" | "F":
                break
            case _:
                print("Error: Invalid operation")

