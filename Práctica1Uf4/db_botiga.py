from conexion import db_botiga

def read():
    try:
        conn = db_botiga()
        cur = conn.cursor()
        cur.execute("select * from product")
    
        products = cur.fetchall()
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
    
    return products

def read_id(id):
    try:
        conn = db_botiga()
        cur = conn.cursor()
        query = "select * from product WHERE product_id = %s"
        value = (id,)
        cur.execute(query,value)
    
        product = cur.fetchone()

    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
    
    return product


def create(name,description,company,price,units,subcategory_id):
    try:
        conn = db_botiga()
        cur = conn.cursor()
        query = "insert into product (name,description,company,price,units,subcategory_id) VALUES (%s,%s,%s,%s,%s,%s);"
        values=(name,description,company,price,units,subcategory_id)
        cur.execute(query,values)
    
        conn.commit()
        film_id = cur.lastrowid
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()

    return film_id

def update_preu(preu,id):
    try:
        conn = db_botiga()
        cur = conn.cursor()
        query = "update product SET price = %s WHERE product_id = %s;"
        values=(id,preu)
        cur.execute(query,values)
        updated_recs = cur.rowcount
    
        conn.commit()
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()

    return updated_recs


def delete_products(id):
    try:
        conn = db_botiga()
        cur = conn.cursor()
        query = "DELETE FROM product WHERE id = %s;"
        cur.execute(query,(id,))
        deleted_recs = cur.rowcount
        conn.commit()
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
        
    return deleted_recs


def read_all_products():
    try:
        conn = db_botiga()
        cur = conn.cursor()
        query = """
        SELECT c.name AS category_name, sc.name AS subcategory_name,
               p.name AS product_name, p.company AS product_brand,
               p.price AS product_price
        FROM product p
        INNER JOIN subcategory sc ON p.subcategory_id = sc.subcategory_id
        INNER JOIN category c ON sc.category_id = c.category_id
        """
        cur.execute(query)
        products_info = cur.fetchall()
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
    
    return products_info


def check_category_exists(name):
    try:
        conn = db_botiga()
        cur = conn.cursor()
        query = "SELECT category_id FROM category WHERE name = %s"
        cur.execute(query, (name,))
        category = cur.fetchone()
        if category:
            return category[0]  # Devuelve el ID de la categoría si existe
        else:
            return None  # Devuelve None si la categoría no existe
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    finally:
        conn.close()

def create_category(name):
    try:
        conn = db_botiga()
        cur = conn.cursor()
        query = "INSERT INTO category (name) VALUES (%s)"
        cur.execute(query, (name,))
        conn.commit()
        category_id = cur.lastrowid  # Obtiene el ID de la categoría insertada
        return category_id
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    finally:
        conn.close()

def update_category(name, category_id):
    try:
        conn = db_botiga()
        cur = conn.cursor()
        query = "UPDATE category SET name = %s WHERE category_id = %s"
        cur.execute(query, (name, category_id))
        conn.commit()
        updated_rows = cur.rowcount  # Obtiene el número de filas actualizadas
        return updated_rows
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    finally:
        conn.close()

def check_subcategory_exists(name, category_id):
    try:
        conn = db_botiga()
        cur = conn.cursor()
        query = "SELECT subcategory_id FROM subcategory WHERE name = %s AND category_id = %s"
        cur.execute(query, (name, category_id))
        subcategory = cur.fetchone()
        if subcategory:
            return subcategory[0]  # Devuelve el ID de la subcategoría si existe
        else:
            return None  # Devuelve None si la subcategoría no existe
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    finally:
        conn.close()

def create_subcategory(name, category_id):
    try:
        conn = db_botiga()
        cur = conn.cursor()
        query = "INSERT INTO subcategory (name, category_id) VALUES (%s, %s)"
        cur.execute(query, (name, category_id))
        conn.commit()
        subcategory_id = cur.lastrowid  # Obtiene el ID de la subcategoría insertada
        return subcategory_id
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    finally:
        conn.close()

def update_subcategory(name, subcategory_id):
    try:
        conn = db_botiga()
        cur = conn.cursor()
        query = "UPDATE subcategory SET name = %s WHERE subcategory_id = %s"
        cur.execute(query, (name, subcategory_id))
        conn.commit()
        updated_rows = cur.rowcount  # Obtiene el número de filas actualizadas
        return updated_rows
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    finally:
        conn.close()

def check_product_exists(name, subcategory_id):
    try:
        conn = db_botiga()
        cur = conn.cursor()
        query = "SELECT product_id FROM product WHERE name = %s AND subcategory_id = %s"
        cur.execute(query, (name, subcategory_id))
        product = cur.fetchone()
        if product:
            return product[0]  # Devuelve el ID del producto si existe
        else:
            return None  # Devuelve None si el producto no existe
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    finally:
        conn.close()

def create_product(name, description, company, price, units, subcategory_id):
    try:
        conn = db_botiga()
        cur = conn.cursor()
        query = "INSERT INTO product (name, description, company, price, units, subcategory_id) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(query, (name, description, company, price, units, subcategory_id))
        conn.commit()
        product_id = cur.lastrowid  # Obtiene el ID del producto insertado
        return product_id
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    finally:
        conn.close()

def update_product(name, description, company, price, units, product_id):
    try:
        conn = db_botiga()
        cur = conn.cursor()
        query = "UPDATE product SET name = %s, description = %s, company = %s, price = %s, units = %s WHERE product_id = %s"
        cur.execute(query, (name, description, company, price, units, product_id))
        conn.commit()
        updated_rows = cur.rowcount  # Obtiene el número de filas actualizadas
        return updated_rows
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    finally:
        conn.close()