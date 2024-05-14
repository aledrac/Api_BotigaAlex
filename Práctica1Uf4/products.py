import db_botiga

def product_schema(product) -> dict:
    return {"product_id": product[0],
            "name": product[1],
            "description": product[2],
            "company": product[3],
            "price": product[4],
            "units": product[5]
            }

def products_schema(products) -> dict:
    return [product_schema(product) for product in products]


def product_info_schema(product_info) -> dict:
    return {"category_name": product_info[0],
            "subcategory_name": product_info[1],
            "product_name": product_info[2],
            "product_brand": product_info[3],
            "product_price": product_info[4]
            }

def products_info_schema(products_info) -> dict:
    return [product_info_schema(product_info) for product_info in products_info]