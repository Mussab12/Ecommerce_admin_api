from fastapi import APIRouter,HTTPException,status
from dependencies import dependencies
from schemas import schema
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from crud import cruds

from models import models

product_route=APIRouter()


# Get All Products

@product_route.get('/products/',status_code=status.HTTP_200_OK)
async def get_all_products(db:dependencies.db_dependency):
    products = cruds.get_all_products_handler(db)
    return products

# Get Product By Id
@product_route.get('/get_products/{product_id}')
def get_product_by_id(product_id: int,db: dependencies.db_dependency):
    product = cruds.get_product_byid_handler(db, product_id)
    return product

# Getting Revenue 

@product_route.get("/product/revenue/{period}")
async def get_revenue(period: str,db:dependencies.db_dependency, category: str = None):
    try:
        revenue_data = cruds.get_revenue_by_period_handler(db, period, category)
        return {"revenue_data": revenue_data}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Create Products
@product_route.post("/create_products/",status_code=status.HTTP_201_CREATED)
async def create_product(product:schema.ProductBase,db:dependencies.db_dependency):
    new_product = cruds.create_product_handler(db, product)
    return {"product":new_product}



# Update Product

@product_route.put('/update_product/{product_id}',status_code=status.HTTP_200_OK)
async def update_product(product_id:int,product:schema.ProductBase,db:dependencies.db_dependency):
    new_product = cruds.update_product_handler(db,product_id,product)
    return new_product

# Delete Product

@product_route.delete('/delete-user/{product_id}')
async def delete_product(product_id:int,db:dependencies.db_dependency):
    product=cruds.delete_product_handler(db,product_id)
    return {"product":product}


