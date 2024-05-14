from typing import List, Union

from fastapi import FastAPI, HTTPException, File, UploadFile
import csv
from pydantic import BaseModel

import products
import db_botiga

app = FastAPI()

class product(BaseModel):
    name:str
    description: str
    company: str
    price: float
    units: int 
    subcategory_id: int


@app.get("/product",response_model=List[dict])
def read_products():
    return products.products_schema(db_botiga.read())


@app.get("/product/{id}", response_model=product)
def read_products_id(id:int):
    if db_botiga.read_id(id) is not None:
        product = products.product_schema(db_botiga.read_id(id))
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    return product


@app.post("/product")
async def create_product(data: product):
    name = data.name
    description = data.description
    company = data.company
    price = data.price
    units = data.units
    subcategory_id = data.subcategory_id
    l_product_id = db_botiga.create(name,description,company,price,units,subcategory_id)
    return {
        "msg": "we got data succesfully",
        "id product": l_product_id,
        "name": name
    }


@app.put("/producte/{id}")
def update_vots(id:int,preu:float):
    updated_records = db_botiga.update_preu(id,preu)
    if updated_records == 0:
       raise HTTPException(status_code=404, detail="Items to update not found") 
    
@app.delete("/delete_product/{id}")
def delete_product(id:int):
    deleted_records = db_botiga.delete_products(id)
    if deleted_records == 0:
       raise HTTPException(status_code=404, detail="Items to delete not found") 
    

@app.get("/productAll", response_model=List[dict])
def read_all_products():
    return products.products_info_schema(db_botiga.read_all_products())

@app.post("/loadProducts")
async def load_products(file: UploadFile = File(...)):
    try:
        with open(file.filename, "wb") as buffer:
            buffer.write(file.file.read())
        
        # Procesar el archivo CSV
        with open(file.filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category_name = row['nom_categoria']
                subcategory_name = row['nom_subcategoria']
                product_name = row['nom_producto']
                description = row['descripcion_producto']
                company = row['companyia']
                price = float(row['precio'])
                units = int(row['unidades'])

                # Verificar si la categoría ya existe en la base de datos
                category_id = db_botiga.check_category_exists(category_name)
                if category_id is None:
                    # Si no existe, insertarla
                    category_id = db_botiga.create_category(category_name)
                else:
                    # Si existe, actualizarla
                    db_botiga.update_category(category_name, category_id)

                # Verificar si la subcategoría ya existe en la base de datos
                subcategory_id = db_botiga.check_subcategory_exists(subcategory_name, category_id)
                if subcategory_id is None:
                    # Si no existe, insertarla
                    subcategory_id = db_botiga.create_subcategory(subcategory_name, category_id)
                else:
                    # Si existe, actualizarla
                    db_botiga.update_subcategory(subcategory_name, subcategory_id)

                # Verificar si el producto ya existe en la base de datos
                product_id = db_botiga.check_product_exists(product_name, subcategory_id)
                if product_id is None:
                    # Si no existe, insertarlo
                    db_botiga.create_product(product_name, description, company, price, units, subcategory_id)
                else:
                    # Si existe, actualizarlo
                    db_botiga.update_product(product_name, description, company, price, units, product_id)

    except Exception as e:
        return {"status": "error", "message": f"Error de carga: {e}" }

    return {"status": "success", "message": "Carga masiva completada con éxito"}