
from fastapi import APIRouter, HTTPException, status
from dependencies import dependencies
from schemas import schema
from models import models
from utils.utilities import validate
from crud import cruds

 
inventory_route=APIRouter()

LOW_STOCK_THRESHOLD=400





# Getting Inventory Status
@inventory_route.get("/get_inventory/{product_id}")
async def get_inventory_status(product_id: int, db: dependencies.db_dependency):
    product =cruds.get_product_byid_handler(db, product_id)
    validate(product, 404, 'Product not found')
    # Get the current inventory status for the product
    inventory_item = cruds.get_inventory_by_productid_handler(db, product_id)
    return {"product": product, "inventory_status": inventory_item}

# Adding product in inventory

@inventory_route.post("/create_inventory/{product_id}/inventory", status_code=status.HTTP_201_CREATED)
async def add_product_to_inventory(product_id: int, quantity: int, db: dependencies.db_dependency):
    # Retrieve product using CRUD operation
    product = cruds.get_product_byid_handler(db, product_id)
    validate(product, 404, 'Product not found')
    # Add product to inventory using CRUD operation
    inventory_item = cruds.add_product_to_inventory_handler(db, product, quantity,LOW_STOCK_THRESHOLD)
    return {"message": "Inventory added to product", "product": product, "inventory_item": inventory_item}
   

# Updating Inventory

@inventory_route.put("/update_inventory/{inventory_id}", status_code=status.HTTP_201_CREATED)
async def update_inventory(inventory: schema.InventoryBase, inventory_id: int, db: dependencies.db_dependency):
    updated_inventory = cruds.update_inventory_handler(db, inventory_id, inventory.quantity,LOW_STOCK_THRESHOLD)
    return {"Inventory": updated_inventory}

    
# Deleting Inventory
   
@inventory_route.delete('/delete-inventory/{inventory_id}')
async def delete_product(inventory_id:int,db:dependencies.db_dependency):
    inventory=cruds.delete_inventory_handler(db,inventory_id)
    return {"inventory":inventory}

    
